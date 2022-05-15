"""
Modified version of code from https://github.com/digitalbazaar/pyld#quick-examples
with working examples.
Framing example has been taken from: https://json-ld.org/spec/latest/json-ld-framing/#framing

This script demonstrates following features of JSON-LD 1.1:
1. compaction,
2. compaction using remote context file,
3. expansion,
4. expansion of remote file,
5. flattening,
6. flattening and compaction,
7. framing,
8. normalization,
9. conversion between serialization formats: JSON-LD -> N-Quads,
10. conversion between serialization formats: N-Quads -> JSON-LD,
"""

from pyld import jsonld
import json

doc = {
    "http://schema.org/name": "Manu Sporny",
    "http://schema.org/url": {"@id": "http://manu.sporny.org/"},
    "http://schema.org/image": {"@id": "http://manu.sporny.org/images/manu.png"},
}

doc2 = {
    "http://xmlns.com/foaf/0.1/name": "Manu Sporny",
    "http://xmlns.com/foaf/0.1/homepage": {"@id": "http://manu.sporny.org/"},
    "http://xmlns.com/foaf/0.1/img": {"@id": "http://manu.sporny.org/images/manu.png"},
}

doc3 = {
    "@context": {"@vocab": "http://example.org/", "contains": {"@type": "@id"}},
    "@graph": [
        {
            "@id": "http://example.org/library",
            "@type": "Library",
            "contains": "http://example.org/library/the-republic",
        },
        {
            "@id": "http://example.org/library/the-republic",
            "@type": "Book",
            "creator": "Plato",
            "title": "The Republic",
            "contains": "http://example.org/library/the-republic#introduction",
        },
        {
            "@id": "http://example.org/library/the-republic#introduction",
            "@type": "Chapter",
            "description": "An introductory chapter on The Republic.",
            "title": "The Introduction",
        },
    ],
}

context = {
    "name": "http://schema.org/name",
    "homepage": {"@id": "http://schema.org/url", "@type": "@id"},
    "image": {"@id": "http://schema.org/image", "@type": "@id"},
}


# compact a document according to a particular context
# see: https://json-ld.org/spec/latest/json-ld/#compacted-document-form
compacted = jsonld.compact(doc, context)
print("1) Compacted JSON-LD:")
print(json.dumps(compacted, indent=2))
# Output:
# {
#   "@context": {...},
#   "image": "http://manu.sporny.org/images/manu.png",
#   "homepage": "http://manu.sporny.org/",
#   "name": "Manu Sporny"
# }

# compact using URLs
compacted2 = jsonld.compact(doc2, "http://json-ld.org/contexts/person.jsonld")
print("2) Compacted JSON-LD (other file, using remote context file):")
print(json.dumps(compacted2, indent=2))
# Output:
# {
#   "@context": "http://json-ld.org/contexts/person.jsonld",
#   "homepage": "http://manu.sporny.org/",
#   "image": "http://manu.sporny.org/images/manu.png",
#   "name": "Manu Sporny"
# }


# expand a document, removing its context
# see: https://json-ld.org/spec/latest/json-ld/#expanded-document-form
expanded = jsonld.expand(compacted)
print("3) Expanded JSON-LD:")
print(json.dumps(expanded, indent=2))
# Output:
# [{
#   "http://schema.org/image": [{"@id": "http://manu.sporny.org/images/manu.png"}],
#   "http://schema.org/name": [{"@value": "Manu Sporny"}],
#   "http://schema.org/url": [{"@id": "http://manu.sporny.org/"}]
# }]

# expand using URLs
# won't work with dummy URI
expanded2 = jsonld.expand(
    "https://raw.githubusercontent.com/w3c/json-ld-syntax/main/examples/Sample-JSON-LD-document-to-be-expanded.jsonld"
)
print("4) Expanded JSON-LD (remote jsonld):")
print(json.dumps(expanded2, indent=2))
# Output:
# [
#   {
#     "http://schema.org/image": [
#       {
#         "@id": "http://manu.sporny.org/images/manu.png"
#       }
#     ],
#     "http://schema.org/name": [
#       {
#         "@value": "Manu Sporny"
#       }
#     ],
#     "http://schema.org/url": [
#       {
#         "@id": "http://manu.sporny.org/"
#       }
#     ]
#   }
# ]


# flatten a document
# see: https://json-ld.org/spec/latest/json-ld/#flattened-document-form
flattened = jsonld.flatten(doc)
print("5) Flattened JSON-LD:")
print(json.dumps(flattened, indent=2))
# all deep-level trees flattened to the top-level

flattened_compacted = jsonld.flatten(doc, context)
print("6) Flattened and compacted JSON-LD:")
print(json.dumps(flattened_compacted, indent=2))

# frame a document
# see: https://json-ld.org/spec/latest/json-ld-framing/#introduction
frame = {
    "@context": {"@vocab": "http://example.org/"},
    "@type": "Library",
    "contains": {"@type": "Book", "contains": {"@type": "Chapter"}},
}
framed = jsonld.frame(doc3, frame)
print("7) Framed JSON-LD:")
print(json.dumps(framed, indent=2))
# Output:
# {
#   "@context": {"@vocab": "http://example.org/"},
#   "@graph": [{
#     "@id": "http://example.org/library",
#     "@type": "Library",
#     "contains": {
#       "@id": "http://example.org/library/the-republic",
#       "@type": "Book",
#       "contains": {
#         "@id": "http://example.org/library/the-republic#introduction",
#         "@type": "Chapter",
#         "description": "An introductory chapter on The Republic.",
#         "title": "The Introduction"
#       },
#       "creator": "Plato",
#       "title": "The Republic"
#     }
#   }]
# }
# document transformed into a particular tree structure per the given frame

# normalize a document using the RDF Dataset Normalization Algorithm
# (URDNA2015), see: https://json-ld.github.io/normalization/spec/
normalized = jsonld.normalize(
    doc, {"algorithm": "URDNA2015", "format": "application/n-quads"}
)
print("8) Normalized JSON-LD:")
print(json.dumps(normalized, indent=2))
# normalized is a string that is a canonical representation of the document
# that can be used for hashing, comparison, etc.


# RDF conversions between different serialization formats
## JSON-LD -> N-Quads (N-Triples)
nq_str = jsonld.to_rdf(doc, options={"format": "application/nquads"})
print("9) JSON-LD converted to N-Quads:")
print(nq_str)

## N-Quads -> JSON-LD
jsonld_obj = jsonld.from_rdf(nq_str, {"format": "application/nquads"})
print("10) N-Quads converted back to JSON-LD:")
print(json.dumps(jsonld_obj, indent=2))

# ttl conversion is not supported, but can be added with ``register_rdf_parser`` function
# ttl_str = '''
# @prefix foaf: <http://xmlns.com/foaf/0.1/> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#  [
#    foaf:name "Manu Sporny";
#    foaf:homepage <http://manu.sporny.org/>;
#    foaf:img <http://manu.sporny.org/images/manu.png>
#  ] .
# '''
# jsonld_obj = jsonld.from_rdf(ttl_str, {'format':"application/n-quads"})
# print(json.dumps(jsonld_obj, indent=2))
