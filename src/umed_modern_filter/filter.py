from umed_modern_filter.create_dict import create_dictionary, pretty_print_dict
from umed_modern_filter.update_dict import update_dictionary


def traverse_nested_dict(input_dict):
    filter_list = []
    for key, value in input_dict.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, dict):
                    if (
                        v["printMethod"] == "PrintMethod_Manuscript"
                        and v["script"] == "ScriptDbuMed"
                    ):
                        filter_list.append(k)
    return filter_list


if __name__ == "__main__":

    root_directory = "/home/gangagyatso/Desktop/experiment"
    data_dictionary = create_dictionary(root_directory)
    pretty_print_dict(data_dictionary)
    update_data = update_dictionary(data_dictionary)
    print("\n --updated dictionary-- \n")
    pretty_print_dict(update_data)
    filter_list = []
    filter_list = traverse_nested_dict(update_data)
    print(filter_list)
