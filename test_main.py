import os.path
import unittest
import subprocess
import shutil


def create_dir_for_recursive_test(directory_name):
    dir_path = os.path.join(os.getcwd(), directory_name)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(os.path.join(dir_path, 'subdir'))
    file1 = os.path.join(dir_path, 'file1.txt')
    file2 = os.path.join(dir_path, 'subdir', 'file2.txt')
    file3 = os.path.join(dir_path, 'subdir', 'file3.txt')
    with open(file1, 'w') as f:
        f.write('This is a test file.\n')
    with open(file2, 'w') as f:
        f.write('One can test a program by running test cases.\n')
    with open(file3, 'w') as f:
        f.write('This file contains a test line.\n')


def remove_temp_files():
    if os.path.exists(os.path.join(os.getcwd(), 'output.txt')):
        os.remove(os.path.join(os.getcwd(), 'output.txt'))
    if os.path.exists(os.path.join(os.getcwd(), 'param_test.txt')):
        os.remove(os.path.join(os.getcwd(), 'param_test.txt'))
    if os.path.exists(os.path.join(os.getcwd(), 'test_output.txt')):
        os.remove(os.path.join(os.getcwd(), 'test_output.txt'))
    if os.path.exists(os.path.join(os.getcwd(), 'test_recursive_search')):
        shutil.rmtree(os.path.join(os.getcwd(), 'test_recursive_search'))


class GrepTestCases(unittest.TestCase):

    def test_zero_matches(self):
        result = subprocess.run(['python', 'main.py', 'grep', 'test.txt'], capture_output=True, text=True)
        expected_output = ""
        self.assertEqual(result.stdout, expected_output)

    def test_one_match(self):
        result = subprocess.run(['python', 'main.py', 'second', 'test.txt'], capture_output=True, text=True)
        expected_output = "This is the second line.\nI found 'second' in the file.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_many_matches(self):
        result = subprocess.run(['python', 'main.py', 'line', 'test.txt'], capture_output=True, text=True)
        expected_output = "It contains multiple lines.\nThis is the first line.\nThis is the second line.\n" \
                          "This line has the search string.\n" \
                          "Another line with the search string.\n" \
                          "This line does not match the search string.\n" \
                          "I found 'line' in the file.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_file_not_found(self):
        result = subprocess.run(['python', 'main.py', 'param', 'non_existing_file.txt'], capture_output=True, text=True)
        expected_output = "File 'non_existing_file.txt' not found.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_no_read_permission(self):
        filename = "file_without_read_permission.txt"
        if not os.path.exists(os.path.join(os.getcwd(), filename)):
            with open(os.path.join(os.getcwd(), filename), "w"):
                pass
            subprocess.run(['chmod', '-r', filename])

        result = subprocess.run(['python', 'main.py', 'line', filename], capture_output=True, text=True)
        expected_output = f"No read permission for file '{filename}'.\n"
        self.assertEqual(result.stdout, expected_output)

        subprocess.run(['chmod', '+r', os.path.join(os.getcwd(), filename)])
        subprocess.run(['rm', os.path.join(os.getcwd(), filename)])

    # TODO: Need to handle this!
    # def test_different_file_encoding(self):
    #     # Create a test file with a specific encoding
    #     filename = "encoded_file.txt"
    #     encoding = "utf-16"  # Replace with the desired file encoding
    #     content = "This is a test file with different encoding."
    #
    #     with open(filename, 'w', encoding=encoding) as file:
    #         file.write(content)
    #
    #     # Run the command to search for a string in the file
    #     result = subprocess.run(['python', 'main.py', 'test', filename], capture_output=True, text=True)
    #
    #     # Check the expected output based on the file encoding and content
    #     expected_output = "This is a test file with different encoding.\nI found 'test' in the file.\n"
    #     self.assertEqual(result.stdout, expected_output)
    #
    #     # Clean up the test file
    #     os.remove(filename)

    def test_output_file_write(self):
        output_filename = "output.txt"
        if os.path.exists(os.path.join(os.getcwd(), output_filename)):
            os.remove(os.path.join(os.getcwd(), output_filename))
        expected_content = "This is the second line.\n"
        result = subprocess.run(['python', 'main.py', 'second', 'test.txt', '-o', output_filename], capture_output=True,
                                text=True)
        # check if the command executed successfully
        self.assertEqual(result.returncode, 0)

        # check if the file created or not
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), output_filename)))

        # check if the file has the expected content or not
        with open(os.path.join(os.getcwd(), output_filename), 'r') as file:
            file_content = file.read()
        self.assertEqual(file_content, expected_content)

    def test_output_file_already_exists(self):
        output_filename = "test_output.txt"
        existing_content = "This is existing content, which should not change!"
        if not os.path.exists(os.path.join(os.getcwd(), output_filename)):
            with open(os.path.join(os.getcwd(), output_filename), 'w') as file:
                file.write(existing_content)

        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), output_filename)))

        # Run the command that should not overwrite the existing file and should print the desired error
        result = subprocess.run(['python', 'main.py', 'second', 'test.txt', '-o', output_filename], capture_output=True,
                                text=True)
        expected_output = "Output file 'output.txt' already exists."
        self.assertNotEqual(result.stdout, expected_output)  # Check if the command fails

        # Verify that the file's content remains unchanged
        with open(output_filename, 'r') as file:
            file_content = file.read()
        self.assertEqual(file_content, existing_content)

    def test_case_insensitive_search(self):
        result = subprocess.run(['python', 'main.py', 'second', 'test.txt', '-i'], capture_output=True, text=True)
        expected_output = "This is the second line.\nTHIS IS SECOND TEST LINE for case-insensitive.\nI found " \
                          "'second' in the file.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_grep_stdin(self):
        result = subprocess.run(
            ['python', 'main.py', 'foo'], text=True, capture_output=True, input='bar\nbarbazfoo\nFoobar\nfood'
        )
        expected_output = "barbazfoo\nfood\nI found 'foo' in the file.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_grep_stdin_with_output_file(self):
        output_filename = "param_test.txt"
        expected_content = "barbazfoo\nfood\n"
        result = subprocess.run(
            ['python', 'main.py', 'foo', '-o', output_filename], text=True, capture_output=True,
            input='bar\nbarbazfoo\nFoobar\nfood'
        )
        # check if the command executed successfully
        self.assertEqual(result.returncode, 0)

        # check if the file created or not
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), output_filename)))

        # check if the file has the expected content or not
        with open(os.path.join(os.getcwd(), output_filename), 'r') as file:
            file_content = file.read()
        self.assertEqual(file_content, expected_content)

    def test_grep_stdin_with_count_only(self):
        result = subprocess.run(
            ['python', 'main.py', '-C', 'foo'], text=True, capture_output=True, input='bar\nbarbazfoo\nFoobar\nfood'
        )
        expected_output = "2\n"  # Expected count of matches
        self.assertEqual(result.stdout, expected_output)

    def test_lines_before_match(self):
        result = subprocess.run(['python', 'main.py', 'second', 'test.txt', '-A', '1'], capture_output=True, text=True)
        expected_output = "This is the first line.\nThis is the second line.\nI found 'second' in the file.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_lines_after_match(self):
        result = subprocess.run(['python', 'main.py', 'second', 'test.txt', '-B', '2'], capture_output=True, text=True)
        expected_output = "This is the second line.\nThis line has the search string.\n" \
                          "The search string is repeated here.\nI found 'second' in the file.\n"

        self.assertEqual(result.stdout, expected_output)

    def test_recursive_search(self):
        dir_name = "test_recursive_search"
        create_dir_for_recursive_test(dir_name)
        result = subprocess.run(['python', 'main.py', 'test', dir_name, '-r'], capture_output=True, text=True)
        expected_output = 'test_recursive_search/file1.txt: This is a test file.\n' \
                          'test_recursive_search/subdir/file2.txt: One can test a program by running test cases.\n' \
                          'test_recursive_search/subdir/file3.txt: This file contains a test line.\n'
        self.assertEqual(result.stdout, expected_output)

    def test_recursive_search_case_insensitive(self):
        result = subprocess.run(['python', 'main.py', 'TEst', 'test_recursive_search', '-r', '-i'], capture_output=True,
                                text=True)
        expected_output = 'test_recursive_search/file1.txt: This is a test file.\n' \
                          'test_recursive_search/subdir/file2.txt: One can test a program by running test cases.\n' \
                          'test_recursive_search/subdir/file3.txt: This file contains a test line.\n'
        self.assertEqual(result.stdout, expected_output)

    def test_recursive_search_count_only(self):
        result = subprocess.run(['python', 'main.py', 'test', 'test_recursive_search', '-r', '-C'], capture_output=True,
                                text=True)
        expected_output = 'test_recursive_search/file1.txt: 1\n' \
                          'test_recursive_search/subdir/file2.txt: 1\n' \
                          'test_recursive_search/subdir/file3.txt: 1\n'
        self.assertEqual(result.stdout, expected_output)

    def test_lines_before_after_recursive(self):
        if not os.path.exists('test_recursive_search'):
            create_dir_for_recursive_test('test_recursive_search')
        result = subprocess.run(['python', 'main.py', 'test', 'test_recursive_search', '-r', '-A', '1', '-B', '1'],
                                capture_output=True, text=True)
        expected_output = 'test_recursive_search/file1.txt: This is a test file.\n' \
                          'test_recursive_search/file1.txt: \n' \
                          'test_recursive_search/subdir/file2.txt: One can test a program by running test cases.\n' \
                          'test_recursive_search/subdir/file2.txt: \n' \
                          'test_recursive_search/subdir/file3.txt: This file contains a test line.\n' \
                          'test_recursive_search/subdir/file3.txt: \n'
        self.assertEqual(result.stdout, expected_output)

    def test_recursive_search_directory_not_found(self):
        dir_name = "non_existing_directory"
        result = subprocess.run(['python', 'main.py', 'test', dir_name, '-r'], capture_output=True, text=True)
        expected_output = f"Directory '{dir_name}' not found.\n"
        self.assertEqual(result.stdout, expected_output)

    def test_recursive_search_empty_directory(self):
        dir_name = "empty_directory"
        if not os.path.exists(os.path.join(os.getcwd(), dir_name)):
            os.mkdir(dir_name)
        result = subprocess.run(['python', 'main.py', 'test', dir_name, '-r'], capture_output=True, text=True)
        expected_output = f"No files found in directory '{dir_name}'.\n"
        self.assertEqual(result.stdout, expected_output)
        shutil.rmtree(dir_name)

    def test_recursive_search_empty_subdirectory(self):
        dir_name = "empty_sub_directory"
        if not os.path.exists(os.path.join(os.getcwd(), dir_name)):
            os.makedirs(os.path.join(dir_name, 'subdir'))
        result = subprocess.run(['python', 'main.py', 'test', dir_name, '-r'], capture_output=True, text=True)
        expected_output = f"No files found in directory '{dir_name}'.\n"
        self.assertEqual(result.stdout, expected_output)
        shutil.rmtree(dir_name)


if __name__ == '__main__':
    remove_temp_files()
    unittest.main()
