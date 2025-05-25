# TCAMImageCompression
Goal: Use the powerful parallel content matching capability of TCAM to search for similarity within an image to allow for efficient image compression
Dependency: numpy, PIL

# Parts
+ TCAM_encoder.py: Take image blocks as input and TCAM entries as output.
+ TCAM_simulator.py: Store list of TCAM entries memory, and respond to queries and output match
+ main.py: Break image into blocks, call TCAM_encoder to encode them, store them in TCAM_simulator and call TCAM_simulator to find match

# Usage
Run main.py with image to compress
