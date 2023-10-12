from typing import Dict, List, Tuple, Union

from rdflib import ConjunctiveGraph, Literal, URIRef

# Define a type alias for RDF triples
RDF_Triple = Tuple[Union[URIRef, Literal], URIRef, Union[URIRef, Literal]]


def parse_trig_file(trig_file_path: str) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    g = ConjunctiveGraph()
    g.parse(trig_file_path, format="trig")

    triples_by_context: Dict[str, List[RDF_Triple]] = {}
    for subject, predicate, obj, context in g.quads():
        if context not in triples_by_context:
            triples_by_context[context] = []
        triples_by_context[context].append((subject, predicate, obj))

    named_graphs_data: Dict[str, Dict[str, Dict[str, List[str]]]] = {}
    instance_dict: Dict[str, Dict[str, List[str]]] = {}

    for context, triples in triples_by_context.items():
        key = context.identifier.split("/")[-1]
        if key not in named_graphs_data:
            named_graphs_data[key] = {}
        for subject, predicate, obj in triples:
            if str(predicate).endswith("workHasInstance"):
                instance_key = obj.split("/")[-1]
                instance_dict[instance_key] = {
                    "instance_id": [],
                    "print_method": [],
                    "script": [],
                    "url": [],
                }
                named_graphs_data[key] = instance_dict

    return named_graphs_data
