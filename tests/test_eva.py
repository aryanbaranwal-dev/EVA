import sys
import unittest
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.parse import quote_plus

# Add the EVA source folder to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVA_SOURCE = PROJECT_ROOT / "src" / "eva"
sys.path.insert(0, str(EVA_SOURCE))

import main as eva


class TestEVA(unittest.TestCase):

    # Test 1: Greeting
    def test_greeting(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_greeting()

        self.assertIn("EVA", output.getvalue())

    # Test 2: Help command
    def test_help(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_help()

        self.assertTrue(len(output.getvalue()) > 0)

    # Test 3: Capabilities command
    def test_capabilities(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_capabilities()

        self.assertTrue(len(output.getvalue()) > 0)

    # Test 4: Date command
    def test_show_date(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_date()

        self.assertTrue(len(output.getvalue()) > 0)

    # Test 5: Time command
    def test_show_time(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_time()

        self.assertTrue(len(output.getvalue()) > 0)

    # Test 6: Google search opens the correct URL
    @patch.object(eva.webbrowser, "open", return_value=True)
    def test_search_web(self, mock_open):
        query = "Python programming"

        eva.search_web(query)

        expected_url = (
            "https://www.google.com/search?q=" + quote_plus(query)
        )

        mock_open.assert_called_once_with(expected_url)

    # Test 7: Empty search should not open a browser
    @patch.object(eva.webbrowser, "open")
    def test_empty_search(self, mock_open):
        output = StringIO()

        with redirect_stdout(output):
            eva.search_web("")

        mock_open.assert_not_called()

    # Test 8: Search command without query
    @patch.object(eva, "search_web")
    def test_search_command_without_query(self, mock_search):
        output = StringIO()

        with redirect_stdout(output):
            eva.handle_search_command("search")

        mock_search.assert_not_called()

    # Test 9: Search command with a query
    @patch.object(eva, "search_web")
    def test_search_command_with_query(self, mock_search):
        eva.handle_search_command("search Java interview questions")

        mock_search.assert_called_once_with("Java interview questions")


if __name__ == "__main__":
    unittest.main(verbosity=2)