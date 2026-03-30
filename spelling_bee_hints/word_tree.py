from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass
import importlib.resources
from pathlib import Path


@dataclass
class LetterTreeNode:
    letter: str
    children: dict[str, LetterTreeNode]
    is_word: bool = False
    parent: LetterTreeNode | None = None

    def traverse(self, letters: str) -> LetterTreeNode | None:
        if not letters:
            return self

        next_letter = letters[0]

        if next_letter not in self.children:
            return None

        return self.children[next_letter].traverse(letters[1:])

    def add_word(self, letters: str) -> None:
        if not letters:
            self.is_word = True
            return

        next_letter = letters[0]

        if next_letter not in self.children:
            self.children[next_letter] = LetterTreeNode(
                letter=next_letter, children={}, parent=self
            )

        self.children[next_letter].add_word(letters[1:])

    @staticmethod
    def from_word_list(word_list: Iterable[str]) -> LetterTreeNode:
        root = LetterTreeNode(letter="", children={})

        for word in word_list:
            root.add_word(word)

        return root


DEFAULT_WORDS_FILE = importlib.resources.files("spelling_bee_hints").joinpath(
    "words.txt"
)


def read_words_file(override_path: Path | str | None = None) -> Iterable[str]:
    if override_path:
        with open(override_path) as f:
            for line in f:
                yield line.strip()
            return

    with DEFAULT_WORDS_FILE.open() as f:
        for line in f:
            yield line.strip()
