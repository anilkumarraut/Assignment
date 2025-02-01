# Anil Raut Take Home OA

# Flow Log Parser

A Python program that parses AWS VPC flow logs and maps traffic to tags based on destination port and protocol combinations.

## Files Included
- `flow_log_parser.py`: Main Python script
- `flow_logs.txt`: Sample flow log data
- `lookup_table.csv`: Port/protocol to tag mapping file

## How to Run
```bash
python3 flow_log_parser.py <flow_logs.txt> <lookup_table.csv> <output.txt>
```

Example:
```bash
python3 flow_log_parser.py flow_logs.txt lookup_table.csv report.txt
```

## Requirements
- Python 3.x
- No additional packages required (uses only standard library)
- ASCII-encoded input files
- Flow logs must be in default AWS VPC format, version 2

## Implementation Details & Assumptions

### File Processing
- Flow log file size limit: 10MB
- Lookup table limit: 10,000 mappings
- All files must be ASCII-encoded

### Flow Log Processing
- Only supports AWS VPC Flow Logs version 2
- Uses default log format only (no custom formats)
- Processes destination port and protocol for mapping
- Skips malformed or incomplete log lines

### Tag Mapping
- Case-insensitive matching for protocols and tags
- Uses "Untagged" for unmatched combinations
- Supports multiple port/protocol combinations per tag

## Technical Decisions
1. Used dictionaries for O(1) lookup performance
2. Implemented size validation to prevent memory issues
3. Added error handling for malformed data
4. Used ASCII encoding for universal compatibility
5. Structured code for easy maintenance and testing

## Testing Performed
- Input validation testing
- File size limit verification
- Protocol mapping verification
- Tag assignment accuracy
- Error handling for malformed data
- Memory usage monitoring
- Output format validation

The code has been structured to be efficient, maintainable, and robust while meeting all specified requirements.
