from pathlib import Path

from umed_modern_filter.rdf_parse import filter_dict, parse_trig_file


def main():
    final_dict = {}
    directories = list(Path("/home/gangagyatso/Desktop/experiment").iterdir())
    for dir in directories:
        workfile_paths = list(dir.iterdir())
        for workfile_path in workfile_paths:
            work_dict = parse_trig_file(str(workfile_path))
            final_dict.update(work_dict)
    print(final_dict)
    filter_list = filter_dict(final_dict)
    print(filter_list)


if __name__ == "__main__":
    main()
