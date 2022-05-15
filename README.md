# JSON-LD Demo

Repository contains scripts and information useful for starting with
[JSON-LD](https://json-ld.org/) tools (Python and CLI).

## Tools
### Python
#### PyLD
The official Python library supporting version 1.1 is [pyLD](https://github.com/digitalbazaar/pyld).

##### demo
[demo.py](./demo.py) presents available features of _pyLD_ and _JSON-LD 1.1_:
1. compaction,
2. compaction using remote context file,
3. expansion,
4. expansion of remote file,
5. flattening,
6. flattening and compaction,
7. framing,
8. normalization,
9. conversion between serialization formats: JSON-LD -> N-Quads,
10. conversion between serialization formats: N-Quads -> JSON-LD.


##### RDF Serialization formats
_pyLD_ provides possibility to convert from or to JSON-LD.
Currently, only ``N-Quads`` and ``N-Triples`` are supported. Conversion for
other formats can be added using ``jsonld.register_rdf_parser`` function.


#### Rdflib
[Rdflib](https://github.com/RDFLib/rdflib) supports version 1.0 of JSON-LD. It
does not provide support for current JSON-LD 1.1 version, which introduces
important improvements. There are some [plans]((https://github.com/RDFLib/rdflib/pull/1836))
to use _pyLD_ as parser for _rdflib_ and fulfill in that way the
need for JSON-LD 1.1 support in _rdflib_.

### CLI
#### jsonld-cli
[jsonld-cli](https://github.com/digitalbazaar/jsonld-cli) is a CLI tool based on
[jsonld.js](https://github.com/digitalbazaar/jsonld.js).

##### examples
1. Convert remote jsonld file to nquads format:
```bash
jsonld format \
    -f nquads \
    https://raw.githubusercontent.com/w3c/json-ld-syntax/main/examples/Sample-JSON-LD-document-to-be-expanded.jsonld
```
1. Compact local file using remote context file:
```bash
jsonld compact \
    -c http://json-ld.org/contexts/person.jsonld \
    data/file02-exmanded.jsonld
```

#### pyLD
_pyLD_ does not provide official CLI. [cli.py](./cli.py) is a script adding CLI support for
_pyLD_, proposed by Wes Turner.
