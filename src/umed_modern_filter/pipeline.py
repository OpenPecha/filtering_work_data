import json
from pathlib import Path

from umed_modern_filter.rdf_parse import parse_trig


def main():
    final_dict = {}
    curr = {}
    cnt = 0
    directories = list(Path("../../data/gitlab/").iterdir())
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
