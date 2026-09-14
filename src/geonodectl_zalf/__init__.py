"""geonodectl extension for the ZALF GeoNode backend

Brings what only the ZALF GeoNode serves into geonodectl, so geonodectl itself
stays compatible with vanilla GeoNode, see
https://github.com/GeoNodeUserGroup-DE/geonodectl/issues/133
"""

from typing import List

from geonoderest.extensions import CommandSpec, GeonodectlExtension, HandlerOverride

from geonodectl_zalf.tkeywordlabels import (
    ZalfThesauriKeywordLabelsHandler,
    build_tkeywordlabels_parser,
)
from geonodectl_zalf.tkeywords import ZalfThesauriKeywordsHandler


class ZalfExtension(GeonodectlExtension):
    name = "zalf"

    def commands(self) -> List[CommandSpec]:
        return [
            CommandSpec(
                name="tkeywordlabels",
                aliases=("thesaurikeywordlabels",),
                help="thesaurikeywordlabel commands",
                build_parser=build_tkeywordlabels_parser,
                handler_factory=ZalfThesauriKeywordLabelsHandler,
            )
        ]

    def handler_overrides(self) -> List[HandlerOverride]:
        return [
            HandlerOverride(
                command="tkeywords", handler_class=ZalfThesauriKeywordsHandler
            )
        ]


extension = ZalfExtension()
