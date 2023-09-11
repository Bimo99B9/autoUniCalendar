#!/usr/bin/python3
# coding: utf-8

import sys
from datetime import datetime
from utils.http_utils import get_first_request, post_second_request
from utils.data_utils import extract_cookies, create_csv


def convert_date_to_milliseconds(date_str):
    """
    Convert a date string in format 'DD/MM/YYYY' to milliseconds since epoch.
    """
    dt_obj = datetime.strptime(date_str, "%d/%m/%Y")
    return int(dt_obj.timestamp() * 1000)


if __name__ == "__main__":
    # Check if the required arguments have been provided, and indicate the use of the script.
    if len(sys.argv) < 2:
        print(
            "\n[!] Uso: python3 "
            + sys.argv[0]
            + " <JSESSIONID> [START_DATE] [END_DATE]\n"
        )
        sys.exit(1)

    JSESSIONID = sys.argv[1]
    START_DATE = sys.argv[2] if len(sys.argv) > 2 else "01/09/2023"
    END_DATE = sys.argv[3] if len(sys.argv) > 3 else "01/07/2024"

    # Convert dates to milliseconds
    START_DATE_MILLIS = convert_date_to_milliseconds(START_DATE)
    END_DATE_MILLIS = convert_date_to_milliseconds(END_DATE)

    # Script information.
    print(
        "[i] autoUniCalendar, a script which converts the Uniovi calendar into Google and Microsoft calendars."
    )
    print(
        "[i] Designed and programmed by Daniel López Gala from the University of Oviedo."
    )
    print("[i] Visit Bimo99B9.github.io for more content.\n")

    first_request = get_first_request(JSESSIONID)
    cookies = extract_cookies(first_request)
    post_second_request(
        JSESSIONID,
        cookies[0],
        cookies[1],
        START_DATE_MILLIS,
        END_DATE_MILLIS,
        cookies[2],
    )
    create_csv("raw.txt")
