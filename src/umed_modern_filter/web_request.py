import json

import requests
from rdflib import Graph, Namespace

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")


def get_ttl(work_id):
    try:
        ttl = requests.get(f"http://purl.bdrc.io/graph/{work_id}.ttl")
        return ttl.text
    except Exception as e:
        print(" TTL not Found!!!", e)
        return None


def parse_ttl_file(turtle_file_data):
    # Create a new RDF graph
    g = Graph()
    # Create a new dictionary to store the instance information
    instance_info = {}
    try:
        # Load the Turtle file into the graph
        g.parse(data=turtle_file_data, format="turtle")
        instance_info = {"printMethod": [], "script": [], "instanceOf": ""}
        for s, p, o in g:
            if (
                str(p).endswith("printMethod")
                or str(p).endswith("script")
                or str(p).endswith("instanceOf")
            ):
                objects = []
                # Query the graph to retrieve the objects
                for obj in g.objects(s, p):
                    val = obj.split("/")[-1]
                    objects.append(val)
                predicate = p.split("/")[-1]
                instance_info[predicate] = objects
        return instance_info
    except Exception as e:
        print(f"An error occurred while parsing the Turtle file: {e}")
        return None


def get_instance_info(instance_id):
    ttl_file = get_ttl(instance_id)
    instance_info = parse_ttl_file(ttl_file)
    return instance_info


def save_dict_to_json(nested_dict, file_path):
    try:
        with open(file_path, "w") as json_file:
            json.dump(nested_dict, json_file)
        print(f"Nested dictionary saved to {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
