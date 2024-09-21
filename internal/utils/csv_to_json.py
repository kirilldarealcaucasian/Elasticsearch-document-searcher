import csv
import json
import uuid

from common.logger import logger


def convert_from_csv_to_json(csv_file_path: str, output_file_path: str):
    try:
        with open(csv_file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                row["text"] = row["text"].replace("\n", "")
                row["id"] = str(uuid.uuid4())  # adds id to each json
                data.append(row)
    except OSError as e:
        logger.warning(
            "failed to open csv file",
            exc_info=True,
            extra={"csv_file_path": csv_file_path}
        )
        raise e

    try:
        with open(output_file_path, 'w',  encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=6)
    except OSError as e:
        logger.error(
            "failed to write to json file",
            exc_info=True,
            extra={"output_filename_path": output_file_path}
        )
        raise e