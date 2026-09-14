from typing import List

from geonoderest.geonodetypes import GeonodeCmdOutListKey, GeonodeCmdOutObjectKey
from geonoderest.tkeywords import GeonodeThesauriKeywordsRequestHandler


class ZalfThesauriKeywordsHandler(GeonodeThesauriKeywordsRequestHandler):
    """tkeywords as the ZALF GeoNode serves them, with their keyword identifier

    Takes over the built-in `tkeywords` command through a HandlerOverride.
    """

    LIST_CMDOUT_HEADER: List[GeonodeCmdOutObjectKey] = [
        GeonodeCmdOutListKey(key="keyword"),
        *GeonodeThesauriKeywordsRequestHandler.LIST_CMDOUT_HEADER,
    ]
