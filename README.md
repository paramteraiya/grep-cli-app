# grep-like Command Line Tool
A command line program that implements Unix command grep like functionality.

## Requirements

- Python 3.9 or higher

## Installation

Clone the repository:

```bash
git clone https://github.com/paramteraiya09/grep-cli-app
```

## Features
- search string in a file
- search string from the standard input
- write output to the file
- perform case-sensitive search 
- search string recursively in any of the file in a given directory
- print num lines before the match
- print num lines after the match
- print count of match 

## Usage

#### 1. To search for a pattern in a file:
```bash
python main.py search_pattern filename [options]
```

#### 2. To search for a pattern in a directory recursively:
```bash
python main.py search_pattern -r directory_path [options]
```

#### 3. To search for a pattern in standard input::
```bash
python main.py search_pattern
```

- Replace search_pattern with the pattern you want to search for. For file-based searches, provide the filename or directory_path accordingly. Include any desired options as mentioned below.

## Options
- `-o, --output_file: Specify an output file to write the results.`
- `-i, --insensitive: Perform a case-insensitive search.`
- `-C, --count_only: Print only the count of matches.`
- `-A, --lines_before_match: Print N lines before the match.`
- `-B, --lines_after_match: Print N lines after the match.`
- `-r, --recursive: Search recursively in all files in the given directory.`

## Running with Docker
If you prefer to run the program in a Docker container, follow these steps:

1. Install Docker on your machine by following the official Docker installation guide for your operating system: https://docs.docker.com/get-docker/
2. Build the Docker image using the following command:
```bash
docker build -t grep-cli-app .
```
3. Run the Docker container, mounting the input file as a volume and providing it as an argument to the Python script:
- make sure to create a txt file with some content as test.txt
```bash
docker run --rm -v "$(pwd)/test.txt:/app/test.txt" grep-cli-app test.txt [arguments]
```

## Creating a Standalone Executable with PyInstaller
If you prefer to create a standalone executable that can be run on different operating systems without Python installed, you can use PyInstaller. Follow these steps to create an executable:

1. Install PyInstaller using the following command:
```bash
pip install pyinstaller
```
2. In the terminal, navigate to the project directory that contains main.py.
```bash
pyinstaller main.py --onefile --name my_grep
```
##### This command will generate a standalone executable named my_grep in a dist directory.

The executable file will be specific to the operating system on which it was built. You'll need to repeat the build process on each target operating system to generate executables for all platforms.

### Run the test cases by executing the test_main.py file:
```bash
python test_main.py
```

## License
This project is licensed under the MIT License.
Feel free to customize the sections, commands, and examples according to your needs. 

