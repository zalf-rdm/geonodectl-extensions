import argparse
import logging
from typing import Dict, List, Optional, Union

from geonoderest.cliutils import SubParsers, kwargs_append_action
from geonoderest.cmdprint import print_json
from geonoderest.exitcodes import EXIT_FAILED, EXIT_OK
from geonoderest.geonodeobject import GeonodeObjectHandler
from geonoderest.geonodetypes import GeonodeCmdOutListKey, GeonodeCmdOutObjectKey


class ZalfThesauriKeywordLabelsHandler(GeonodeObjectHandler):
    ENDPOINT_NAME = "tkeywordlabels"
    JSON_OBJECT_NAME = "ThesaurusKeywordLabels"
    SINGULAR_RESOURCE_NAME = "ThesaurusKeywordLabels"

    LIST_CMDOUT_HEADER: List[GeonodeCmdOutObjectKey] = [
        GeonodeCmdOutListKey(key="keyword"),
        GeonodeCmdOutListKey(key="lang"),
        GeonodeCmdOutListKey(key="label"),
    ]

    def cmd_describe(self, pk: str, **kwargs) -> int:
        """print the labels of a keyword

        Args:
            pk (str): keyword identifier. Not a numeric pk, so it takes no range
                or list like the pks of the other commands do.

        Returns:
            int: EXIT_OK, or EXIT_FAILED when the labels could not be fetched
        """
        obj = self.get(pk=pk, **kwargs)
        if obj is None:
            logging.error(f"describing {pk} failed ... ")
            return EXIT_FAILED
        print_json(obj)
        return EXIT_OK

    def get(self, pk: Union[int, str], **kwargs) -> Optional[Dict]:
        """
        get details for a given keyword (identifier)

        Args:
            pk (Union[int, str]): keyword of the object

        Returns:
            Dict: obj details
        """
        r = self.http_get(endpoint=f"{self.ENDPOINT_NAME}?keyword={pk}")
        if r is None:
            return None
        return r[self.SINGULAR_RESOURCE_NAME]


# the name it had in geonodectl < 0.4, so library code only changes the import
GeonodeThesauriKeywordLabelsRequestHandler = ZalfThesauriKeywordLabelsHandler


def build_tkeywordlabels_parser(
    thesaurikeywordlabels: argparse.ArgumentParser,
) -> SubParsers:
    thesaurikeywordlabels_subparsers = thesaurikeywordlabels.add_subparsers(
        help="geonodectl thesaurikeywordlabels commands",
        dest="subcommand",
        required=True,
    )

    # LIST
    thesaurikeywordlabels_list = thesaurikeywordlabels_subparsers.add_parser(
        "list", help="list thesaurikeywordlabels"
    )
    thesaurikeywordlabels_list.add_argument(
        "--filter",
        nargs="*",
        action=kwargs_append_action,
        dest="filter",
        type=str,
        help="filter thesaurikeywordlabels requests by key value pairs. E.g. --filter lang=de label=Abbau",
    )
    thesaurikeywordlabels_list.add_argument(
        "--ordering",
        dest="ordering",
        default="keyword",
        type=str,
        help="Which field to use when ordering the results. --ordering keyword (default: keyword)",
    )
    thesaurikeywordlabels_list.add_argument(
        "--search",
        dest="search",
        type=str,
        required=False,
        help="A search term to filter the results by. --search uuid",
    )

    # DESCRIBE
    thesaurikeywordlabels_describe = thesaurikeywordlabels_subparsers.add_parser(
        "describe", help="get thesaurikeywordlabels details"
    )
    # not fully clean to use pk here, as it is actually keyword but for now ...
    thesaurikeywordlabels_describe.add_argument(
        type=str, dest="pk", help="keyword of thesaurikeywordlabels to describe ..."
    )
    return thesaurikeywordlabels_subparsers
