#!/usr/bin/python3
# coding: utf-8

import sys
from utils.http_utils import get_first_request, post_second_request
from utils.data_utils import extract_cookies, create_csv


# Declare global variables.
SIES_URL = "https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml"


if __name__ == "__main__":
    # Check if the required arguments have been provided, and indicate the use of the script.
    if len(sys.argv) != 3:
        print("\n[!] Uso: python3 " + sys.argv[0] + " <JSESSIONID> <RENDERMAP.TOKEN>\n")
        sys.exit(1)

    JSESSIONID = sys.argv[1]
    RENDERMAP = sys.argv[2]

    # Script information.
    print(
        "[i] autoUniCalendar, a script which converts the Uniovi calendar into Google and Microsoft calendars."
    )
    print(
        "[i] Designed and programmed by Daniel López Gala from the University of Oviedo."
    )
    print("[i] Visit Bimo99B9.github.io for more content.\n")

    first_request = get_first_request(SIES_URL, JSESSIONID, RENDERMAP)
    cookies = extract_cookies(first_request)
    post_second_request(
        SIES_URL,
        JSESSIONID,
        RENDERMAP,
        "true",
        cookies[0],
        cookies[1],
        "1662444000000",
        "1683612000000",
        cookies[2],
    )
    create_csv("raw.txt")
