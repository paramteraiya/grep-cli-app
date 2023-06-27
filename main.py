# Importing required libraries
import argparse
import os
import re
import sys


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
        return []

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
            matches.extend(array_of_strings[i+1:end])
    matches = [s.strip("\n") for s in matches]
    return matches


def search_files_recursive(directory: str, search_pattern: str, case_insensitive: bool = False,
                           count_only: bool = False, lines_before: int = 0, lines_after: int = 0) -> None:
    """
    Recursively search files in a directory for a pattern and print the matched lines along with its file name.

    :param directory: directory to search in
    :param search_pattern: pattern to search for
    :param case_insensitive: flag for case-insensitive search (default value is False, search for case-sensitive)
    :param count_only: flag to only print the count of matching (default is False)
    :param lines_before: number of lines to include before a match (default is 0)
    :param lines_after: number of lines to include after a match (default is 0)
    :return: list of matching lines
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file_content:
                    result = search_pattern_in_strings(search_pattern, file_content.readlines(), case_insensitive,
                                                       lines_before, lines_after)
                    if result:
                        if count_only:
                            print(f"{filepath}: {len(result)}")
                        else:
                            if lines_before:
                                print(f"{filepath}: {''.join(result[:lines_before])}")
                            print(f"{filepath}: {''.join(result[lines_after:])}")


def my_grep(search_pattern: str, filename: str = None, output_file_path: str = None, case_insensitive: bool = False
            , count_only: bool = False, lines_before: int = 0, lines_after: int = 0,
            recursive: bool = False) -> None:
    """
    Search provided string/pattern in file/STDIN/directory and print the matches

    :param case_insensitive:
    :param output_file_path:
    :param filename:
    :param search_pattern:
    :param recursive:
    :param count_only:
    :param lines_before:
    :param lines_after:
    :return: None
    """
    # search_string = re.compile(search_string)
    if recursive and filename:
        search_files_recursive(filename, search_pattern, case_insensitive, count_only, lines_before,
                               lines_after)
        return
    if filename:
        # filepath is variable which has the value for filename relative path
        filepath = os.path.join(os.getcwd(), filename)
        # checks if the file does not exist
        if not os.path.exists(filepath):
            print(f"File '{filename}' not found.")
            return
        # checks weather file has the read access or not
        if not os.access(filepath, os.R_OK):
            print(f"No read permission for file '{filename}'.")
            return

        # open a file and iterate through line by line to check weather the provided string exists in the line or not
        stream = open(filepath, 'r')
    else:
        stream = sys.stdin
    result = search_pattern_in_strings(search_pattern, stream.readlines(), case_insensitive, lines_before
                                       , lines_after)

    # checks if the filename for output has been provided
    if output_file_path and result:
        if os.path.exists(os.path.join(os.getcwd(), output_file_path)):
            print(f"Output file '{output_file_path}' already exists.")
            return
        with open(os.path.join(os.getcwd(), output_file_path), 'w') as output_file_content:
            if count_only:
                output_file_content.write(str(len(result)) + '\n')
            else:
                for line in result:
                    output_file_content.write(line + '\n')
            return
    if result:
        if count_only:
            print(len(result))
            return

        if lines_before:
            print("\n".join(result[:lines_before]))

        print("\n".join(result[lines_before:]))
        print(f"I found '{search_pattern}' in the file.")
        return


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
    my_grep(args.search_string, filename=args.filename, output_file_path=args.output_file,
            case_insensitive=args.insensitive, count_only=args.count_only, lines_before=args.lines_before_match,
            lines_after=args.lines_after_match, recursive=args.recursive)
