#!/usr/bin/env python3

# Anil Raut
# These comment are like student comments to share my understanding of this code knowledge with you (not the industry level comment)


"""
Approach to Solving the Problem:
1) Followed all the requirement details given in the problem statement and structured the implementation accordingly.
   - Used ASCII encoding to ensure compatibility with legacy systems and prevent encoding issues
   - Implemented size limits to prevent memory overload (10MB for logs, 1MB for lookup files)
   - Built parser specifically for version 2 flow logs due to their standardized format

2) Ensured compliance with constraints through:
   - File size validation before processing to fail fast
   - ASCII encoding checks to maintain data integrity
   - Version 2 flow log format validation using field count and version marker
   
3) Implemented lookup mechanism using dictionaries because:
   - O(1) constant time lookup performance for port/protocol combinations
   - Memory efficient for storing sparse mappings
   - Easy to update and maintain mappings dynamically
   
4) Verified results through:
   - Input validation at each processing step
   - Error handling for malformed data
   - Consistent output formatting
   
5) Handled edge cases through:
   - Try-except blocks to gracefully handle parsing errors
   - Protocol number to name mapping for common protocols
   - Default "Untagged" category for unknown combinations
"""

import sys  
import os   

class FlowParser:  
    def __init__(self, lookup_path):
        # Dictionary for O(1) lookup performance instead of linear search through list
        self.lookup_dict = {}          # Maps (port, protocol) tuples to tags for instant lookups
        self.tag_count = {}            # Tracks tag frequencies using dictionary for efficient updates
        self.traffic_count = {}        # Stores traffic statistics with port/protocol as composite key
        
        # Load lookups immediately to fail fast if lookup file has issues
        self._load_lookups(lookup_path)
    
    def _load_lookups(self, path):
        try:
            # Counter for mapping limit enforcement
            num_mappings = 0
            
            # ASCII encoding ensures text-only content and catches binary/unicode files early
            with open(path, 'r', encoding='ascii') as f:
                # Skip header to avoid processing metadata as actual mapping
                next(f)
                
                for line in f:
                    # Hard limit of 10000 mappings for memory management
                    if num_mappings >= 10000:
                        print("Warning: Reached 10000 mapping limit")
                        break
                    
                    # Skip empty lines to handle file formatting issues
                    if not line.strip():
                        continue
                    
                    try:
                        # Parse each mapping line into components
                        port, proto, tag = line.strip().split(',')
                        
                        # Create composite key for consistent lookup
                        # Integer port for numeric comparison, lowercase protocol for case-insensitive matching
                        key = (int(port), proto.lower())
                        
                        self.lookup_dict[key] = tag
                        num_mappings += 1
                        
                    except ValueError as e:
                        # Skip malformed lines without failing entire process
                        print(f"Skipping bad line: {line.strip()}")
                        
        except UnicodeDecodeError:
            # Fail early if file contains non-ASCII data
            raise ValueError("Lookup file must be ASCII text")
    
    def _parse_line(self, line):
        try:
            # Split on whitespace as per v2 flow log format
            fields = line.strip().split()
            
            # Version 2 logs have minimum 14 fields and start with '2'
            # This validation ensures we only process v2 format logs
            if len(fields) < 14 or fields[0] != '2':
                return None
            
            # Extract destination port from field 6 as per v2 format specification
            dst_port = int(fields[6])
            
            # Map numeric protocols to names for readability
            # Common protocols mapped to standard names
            proto_map = {
                '6': 'tcp',    # TCP - Transmission Control Protocol
                '17': 'udp',   # UDP - User Datagram Protocol
                '1': 'icmp',   # ICMP - Internet Control Message Protocol
                '50': 'esp',   # ESP - Encapsulating Security Payload
                '51': 'ah'     # AH - Authentication Header
            }
            
            # Use protocol name if known, otherwise use protocol number with prefix
            protocol = proto_map.get(fields[7], f"proto_{fields[7]}")
            
            return dst_port, protocol
            
        except (ValueError, IndexError):
            # Return None for any parsing failures to skip malformed lines
            return None
    
    def process_logs(self, log_path):
        # 10MB size limit prevents memory issues with large files
        if os.path.getsize(log_path) > 10 * 1024 * 1024:  # 10MB = 10 * 1024 * 1024 bytes
            raise ValueError("Log file too large (>10MB)")
        
        try:
            with open(log_path, 'r', encoding='ascii') as f:
                for line in f:
                    # Parse each line into port and protocol
                    result = self._parse_line(line)
                    
                    if result:
                        port, proto = result
                        
                        # Create composite key for traffic counting
                        traffic_key = f"{port},{proto}"
                        
                        # Increment traffic counter using get() with default to handle new entries
                        self.traffic_count[traffic_key] = self.traffic_count.get(traffic_key, 0) + 1
                        
                        # Look up tag using composite key
                        lookup_key = (port, proto)
                        # Default to "Untagged" for unknown combinations
                        tag = self.lookup_dict.get(lookup_key, "Untagged")
                        
                        # Update tag statistics
                        self.tag_count[tag] = self.tag_count.get(tag, 0) + 1
                        
        except UnicodeDecodeError:
            # Fail if non-ASCII characters are encountered
            raise ValueError("Log file must be ASCII text")
    
    def write_report(self, output_path):
        try:
            # Write in ASCII to ensure universal compatibility
            with open(output_path, 'w', encoding='ascii') as f:
                # Write tag statistics section
                f.write("Tag Counts:\n")
                f.write("Tag,Count\n")
                # Sort for consistent output
                for tag, count in sorted(self.tag_count.items()):
                    f.write(f"{tag},{count}\n")
                
                # Write traffic statistics section
                f.write("\nPort/Protocol Combination Counts:\n")
                f.write("Port,Protocol,Count\n")
                # Sort for consistent output
                for traffic, count in sorted(self.traffic_count.items()):
                    f.write(f"{traffic},{count}\n")
                    
        except UnicodeEncodeError:
            # Ensure output maintains ASCII encoding
            raise ValueError("Cannot write non-ASCII characters")

def main():
    # Validate command line arguments
    if len(sys.argv) != 4:
        print("Usage: python flow_parser.py <log_file> <lookup_file> <output_file>")
        sys.exit(1)
    
    try:
        # Extract file paths from command line arguments
        log_file = sys.argv[1]
        lookup_file = sys.argv[2]
        output_file = sys.argv[3]
        
        # Validate file sizes before processing
        # 10MB limit for log files prevents memory exhaustion
        if os.path.getsize(log_file) > 10 * 1024 * 1024:  # 10MB
            raise ValueError("Flow log file too large")
        # 1MB limit for lookup files ensures reasonable memory usage
        if os.path.getsize(lookup_file) > 1 * 1024 * 1024:  # 1MB
            raise ValueError("Lookup file too large")
        
        # Create parser instance and process files
        parser = FlowParser(lookup_file)
        parser.process_logs(log_file)
        parser.write_report(output_file)
        
    except Exception as e:
        # Catch all exceptions for graceful error handling
        print(f"Error: {str(e)}")
        sys.exit(1)

# Standard Python idiom to run main() when script is run directly
if __name__ == "__main__":
    main()