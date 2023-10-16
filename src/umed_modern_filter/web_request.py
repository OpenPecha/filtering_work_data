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

    try:
        # Load the Turtle file into the graph
        g.parse(data=turtle_file_data, format="turtle")
        
        # Create a new dictionary to store the instance information
        instance_info = {}
        return instance_info
    except Exception as e:
        print(f"An error occurred while parsing the Turtle file: {e}")
        return None


def get_instance_info(instance_id):
    ttl_file = get_ttl(instance_id)
    instance_info = parse_ttl_file(ttl_file)
    return instance_info
