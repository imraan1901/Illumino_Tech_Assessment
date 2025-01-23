import sys
import os
import socket
import csv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROTOCOL = "IPPROTO"

LOOKUP_TABLE_IN_FILE = "data_in/lookup_table.csv"
FLOW_LOG_IN_FILE = "data_in/flow_log.csv"

DST_PORT_PROTOCOL_COUNT_OUT_FILE = "data_out/port_protocol_out_file.csv"
TAG_COUNT_OUT_FILE = "data_out/tag_count_out_file.csv"

DST_PORT_PROTOCOL_COUNT_OUT_FILE_HEADER = ["Port", "Protocol", "Count"]
TAG_COUNT_OUT_FILE_HEADER = ["Tag", "Count"]

if __name__ == "__main__":
    # Could also check if all files are valid before running program.
    base_path = os.getcwd()
    parent = os.path.dirname(base_path)

    protocol_num_to_name_mapping = {}
    dst_port_protocol_count = {}

    dst_port_protocol_to_tag_mapping = {}
    tag_count = {}

    # Map the number of the protocol to the name
    # e.x. - 6: 'tcp'
    for name, num in vars(socket).items():
        if name.startswith(PROTOCOL):
            cleaned_name = name.replace(f"{PROTOCOL}_", "").lower()
            str_num = str(num)
            protocol_num_to_name_mapping[str_num] = cleaned_name

    # Ingest the lookup table
    try:
        with (open(os.path.join(parent, LOOKUP_TABLE_IN_FILE), 'r') as file):
            reader = csv.reader(file, delimiter=',')
            # Watch out for header count
            line_counter = 0
            for row in reader:
                try:
                    dst_port = row[0]
                    protocol = row[1]
                    tag = row[2]
                    key = f"{dst_port}-{protocol}"
                    dst_port_protocol_to_tag_mapping[key] = tag
                    line_counter += 1
                except IndexError:
                    logger.warning(f"WARNING: {LOOKUP_TABLE_IN_FILE} has malformed data")
            logger.info(f"INFO: {LOOKUP_TABLE_IN_FILE} has successfully been read with {line_counter} lines of data")

    except FileNotFoundError:
        logger.error(f"ERROR: {LOOKUP_TABLE_IN_FILE} not found")
        sys.exit(1)

    # Ingest the flow log file and update counts O(n) runtime
    try:
        with open(os.path.join(parent, FLOW_LOG_IN_FILE), 'r') as file:
            reader = csv.reader(file, delimiter=',')
            # Watch out for header count
            line_counter = 0
            for row in reader:
                try:
                    dst_port = row[6]
                    protocol_name = protocol_num_to_name_mapping[row[7]]
                    key = f"{dst_port}-{protocol_name}"
                    # Count the port-protocol pairs in the flow log
                    if key not in dst_port_protocol_count:
                        dst_port_protocol_count[key] = 1
                    else:
                        dst_port_protocol_count[key] += 1

                    # Count the tags
                    if key in dst_port_protocol_to_tag_mapping:
                        tag_key = dst_port_protocol_to_tag_mapping[key]
                        if tag_key not in tag_count:
                            tag_count[tag_key] = 1
                        else:
                            tag_count[tag_key] += 1
                    # Count the untagged
                    else:
                        untagged_key = "untagged"
                        if untagged_key not in tag_count:
                            tag_count[untagged_key] = 1
                        else:
                            tag_count[untagged_key] += 1

                    line_counter += 1
                except IndexError:
                    logger.warning(f"WARNING: {FLOW_LOG_IN_FILE} has malformed data")
            logger.info(f"INFO: {FLOW_LOG_IN_FILE} has successfully been read with {line_counter} lines of data")

    except FileNotFoundError:
        logger.error(f"ERROR: {FLOW_LOG_IN_FILE} not found")
        sys.exit(1)

    # Save the port-protocol counts to a file
    with open(os.path.join(parent, DST_PORT_PROTOCOL_COUNT_OUT_FILE), 'w+') as file:
        writer = csv.writer(file)
        writer.writerow(DST_PORT_PROTOCOL_COUNT_OUT_FILE_HEADER)
        line_counter = 0
        for key, count in dst_port_protocol_count.items():
            dst_port, protocol = key.split("-")
            to_write = [dst_port, protocol, count]
            writer.writerow(to_write)
            line_counter += 1
        logger.info(f"INFO: {DST_PORT_PROTOCOL_COUNT_OUT_FILE} "
                    f"has successfully been written to with {line_counter} lines of data")

    # Save the tag counts to a file
    with open(os.path.join(parent, TAG_COUNT_OUT_FILE), 'w+') as file:
        writer = csv.writer(file)
        writer.writerow(TAG_COUNT_OUT_FILE_HEADER)
        line_counter = 0
        for tag, count in tag_count.items():
            to_write = [tag, count]
            writer.writerow(to_write)
            line_counter += 1
        logger.info(f"INFO: {TAG_COUNT_OUT_FILE} "
                    f"has successfully been written to with {line_counter} lines of data")

