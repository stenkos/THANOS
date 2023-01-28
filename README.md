# THANOS
This script deletes half of the files in a directory. It is meant to be used in the command line.
## Installation & Usage
To use this script you must have the `pathlib` library, which is in the `requirements.txt` file. Then, you can clone the repository using this git command:
```
git clone https://github.com/stenkos/THANOS.git
```
Then, run the script using this command, where `<directory>` is the folder you would like to unleash wrath on:
```
python THANOS.py <directory>
```
Alternatively, you can download the binary on the releases and replace `python THANOS.py` with `thanos`.
### Compatibility
This code was designed for compatibility for a Windows file system, and thus the code may not function as intended in a system such as Linux or macOS.

## To-do (i probably won't update this)
- [ ] Fix PermissionError that causes the script to skip files
