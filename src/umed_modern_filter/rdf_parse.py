from typing import Dict, List, Tuple, Union

from rdflib import ConjunctiveGraph, Literal, URIRef
from umed_modern_filter.web_request import get_instance_info

# Define a type alias for RDF triples
RDF_Triple = Tuple[Union[URIRef, Literal], URIRef, Union[URIRef, Literal]]


def parse_trig_file(trig_file_path: str) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    curr = {}
    work_dict = {}
    work_id = trig_file_path.name.split(".")[0]
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
                instance_id = obj.split("/")[-1]
                if instance_id[0] == "M":
                    if "_" not in instance_id:
                        instance_info = get_instance_info(instance_id)
                        curr[work_id].append(instance_info)
                        work_dict.update(curr)
                        curr ={}
                    else:
                        instance_id = instance_id.split("_")[0]
                        instance_info = get_instance_info(instance_id)
                        curr[work_id].append(instance_info)
                        work_dict.update(curr)
                        curr ={}


    return named_graphs_data
