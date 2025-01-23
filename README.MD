# Illumino Tech Assessment 

## Requirements
    1. Input file as well as the file containing tag mappings 
        are plain text (ascii) files.
    2. The flow log file size can be up to 10 MB. 
    3. The lookup file can have up to 10000 mappings. 
    4. The tags can map to more than one port, protocol combinations.  
        for e.g. sv_P1 and sv_P2 in the sample above. 
    5. The matches should be case insensitive.

## Assumptions
    1. The machine is using python 3.9 to run the script.
    2. The data files are well formatted csv files.
    3. This script only conforms to the default format
        of flow logs (version 2) and does not support custom 
        formatting. For more information about flow logs
        refer to link [1]

[1] [AWS Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html) 


## How to execute script?
    1. Make sure you are executing in the script directory -
        type `cd {base_path}/main/`.
    2. Run the script - type `python3 main.py`.
    3. The two output files with the counts will be in the data_out folder.
    
    
Note: No need to install requirements.txt since no
        external modules where used.

## Tests
    No formal testing was done. However using a small data
    set and manually verifying the output at every step was used 
    as a preliminary show of correctness.

## Space and Time Complexity
    The program runs in O(n) time complexity
    and O(n) space complexity where n is the size
    of the largest file.


## All Links
[1] [AWS Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html) 
