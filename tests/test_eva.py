
import sys
import unittest
import tempfile
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVA_SOURCE = PROJECT_ROOT / "src" / "eva"
sys.path.insert(0, str(EVA_SOURCE))

import main as eva


class TestEVA(unittest.TestCase):

    def test_greeting(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_greeting()

        self.assertIn("EVA", output.getvalue())

    def test_help(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_help()

        self.assertIn("search", output.getvalue())

    def test_capabilities(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_capabilities()

        self.assertIn("approved", output.getvalue().lower())

    def test_show_date(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_date()

        self.assertIn("Today's date", output.getvalue())

    def test_show_time(self):
        output = StringIO()

        with redirect_stdout(output):
            eva.show_time()

        self.assertIn("Current time", output.getvalue())

    @patch.object(eva.webbrowser, "open", return_value=True)
    def test_search_web(self, mock_open):
        query = "Python Programming"

        eva.search_web(query)

        expected_url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        mock_open.assert_called_once_with(expected_url)

    @patch.object(eva.webbrowser, "open")
    def test_empty_search(self, mock_open):
        output = StringIO()

        with redirect_stdout(output):
            eva.search_web("")

        mock_open.assert_not_called()
        self.assertIn("enter something", output.getvalue().lower())

    @patch.object(eva, "search_web")
    def test_search_command_without_query(self, mock_search):
        output = StringIO()

        with redirect_stdout(output):
            eva.handle_search_command("search")

        mock_search.assert_not_called()

    @patch.object(eva, "search_web")
    def test_search_command_with_query(self, mock_search):
        eva.handle_search_command(
            "search Python Programming"
        )

        mock_search.assert_called_once_with(
            "Python Programming"
        )

    def test_application_allowlist(self):
        self.assertIn("notepad", eva.APP_ALLOWLIST)
        self.assertIn("calculator", eva.APP_ALLOWLIST)
        self.assertNotIn("powershell", eva.APP_ALLOWLIST)

    @patch.object(eva.subprocess, "Popen")
    @patch.object(eva, "resolve_application", return_value=None)
    def test_unapproved_application_not_launched(
        self, mock_resolve, mock_popen
    ):
        output = StringIO()

        with redirect_stdout(output):
            eva.open_application("powershell")

        mock_resolve.assert_not_called()
        mock_popen.assert_not_called()
        self.assertIn("not in my approved list", output.getvalue())

    def test_website_allowlist(self):
        self.assertIn("google", eva.WEBSITE_ALLOWLIST)
        self.assertNotIn("example", eva.WEBSITE_ALLOWLIST)

    @patch.object(eva.webbrowser, "open")
    def test_unapproved_website_not_opened(self, mock_open):
        output = StringIO()

        with redirect_stdout(output):
            eva.open_website("example")

        mock_open.assert_not_called()
        self.assertIn("not in my approved list", output.getvalue())

    def test_folder_allowlist(self):
        self.assertIn("eva", eva.FOLDER_ALLOWLIST)
        self.assertNotIn("system32", eva.FOLDER_ALLOWLIST)

    def test_folder_path_validation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = eva.validate_folder_path(temp_dir)

            self.assertIsNotNone(result)
            self.assertTrue(Path(result).is_dir())

    def test_invalid_folder_path(self):
        result = eva.validate_folder_path(
            str(Path("Z:/EVA_FOLDER_THAT_DOES_NOT_EXIST"))
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
