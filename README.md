# TCAMImageCompression
Goal: Use the powerful parallel content matching capability of TCAM to search for similarity within an image to allow for efficient image compression
Dependency: numpy, PIL

# Parts
+ TCAM_encoder.py: Take image blocks as input and TCAM entries as output.
+ TCAM_simulator.py: Store list of TCAM entries memory, and respond to queries and output match
+ sim.py: Ideal RMT simulator, for fessibility estimation
+ point_encoder.py: Encode a point
+ interval_encoder.py: Encode an interval around a point
+ main.ipynb: Break image into blocks, call TCAM_encoder to encode them, store them in TCAM_simulator and call TCAM_simulator to find match

# Usage
Put the image in the directory and run main.ipynb with filename of the image.
