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
@click.option(
    "--case-sensitive",
    help=(
        "Enable case sensitivity for the required and optional letters,"
        + " and the word list"
    ),
    is_flag=True,
    default=False,
    show_default=True,
)
def main(
    required: str,
    letters: str,
    min_length: int,
    words_file: str | None,
    case_sensitive: bool,
) -> None:
    words = read_words_file(words_file)
    if not case_sensitive:
        required = required.lower()
        letters = letters.lower()
        words = (word.lower() for word in words)
    tree = LetterTreeNode.from_word_list(words)

    for word in find_words(tree, required, letters, min_length):
        click.echo(word)


def find_words(
    root_node: LetterTreeNode,
    required: str,
    letters: str,
    min_length: int,
) -> Iterable[str]:
    attempt_stack: list[tuple[str, LetterTreeNode]] = [("", root_node)]
    letter_choices = set(letters + required)

    while attempt_stack:
        current_attempt, current_node = attempt_stack.pop()

        if (
            current_node.is_word
            and len(current_attempt) >= min_length
            and all(letter in current_attempt for letter in required)
        ):
            yield current_attempt

        for letter in letter_choices:
            if letter in current_node.children:
                attempt_stack.append(
                    (current_attempt + letter, current_node.children[letter])
                )


if __name__ == "__main__":
    main()
