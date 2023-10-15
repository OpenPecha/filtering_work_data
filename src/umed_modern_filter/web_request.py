import requests


def get_ttl(work_id):
    try:
        ttl = requests.get(f"http://purl.bdrc.io/graph/M{work_id}.ttl")
        return ttl.text
    except Exception as e:
        print(" TTL not Found!!!", e)
        return None


print(get_ttl("W00KG01589"))
