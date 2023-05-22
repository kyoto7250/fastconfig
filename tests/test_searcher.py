import unittest
from pathlib import Path

from fastconfig import find_project_root, is_project_root, search


class TestSearch(unittest.TestCase):
    def test_search(self) -> None:
        # file search
        self.assertIsNotNone(search(target="README.md"))
        self.assertIsNotNone(search(target="README.md", path="tests/"))
        self.assertIsNotNone(
            search(target="README.md", path="tests/", end_up_the_project_root=False)
        )
        self.assertIsNone(
            search(
                target="README.md",
                path="./a/b/c/d/e/f/g/h/i/j/k/l/m/n",
                end_up_the_project_root=False,
            )
        )

        # not found file search
        self.assertIsNone(search(target="README.txt"))
        self.assertIsNone(search(target="README.txt", path="tests/"))
        self.assertIsNone(
            search(target="README.txt", path="tests/", end_up_the_project_root=False)
        )

        # directory search
        self.assertIsNotNone(search(target=".git/"))
        self.assertIsNotNone(search(target=".git/", path="tests/"))
        self.assertIsNotNone(
            search(target=".git/", path="tests/", end_up_the_project_root=False)
        )
        self.assertIsNone(
            search(
                target=".git/",
                path="./a/b/c/d/e/f/g/h/i/j/k/l/m/n",
                end_up_the_project_root=False,
            )
        )

        # not found directory search
        self.assertIsNone(search(target=".hg/"))
        self.assertIsNone(search(target=".hg/", path="tests/"))
        self.assertIsNone(
            search(target=".hg/", path="tests/", end_up_the_project_root=False)
        )

    def test_is_project_root(self) -> None:
        # str
        self.assertTrue(is_project_root("./"))
        self.assertTrue(is_project_root("./README.md"))
        self.assertFalse(is_project_root("tests/"))
        self.assertFalse(is_project_root("tests/README.txt"))

        # Path
        self.assertTrue(is_project_root(Path("./")))
        self.assertFalse(is_project_root(Path("./hoge.txt")))
        self.assertFalse(is_project_root(Path("tests/")))
        self.assertFalse(is_project_root(Path("tests/hoge.txt")))

    def test_find_project_root(self) -> None:
        # str
        self.assertIsNotNone(find_project_root("./"))
        self.assertIsNotNone(find_project_root("./tests"))
        self.assertIsNone(find_project_root("./a/b/c/d/e/f/g/h/i/j/k/j/l/m/n"))

        # Path
        self.assertIsNotNone(find_project_root(Path("./")))
        self.assertIsNotNone(find_project_root(Path("./tests")))
        self.assertIsNone(find_project_root(Path("./a/b/c/d/e/f/g/h/i/j/k/j/l/m/n")))

        # None
        self.assertIsNotNone(find_project_root())
