import json
from pathlib import Path
import hashlib
from umed_modern_filter.rdf_parse import parse_trig
from umed_modern_filter.web_request import get_instance_info


def get_hash(work_id):
    md5 = hashlib.md5(str.encode(work_id))
    two = md5.hexdigest()[:2]
    return two

def main():
    final_dict = {}
    curr = {}
    work_ids = Path(f"./keys.txt").read_text().splitlines()
    for work_id in work_ids:
        work_dict = get_instance_info(f"M{work_id}")
        curr[work_id] = work_dict
        final_dict.update(curr)
        curr = {}
    file_path = Path(f"./json_list.json")
    with file_path.open("w") as json_file:
        json.dump(final_dict, json_file, indent=4)

def main():
    final_dict = {}
    curr = {}
    cnt = 0
    directories = list(Path("./data/gitlab/").iterdir())
    for dir in directories:
        cnt = cnt + 1
        if Path(f"../../data/json/{dir.name}.json").exists():
            print(cnt, "directory already exist", dir.name)
        else:
            workfile_paths = list(dir.iterdir())
            for workfile_path in workfile_paths:
                work_id = workfile_path.stem
                work_dict = parse_trig(workfile_path)
                curr[work_id] = work_dict
                final_dict.update(curr)
                curr = {}
            dir_name = dir.name
            write_json(final_dict, dir_name, cnt)


def write_json(data, dir_name, cnt):
    file_path = Path(f"../../data/json/{dir_name}.json")
    with file_path.open("w") as json_file:
        json.dump(data, json_file, indent=4)

    print(cnt, "JSON file updated or created successfully.", dir_name)


if __name__ == "__main__":
    main()
