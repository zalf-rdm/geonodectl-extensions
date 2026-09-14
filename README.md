# geonodectl-zalf

A [geonodectl](https://github.com/GeoNodeUserGroup-DE/geonodectl) extension for the ZALF GeoNode
backend. It adds what only the ZALF GeoNode serves, so geonodectl itself stays compatible with
vanilla GeoNode.

| Command | Capabilities | Notes |
|---|---|---|
| `tkeywordlabels` (`thesaurikeywordlabels`) | list, describe | `describe` takes the keyword identifier, e.g. `describe soil` |
| `tkeywords` | list, describe | `list` additionally shows the `keyword` column |

## Installation

```bash
pip install geonodectl-zalf
geonodectl extensions list   # zalf should show as loaded
```

It requires geonodectl 0.4 and is picked up automatically, nothing needs to be configured.

## Usage

```bash
export GEONODE_API_URL=https://your-geonode-instance/api/v2/
export GEONODE_API_BASIC_AUTH=$(echo -n user:password | base64)

geonodectl tkeywordlabels list --filter lang=de
geonodectl tkeywordlabels describe soil
geonodectl tkeywords list
```

As a library:

```python
from geonoderest.apiconf import GeonodeApiConf
from geonoderest.extensions import get_handler
from geonodectl_zalf.tkeywordlabels import ZalfThesauriKeywordLabelsHandler

conf = GeonodeApiConf.from_env_vars()
labels = ZalfThesauriKeywordLabelsHandler(env=conf)
labels.get(pk="soil")

# the same through geonodectl, overrides of built-in commands included
get_handler("tkeywordlabels", conf)
get_handler("tkeywords", conf)  # -> ZalfThesauriKeywordsHandler
```

Code that imported `geonoderest.tkeywordlabels.GeonodeThesauriKeywordLabelsRequestHandler` from
geonodectl < 0.4 only needs to change the import to `geonodectl_zalf.tkeywordlabels`, the old class
name is kept there.

## Development

```bash
pip install -e ../geonodectl          # until geonodectl 0.4 is released
pip install -e .[test]
pre-commit install
pytest
```

The tests find the extension through its entry point, so it has to be installed (`pip install -e .`).
See geonodectl's [docs/extensions.md](https://github.com/GeoNodeUserGroup-DE/geonodectl/blob/main/docs/extensions.md)
for how extensions work.

## License

GPL-3.0, see [LICENSE](LICENSE).
