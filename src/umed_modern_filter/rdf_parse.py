from pathlib import Path
from typing import Dict, List, Tuple, Union
from rdflib import ConjunctiveGraph, Literal, URIRef
from umed_modern_filter.web_request import get_instance_info, get_id
RDF_Triple = Tuple[Union[URIRef, Literal], URIRef, Union[URIRef, Literal]]
from rdflib.namespace import RDF, RDFS, SKOS, OWL, Namespace, NamespaceManager, XSD

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")


def parse_trig_file(trig_file_path: str) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    curr = {}
    work_dict = {}
    # Assuming trig_file_path is a string, convert it to a Path object
    trig_path = Path(trig_file_path)

    # Extract the base filename (without extension)
    work_id = trig_path.stem
    g = ConjunctiveGraph()
    g.parse(trig_file_path, format="trig")

    for graph in g.contexts():
        for subject, predicate, obj in graph:
            if str(predicate).endswith("workHasInstance"):
                org_instance_id = obj.split("/")[-1]
                if org_instance_id[0] == "M":
                    if "_" not in org_instance_id:
                        instance_id = org_instance_id
                        instance_info = get_instance_info(instance_id)
                        curr[work_id] = {
                            org_instance_id : instance_info
                        }
                        work_dict.update(curr)
                        curr = {}
                    else:
                        instance_id = org_instance_id.split("_")[0]
                        instance_info = get_instance_info(instance_id)
                        curr[work_id] = {
                            org_instance_id : instance_info
                            }
                        work_dict.update(curr)
                        curr = {}
    return work_dict


def parse_trig(file_path):
    work_dict = []
    curr = {}
    work_id = file_path.stem
    g = ConjunctiveGraph()
    g.parse(file_path, format="trig")
    instances = g.objects(BDR[work_id], BDO["workHasInstance"])
    for instance in instances:
        org_instance_id = get_id(str(instance))
        if org_instance_id[0] == "M":
            if "_" not in org_instance_id:
                instance_id = org_instance_id
                instance_info = get_instance_info(instance_id)
                curr = {
                    org_instance_id : instance_info
                }
                work_dict.append(curr)
                curr = {}
            else:
                instance_id = org_instance_id.split("_")[0]
                instance_info = get_instance_info(instance_id)
                curr = {
                    org_instance_id : instance_info
                    }
                work_dict.append(curr)
                curr = {}
    return work_dict

def filter_dict(input_dict):
    filter_list = []
    for key, value in input_dict.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if (
                    "PrintMethod_Manuscript" in v["printMethod"]
                    and "ScriptDbuMed" in v["script"]
                ):
                    filter_list.append(k)
    return filter_list
