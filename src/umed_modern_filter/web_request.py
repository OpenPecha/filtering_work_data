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


def get_id(URI):
    if URI == "None":
        return None
    return URI.split("/")[-1]


def parse_instance_ttl(ttl_file, ttl_id):
    script_ids = []
    print_method_ids = []
    instance_info = {}

    g = Graph()
    try:
        g.parse(data=ttl_file, format="ttl")
    except Exception as e:
        print("cant read ttl", ttl_id, e)
        return None
    script_type = g.objects(BDR[ttl_id], BDO["script"])
    for script in script_type:
        script_id = get_id(str(script))
        script_ids.append(script_id)
    print_methods = g.objects(BDR[ttl_id], BDO["printMethod"])
    for print_method in print_methods:
        print_method_id = get_id(str(print_method))
        print_method_ids.append(print_method_id)
    instance_of = g.value(BDR[ttl_id], BDO["instanceOf"])
    instance_id = get_id(str(instance_of))
    instance_info = {
        "script": script_ids,
        "printMethod": print_method_ids,
        "instanceOf": instance_id,
    }
    return instance_info


def get_instance_info(instance_id):
    ttl_file = get_ttl(instance_id)
    instance_info = parse_instance_ttl(ttl_file, instance_id)
    return instance_info
