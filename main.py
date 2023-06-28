# Importing required libraries
import argparse
import os
import re
import sys
import codecs


def search_pattern_in_strings(search_pattern: str, array_of_strings: list, case_insensitive: bool = False,
                              lines_before: int = 0, lines_after: int = 0) -> list:
    """
    Search a pattern from list of strings and return the matching lines.

    :param search_pattern: pattern to search for
    :param array_of_strings: list of strings to search from
    :param case_insensitive: flag for case-insensitive search (default value is False, search for case-sensitive)
    :param lines_before: number of lines to include before a match (default is 0)
    :param lines_after: number of lines to include after a match (default is 0)
    :return: list of matching lines
    """
    if not array_of_strings:
        return "", []

    # list to store the matching lines
    matches = []

    for i, line in enumerate(array_of_strings):
        if re.search(search_pattern, line, re.IGNORECASE if case_insensitive else 0):
            # line matches the search pattern

            # add lines before the match
            start = max(i - lines_before, 0)
            matches.extend(array_of_strings[start:i])

            # add the matched line
            matches.append(line.strip())

            # add lines after the match
            end = min(i + lines_after + 1, len(array_of_strings))
            matches.extend(array_of_strings[i + 1:end])
    matches = [s.strip("\n") for s in matches]
    return "", matches


def search_files_recursive(directory: str, search_pattern: str, case_insensitive: bool = False,
                           count_only: bool = False, lines_before: int = 0, lines_after: int = 0) -> tuple:
    """
    Recursively search files in a directory for a pattern and return the matched lines along with its file name.

    :param directory: directory to search in
    :param search_pattern: pattern to search for
    :param case_insensitive: flag for case-insensitive search (default value is False, search for case-sensitive)
    :param count_only: flag to only return the count of matching (default is False)
    :param lines_before: number of lines to include before a match (default is 0)
    :param lines_after: number of lines to include after a match (default is 0)
    :return: tuple containing the error message (if any) and the list of matching lines
    """
    if not os.path.isdir(directory):
        return f"Directory '{directory}' not found.", []

    files_found = False  # Flag to check if any files are found in the directory or its subdirectories

    matches = []

    for root, dirs, files in os.walk(directory):
        if not files and not dirs:
            # Directory is empty
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                files_found = True
                try:
                    with open(filepath, 'r') as file_content:
                        result = search_pattern_in_strings(search_pattern, file_content.readlines(), case_insensitive,
                                                           lines_before, lines_after)
                        if result[1]:
                            if count_only:
                                matches.append(f"{filepath}: {len(result[1])}")
                            else:
                                if lines_before:
                                    matches.append(f"{filepath}: {''.join(result[1][:lines_before])}")
                                matches.append(f"{filepath}: {''.join(result[1][lines_after:])}")
                except UnicodeDecodeError as e:
                    return f"Error reading file '{filepath}': {e}", []
    if not files_found:
        return f"No files found in directory '{directory}'.", []
    return "", matches


def my_grep(search_pattern: str, filename: str = None, output_file_path: str = None, case_insensitive: bool = False,
            count_only: bool = False, lines_before: int = 0, lines_after: int = 0,
            recursive: bool = False) -> tuple:
    """
    Search provided string/pattern in file/STDIN/directory and return the matches

    :param case_insensitive:
    :param output_file_path:
    :param filename:
    :param search_pattern:
    :param recursive:
    :param count_only:
    :param lines_before:
    :param lines_after:
    :return: tuple containing the error message (if any) and the list of matching lines
    """
    # search_string = re.compile(search_string)
    if recursive and filename:
        return search_files_recursive(filename, search_pattern, case_insensitive, count_only, lines_before,
                                      lines_after)
    if filename:
        # filepath is variable which has the value for filename relative path
        filepath = os.path.join(os.getcwd(), filename)
        # checks if the file does not exist
        if not os.path.exists(filepath):
            return f"File '{filename}' not found.", []
        # checks weather file has the read access or not
        if not os.access(filepath, os.R_OK):
            return f"No read permission for file '{filename}'.", []
        stream = []
        try:
            # open a file and iterate through line by line to check weather the provided string exists in the line or
            # not
            stream = codecs.open(filepath, 'r', encoding='utf-8')
        except IsADirectoryError as err:
            return f'{err}', []
        except UnicodeDecodeError as e:
            return f"Error decoding file '{filepath}' with encoding 'utf-8'", []
    else:
        stream = sys.stdin
    if stream:
        result = search_pattern_in_strings(search_pattern, stream.readlines(), case_insensitive, lines_before,
                                           lines_after)
    else:
        result = []

    if output_file_path and result[1]:
        if os.path.exists(os.path.join(os.getcwd(), output_file_path)):
            return f"Output file '{output_file_path}' already exists.", []
        with open(os.path.join(os.getcwd(), output_file_path), 'w') as output_file_content:
            if count_only:
                output_file_content.write(str(len(result[1])) + '\n')
            else:
                for line in result[1]:
                    output_file_content.write(line + '\n')
            return "", result[1]

    if result[1]:
        if count_only:
            return "", [len(result[1])]

        output_lines = []
        if lines_before:
            output_lines.append("\n".join(result[1][:lines_before]))

        output_lines.append("\n".join(result[1][lines_before:]))
        output_lines.append(f"I found '{search_pattern}' in the file.")
        return "", output_lines
    return "", []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="search for a string/patten in the file.")
    parser.add_argument('search_string', type=str, help="the string to search for")
    parser.add_argument('filename', type=str, help="the filename to search from", nargs="?")
    parser.add_argument('-o', '--output_file', type=str, help="the file to write output")
    parser.add_argument('-i', '--insensitive', action='store_true', help='This will allow case-insensitive search')
    parser.add_argument('-C', '--count_only', action='store_true', help='Print only the count of matches')
    parser.add_argument('-A', '--lines_before_match', type=int, help="Print N lines before the match", default=0)
    parser.add_argument('-B', '--lines_after_match', type=int, help="Print N lines after the match", default=0)
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Search recursively in all files in the given directory')
    args = parser.parse_args()
    error_message, result = my_grep(args.search_string, filename=args.filename, output_file_path=args.output_file,
                                    case_insensitive=args.insensitive, count_only=args.count_only,
                                    lines_before=args.lines_before_match,
                                    lines_after=args.lines_after_match, recursive=args.recursive)
    if error_message:
        print(f"{error_message}")
    else:
        for line in result:
            print(line)
