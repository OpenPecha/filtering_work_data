from typing import Tuple, Union

from rdflib import ConjunctiveGraph, Literal, URIRef
from rdflib.namespace import Namespace

from umed_modern_filter.web_request import get_id, get_instance_info

RDF_Triple = Tuple[Union[URIRef, Literal], URIRef, Union[URIRef, Literal]]

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")


def parse_trig(file_path):
    work_dict = []
    curr = {}
    work_id = file_path.stem
    try:
        g = ConjunctiveGraph()
        g.parse(file_path, format="trig")
        instances = g.objects(BDR[work_id], BDO["workHasInstance"])
        for instance in instances:
            org_instance_id = get_id(str(instance))
            if org_instance_id[0] == "M":
                if "_" not in org_instance_id:
                    instance_id = org_instance_id
                    instance_info = get_instance_info(instance_id)
                    curr = {org_instance_id: instance_info}
                    work_dict.append(curr)
                    curr = {}
                else:
                    instance_id = org_instance_id.split("_")[0]
                    instance_info = get_instance_info(instance_id)
                    curr = {org_instance_id: instance_info}
                    work_dict.append(curr)
                    curr = {}
    except Exception as e:
        print(f"An error occurred while parsing the Trig file: {str(e)}")
    return work_dict
