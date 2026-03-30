import unittest
from click.testing import CliRunner

from spelling_bee_hints.main import main


class MainEndToEndTest(unittest.TestCase):
    def _invoke_with_words_file(self, words: list[str], *args: str):
        runner = CliRunner()
        words_content = "\n".join(words) + "\n"
        with runner.isolated_filesystem():
            with open("words.txt", "w") as f:
                _ = f.write(words_content)

            result = runner.invoke(main, [*args, "--words-file", "words.txt"])
        return result

    def test_outputs_valid_words_with_required_and_optional_letters(self) -> None:
        result = self._invoke_with_words_file(
            ["peal", "pale", "leap", "plea", "apple", "ale", "zebra"],
            "--required",
            "e",
            "--letters",
            "apl",
            "--min-length",
            "4",
        )

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertSetEqual(
            set(result.output.splitlines()),
            {"peal", "pale", "leap", "plea", "apple"},
        )

    def test_case_sensitive_flag_changes_matching_behavior(self) -> None:
        words = ["ABCA", "abca"]

        default_result = self._invoke_with_words_file(
            words,
            "-r",
            "A",
            "-l",
            "BC",
            "-m",
            "4",
        )
        sensitive_result = self._invoke_with_words_file(
            words,
            "-r",
            "A",
            "-l",
            "BC",
            "-m",
            "4",
            "--case-sensitive",
        )

        self.assertEqual(default_result.exit_code, 0, default_result.output)
        self.assertEqual(sensitive_result.exit_code, 0, sensitive_result.output)
        self.assertSetEqual(set(default_result.output.splitlines()), {"abca"})
        self.assertSetEqual(set(sensitive_result.output.splitlines()), {"ABCA"})

    def test_no_matches_prints_nothing(self) -> None:
        result = self._invoke_with_words_file(
            ["dog", "cat", "bird"],
            "-r",
            "e",
            "-l",
            "abcd",
        )

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "")

    def test_missing_required_option_returns_error(self) -> None:
        result = CliRunner().invoke(main, ["--letters", "abcdef"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--required'", result.output)


if __name__ == "__main__":
    _ = unittest.main()
