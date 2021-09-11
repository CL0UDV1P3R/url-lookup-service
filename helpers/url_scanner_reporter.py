#!/usr/bin/python
import re
import pandas as pd
# import validators # uncomment if this library is used for URL validation


def analyze_url(url: str) -> str:
    """
    URL validator regex
    """
    http_regex = r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"

    url_parse = re.search(http_regex, url)

    result = ""
    if url_parse:
        result = f"Valid URL. {check_for_malware(url)}"
    else:
        result = "Invalid URL. Enter valid URL such as: http://www.example.com"

    # In case one wants to use a library to validate URLs
    """
    if validators.url(url):
        result = f"Valid URL. {check_for_malware(url)}"
    else:
        result = "Invalid URL. Enter valid URL such as: http://www.example.com"
    """

    return f"You entered {url}. {result}"


def check_for_malware(url: str) -> str:
    """
    Checks the csv file which acts as a database in this example for
    any URLs which have been identified as malware in the past and thus
    logged in this file.
    """

    malware_data = pd.read_csv(
        "db/malware_urls.csv"
    )

    malware_data["date_modified"] = pd.to_datetime(malware_data.date_modified)

    is_malware_data = malware_data.loc[malware_data["is_malware"] == "yes"]
    mw_filtered_data = is_malware_data.loc[
        is_malware_data.groupby("url").date_modified.idxmax()
    ]

    is_not_malware_data = malware_data.loc[malware_data["is_malware"] == "no"]
    not_mw_filtered_data = is_not_malware_data.loc[
        is_not_malware_data.groupby("url").date_modified.idxmax()
    ]

    if mw_filtered_data["url"].str.contains(fr"^.*{url}.*$", regex=True).any():
        return f"This URL is identified to contain malware!"
    elif not_mw_filtered_data["url"].str.contains(fr"^.*{url}.*$", regex=True).any():
        return "This URL has been identified to be safe!"
    else:
        return "No data found about this URL in the database!"
