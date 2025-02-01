# Anil Raut's Take-Home OA

## Flow Log Parser
A Python script that processes AWS VPC flow logs and maps network traffic to tags based on destination port and protocol. This helps categorize and analyze network traffic efficiently.

## Files Included
* `flow_log_parser.py`: The main Python script that does all the heavy lifting.
* `flow_logs.txt`: Sample flow log data (You can name your file whatever you like, just be sure to reference the correct name when running the script).
* `lookup_table.csv`: A simple lookup table mapping ports and protocols to specific tags.

These files are provided to help you quickly test the code and understand how it works.

## How to Run the Script
Run the script from the terminal like this:
```bash
python3 flow_log_parser.py <your_flow_log_file.txt> <your_lookup_file.csv> <output_file.txt>
```

Example:
```bash
python3 flow_log_parser.py flow_logs.txt lookup_table.csv report.txt
```

**Note:** Ensure that the filenames match the ones in your system. If your `.txt` or `.csv` file has a different name, modify the command accordingly.

## Requirements
* Python 3.x
* No extra libraries required (everything runs on built-in Python functions)
* ASCII-encoded input files (no fancy Unicode stuff)
* Only supports AWS VPC Flow Logs in **default** format, **version 2**

## How I Verified the Code
* **Manual validation** with a small sample size to ensure the results make sense.
* **Checked output correctness** by comparing results against expected outcomes.

## Implementation Details & Assumptions

### File Handling
* Max flow log file size: **10MB** (Prevents the script from consuming too much memory)
* Max lookup table size: **10,000 mappings** (Keeps lookups efficient)
* All files must be **ASCII-encoded** (No special characters that could break parsing)

### Flow Log Processing
* **Only supports Version 2 AWS VPC Flow Logs**
* **Uses the default log format** (Custom formats are not handled)
* **Extracts only destination port & protocol** for tag mapping
* **Ignores incomplete or malformed log entries** to keep things running smoothly

### Tag Mapping
* **Case-insensitive matching** for protocols and tags
* **Defaults to "Untagged"** if no match is found
* **Supports multiple tags per port/protocol combination**

## Why These Design Choices?
1. **Dictionaries for Fast Lookups:** Mapping ports/protocols to tags is O(1) instead of scanning through a list.
2. **File Size Validation:** Prevents large files from overwhelming memory.
3. **Robust Error Handling:** Ensures the script doesn't crash due to bad input.
4. **ASCII Encoding:** Guarantees compatibility with simple text-based logs.
5. **Modular Code Structure:** Easy to modify, extend, and debug.

## What I Tested
* Input validation (ensuring bad data doesn't break execution)
* Handling of large files
* Correct mapping of ports & protocols to tags
* Ensuring the right number of tags are counted
* Proper error handling for malformed data
* Checking output formatting for consistency
* Monitoring memory usage during execution

## Final Thoughts
The script is designed to be **efficient, easy to maintain, and robust** while following all requirements. If you have any feedback or suggestions for improvement, let me know!

Happy coding! 🚀
