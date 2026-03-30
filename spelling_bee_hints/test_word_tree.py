import unittest

from spelling_bee_hints.word_tree import LetterTreeNode


class LetterTreeNodeTest(unittest.TestCase):
    def _must_traverse(self, node: LetterTreeNode, letters: str) -> LetterTreeNode:
        result = node.traverse(letters)
        self.assertIsNotNone(result, f"Expected to find path for '{letters}'")
        assert result is not None  # for type checker
        return result

    def test_traverse_empty_string_returns_same_node(self) -> None:
        node = LetterTreeNode(children={})

        self.assertIs(node.traverse(""), node)

    def test_traverse_missing_path_returns_none(self) -> None:
        root = LetterTreeNode.from_word_list(["able"])

        self.assertIsNone(root.traverse("ax"))

    def test_add_word_marks_only_terminal_node_as_word(self) -> None:
        root = LetterTreeNode(children={})

        root.add_word("cart")

        self.assertFalse(root.is_word)
        self.assertFalse(self._must_traverse(root, "c").is_word)
        self.assertFalse(self._must_traverse(root, "car").is_word)
        self.assertTrue(self._must_traverse(root, "cart").is_word)

    def test_from_word_list_builds_shared_prefixes(self) -> None:
        root = LetterTreeNode.from_word_list(["cat", "car", "dog"])

        self.assertIsNotNone(root.traverse("ca"))
        self.assertTrue(self._must_traverse(root, "cat").is_word)
        self.assertTrue(self._must_traverse(root, "car").is_word)
        self.assertTrue(self._must_traverse(root, "dog").is_word)
        self.assertIsNone(root.traverse("cab"))

    def test_duplicate_words_do_not_break_tree(self) -> None:
        root = LetterTreeNode.from_word_list(["bee", "bee"])

        self.assertTrue(self._must_traverse(root, "bee").is_word)
        self.assertIsNone(root.traverse("bees"))


if __name__ == "__main__":
    _ = unittest.main()
