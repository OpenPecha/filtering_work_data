from umed_modern_filter.create_dict import create_dictionary, pretty_print_dict
from umed_modern_filter.parse_ttl import parse_turtle_file
from umed_modern_filter.web_request import get_ttl


def update_dictionary(data):
    for key, value in data.items():
        inner_dict_1 = {}
        if isinstance(value, dict):
            # If the value is a dictionary, process its keys
            for inner_key in value.keys():
                if inner_key.startswith("W"):
                    turtle_file_data = get_ttl(str(inner_key))
                    turtle_graph = parse_turtle_file(turtle_file_data)
                    inner_dict_2 = {}
                    for s, p, o in turtle_graph:
                        if (
                            str(p).endswith("printMethod")
                            or str(p).endswith("script")
                            or str(p).endswith("instanceOf")
                        ):
                            val = o.split("/")[-1]
                            predicate = p.split("/")[-1]
                            inner_dict_2[predicate] = val
                    inner_dict_1[inner_key] = inner_dict_2
        data[key] = inner_dict_1
    return data


if __name__ == "__main__":

    root_directory = "/home/gangagyatso/Desktop/experiment"
    data_dictionary = create_dictionary(root_directory)
    pretty_print_dict(data_dictionary)
    update_data = update_dictionary(data_dictionary)
    print("\n --updated dictionary-- \n")
    pretty_print_dict(update_data)
