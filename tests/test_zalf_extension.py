"""geonodectl-zalf plugged into geonodectl through its entry point

The extension has to be installed (``pip install -e .``): finding it through
the entry point is exactly what these tests check.
"""

import contextlib
import io
import os
import unittest
from importlib.metadata import entry_points
from unittest.mock import patch

from geonoderest import extensions
from geonoderest.apiconf import GeonodeApiConf
from geonoderest.exitcodes import EXIT_OK
from geonoderest.extensions import ENTRY_POINT_GROUP, get_handler, list_extensions
from geonoderest.geonodectl import geonodectl

from geonodectl_zalf import ZalfExtension
from geonodectl_zalf.tkeywordlabels import ZalfThesauriKeywordLabelsHandler
from geonodectl_zalf.tkeywords import ZalfThesauriKeywordsHandler

ENV = {
    "GEONODE_API_URL": "https://example.org/api/v2/",
    "GEONODE_API_BASIC_AUTH": "dXNlcjpwYXNz",
}
CONF = GeonodeApiConf(
    url=ENV["GEONODE_API_URL"], auth_basic=ENV["GEONODE_API_BASIC_AUTH"], verify=True
)
LABELS = {
    "ThesaurusKeywordLabels": [{"keyword": "soil", "lang": "de", "label": "Boden"}]
}


def _run(*argv):
    """run geonodectl with the given argv, return its exit code and output"""
    out = io.StringIO()
    with (
        patch("sys.argv", ["geonodectl", *argv]),
        patch("logging.basicConfig"),
        contextlib.redirect_stdout(out),
    ):
        code = geonodectl()
    return code, out.getvalue()


class ZalfTestCase(unittest.TestCase):
    def setUp(self):
        extensions._loaded_extensions = None
        self.addCleanup(setattr, extensions, "_loaded_extensions", None)


class TestEntryPoint(ZalfTestCase):
    def test_extension_is_registered(self):
        installed = {ep.name: ep for ep in entry_points(group=ENTRY_POINT_GROUP)}
        self.assertIn("zalf", installed, "install the extension: pip install -e .")
        self.assertIsInstance(installed["zalf"].load(), ZalfExtension)

    def test_extension_loads_without_errors(self):
        [zalf] = [ext for ext in list_extensions() if ext.name == "zalf"]
        self.assertIsNone(zalf.error)


class TestTkeywordlabels(ZalfTestCase):
    def test_library_handler_by_name_and_alias(self):
        for command in ("tkeywordlabels", "thesaurikeywordlabels"):
            with self.subTest(command=command):
                self.assertIsInstance(
                    get_handler(command, CONF), ZalfThesauriKeywordLabelsHandler
                )

    @patch.dict(os.environ, ENV, clear=True)
    @patch.object(ZalfThesauriKeywordLabelsHandler, "http_get", return_value=LABELS)
    def test_describe_asks_for_the_keyword(self, mock_http_get):
        code, out = _run("tkeywordlabels", "describe", "soil")
        self.assertEqual(code, EXIT_OK)
        mock_http_get.assert_called_once_with(endpoint="tkeywordlabels?keyword=soil")
        self.assertIn("Boden", out)

    @patch.dict(os.environ, ENV, clear=True)
    @patch.object(ZalfThesauriKeywordLabelsHandler, "http_get", return_value=LABELS)
    def test_list_passes_the_filter_on(self, mock_http_get):
        code, out = _run("tkeywordlabels", "list", "--filter", "lang=de")
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(mock_http_get.call_args.kwargs["params"]["filter{lang}"], "de")
        self.assertIn("soil", out)


class TestTkeywords(ZalfTestCase):
    def test_zalf_handler_takes_over_the_builtin_command(self):
        self.assertIsInstance(
            get_handler("tkeywords", CONF), ZalfThesauriKeywordsHandler
        )

    @patch.dict(os.environ, ENV, clear=True)
    @patch.object(ZalfThesauriKeywordsHandler, "http_get")
    def test_list_shows_the_keyword_column(self, mock_http_get):
        mock_http_get.return_value = {
            "tkeywords": [
                {
                    "keyword": "k-4711",
                    "thesaurus": {"slug": "inspire"},
                    "name": "soil",
                    "slug": "soil",
                    "uri": "https://example.org/soil",
                }
            ]
        }
        code, out = _run("tkeywords", "list")
        self.assertEqual(code, EXIT_OK)
        self.assertIn("keyword", out.splitlines()[0])
        self.assertIn("k-4711", out)


if __name__ == "__main__":
    unittest.main()
