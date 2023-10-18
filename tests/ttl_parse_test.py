from umed_modern_filter.web_request import parse_instance_ttl


def test_parse_ttl():
    file_path = "./data/MW3PD988.ttl"
    with open(file_path) as file:
        file_content = file.read()

    instance_info = {}
    instance_id = "MW3PD988"
    instance_info = parse_instance_ttl(file_content, instance_id)
    expected_dict = {
        "script": ["ScriptDbuMed", "ScriptTibt", "ScriptDbuCan"],
        "printMethod": [
            "PrintMethod_Manuscript",
            "PrintMethod_Relief_WoodBlock",
            "PrintMethod_Modern",
        ],
        "instanceOf": "WA3PD988",
    }
    print(instance_info)

    assert instance_info == expected_dict
