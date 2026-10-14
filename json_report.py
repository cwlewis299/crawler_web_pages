import json
from crawl import PageData

def write_json_report(page_data: dict[str, PageData], filename="report.json"):
    """
    Writes the page data to a JSON file.

    Args:
        page_data (dict[str, PageData]): A dictionary containing the page data.
        filename (str): The name of the JSON file to write to. Defaults to "report.json".
    """
    # Convert page_data to a list sorted by URL
    sorted_data = sorted(page_data.values(), key=lambda p: p["url"])

    # Write the sorted data to a JSON file
    with open(filename, "w") as json_file:
        json.dump(sorted_data, json_file, indent=2)