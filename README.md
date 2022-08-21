# CDLI Publication File Upload Processor

This is a program that processes CDLI publication files and uploads them to the CDLI database. It scans for potential entities that are mentioned in the publication files and returns them as a pandas dataframe.

OCR is not supported at this time. The program will only process textual PDF files.

## Requirements
    See the ``requirements.txt``. Also make sure the CDLI docker containers are running.
    
## Usage

    python3 process_file.py -n "path/to/file.pdf"