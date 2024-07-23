# Robot Framework Keyword Police

## Overview

This script searches through files within a specified directory (and its subdirectories) and identify unused keywords and variables. It first collects all the items from all the files. A keyword is identified by any line under "Keywords" section that DOESN'T start with at least two empty spaces. Logic for the variables is the same except it looks them under "Variables" and excludes the value instead of saving the whole line. The script then checks if these items are used elsewhere in ANY of the files and lists the unused ones. Used item is determined by finding the string in a line that DOES start with at least two spaces. Commented lines (starting with #) are discarded.

**The script doesn't automatically delete or modify any of the files!**

Note that this hasn't been fully tested and is expected to have some issues.

## Usage

The script can be run with optional arguments as follows

```bash
python keyword_police.py --directory <path_to_directory> --file-types <file_extensions>
```

See explanations with the --help flag

```bash
python keyword_police.py --help
```
