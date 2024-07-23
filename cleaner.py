import os
import argparse
import re

def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description="This script searches through files in the specified directory and lists unused keywords and variables."
    )

    parser.add_argument(
        "--directory",
        type=str,
        default="./",
        help="The root directory where the script will search for items. Defaults to the current directory."
    )

    parser.add_argument(
        "--file-types",
        nargs='+',
        type=str,
        default=[".txt", ".robot"],
        help="The type(s) of file(s) where the script will search items from. Defaults to .txt and .robot."
    )

    return  parser.parse_args()

def get_all_files(root_dir, file_types):
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(file_type) for file_type in file_types):
                file_list.append(os.path.join(root, file))
    return file_list

def collect_keywords_and_variables(file_paths):
    items_dict = {}
    for file_path in file_paths:
        capture_keywords = False
        capture_variables = False
        keywords = set()
        variables = set()

        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()

                # Start capturing keywords
                if stripped_line == '*** Keywords ***':
                    capture_keywords = True
                    capture_variables = False
                    continue
                
                # Start capturing variables
                if stripped_line == '*** Variables ***':
                    capture_variables = True
                    capture_keywords = False
                    continue

                # Stop capturing lines when a new section starts
                if line.startswith('***'):
                    capture_keywords = False
                    capture_variables = False

                # Items are identified by having no identation, not commented and not being an empty line
                if capture_keywords and not line.startswith('  ') and not line.startswith('#') and stripped_line != '':
                    keywords.add(stripped_line)

                if capture_variables and not line.startswith('  ') and not line.startswith('#') and stripped_line != '':
                    # Split line to extract variable name and not its value
                    variable_name = re.split(r' {2,}', stripped_line)[0]
                    variables.add(variable_name)

        if keywords or variables:
            items_dict[file_path] = {"keywords": keywords, "variables": variables}

    return items_dict

def get_unused_keywords_and_variables(items_dict):
    # Generate sets containing all keywords and variables
    all_keywords = set(keyword for file_items in items_dict.values() for keyword in file_items["keywords"])
    all_variables = set(variable for file_items in items_dict.values() for variable in file_items["variables"])
    unused_items_dict = {file_path: {"keywords": items["keywords"].copy(), "variables": items["variables"].copy()} for file_path, items in items_dict.items()}

    # Iterate over each file and its lines
    for file_path in items_dict:
        with open(file_path, 'r') as file:
            for line in file:
                # Only process lines that start with identation
                if line.startswith('  '):
                    # Break line in to segments separated with atleast two spaces and loop through them separately
                    # to make sure we don't skip keywords that would be substrings of other keywords, etc.
                    line_segments = line.strip().split('  ')
                    for segment in line_segments:
                        segment_stripped = segment.strip()
                        for keyword in all_keywords:
                            if segment_stripped == keyword:
                                for file_items in unused_items_dict.values():
                                    file_items["keywords"].discard(keyword)
                        for variable in all_variables:
                            if segment_stripped == variable:
                                for file_items in unused_items_dict.values():
                                    file_items["variables"].discard(variable)

    return {file_path: {"keywords": list(items["keywords"]), "variables": list(items["variables"])} for file_path, items in unused_items_dict.items() if items["keywords"] or items["variables"]}

def list_results(unused_items):
    if any(len(items["keywords"]) > 0 or len(items["variables"]) > 0 for items in unused_items.values()):
        print('\n### Found unused items ###\n')
        for file_path, items in unused_items.items():
            print(f"{file_path}:")
            if items["keywords"]:
                print("  Unused Keywords:")
                for keyword in items["keywords"]:
                    print(f"    - {keyword}")
            if items["variables"]:
                print("  Unused Variables:")
                for variable in items["variables"]:
                    print(f"    - {variable}")
            print()
    else:
        print('\n### No unused items found! ###\n')

if __name__ == '__main__':
    args = parse_command_line_args()
    files = get_all_files(args.directory, args.file_types)
    all_items = collect_keywords_and_variables(files)
    unused_items = get_unused_keywords_and_variables(all_items)
    list_results(unused_items)
