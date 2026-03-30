from collections.abc import Iterable
import click

from spelling_bee_hints.word_tree import LetterTreeNode, read_words_file


@click.command()
@click.option("--required", "-r", help="Required letter(s)", required=True)
@click.option("--letters", "-l", help="Optional letters to use", required=True)
@click.option(
    "--min-length",
    "-m",
    help="Minimum word length",
    default=4,
    show_default=True,
)
@click.option("--words-file", "-w", help="Override the default words file")
def main(
    required: str,
    letters: str,
    min_length: int,
    words_file: str | None,
) -> None:
    words = read_words_file(words_file)
    tree = LetterTreeNode.from_word_list(words)

    for word in find_words(tree, required, letters, min_length):
        click.echo(word)


def find_words(
    root_node: LetterTreeNode,
    required: str,
    letters: str,
    min_length: int,
) -> Iterable[str]:
    attempt_stack = [""]

    while attempt_stack:
        current_attempt = attempt_stack.pop()

        node = root_node.traverse(current_attempt)
        if node is None:
            continue

        if (
            node.is_word
            and len(current_attempt) >= min_length
            and all(letter in current_attempt for letter in required)
        ):
            yield current_attempt

        for letter in set(letters + required):
            attempt_stack.append(current_attempt + letter)


if __name__ == "__main__":
    main()
