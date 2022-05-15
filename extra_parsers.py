"""
Module registers custom rdf parsers for pyLD, using rdflib built-in parsers.
Uses rdflib_pyld_compat as it reformats rdflib to pyLD expected format.
"""
from functools import partial

from pyld.jsonld import register_rdf_parser
from rdflib import Graph
from rdflib_pyld_compat.convert import _pyld_dataset_from_rdflib_graph

def rdflib_parser(rdf_str, format=None):
    g = Graph()
    g.parse(data=rdf_str, format=format)
    graph = _pyld_dataset_from_rdflib_graph(g)
    return graph if isinstance(graph, dict) else {'@default': graph}


def register_rdflib_parsers():
    register_rdf_parser('application/rdf+xml', rdflib_parser)
    register_rdf_parser('application/n-triples', partial(rdflib_parser, format='nt'))
    register_rdf_parser('application/ntriples', partial(rdflib_parser, format='nt'))
    register_rdf_parser('text/turtle', partial(rdflib_parser, format='turtle'))
