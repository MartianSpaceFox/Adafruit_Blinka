"""
Support for getting the URL from the BLINKA_FT232H
and BLINKA_FT2232H_{} environment variables.
"""

import os


def get_ft232h_url():
    """
    Return the FTDI url to use. If BLINKA_FT232H starts with ftdi:, returns
    that. Otherwise, returns a default value.
    """

    url = os.environ.get("BLINKA_FT232H", "1")

    return url if url.startswith("ftdi:") else "ftdi://ftdi:ft232h/1"


def get_ft2232h_url(interface_id):
    """
    Return the FTDI url to use. If BLINKA_FT2232H_{} starts with ftdi:, returns
    that. Otherwise, returns a default value.
    """

    url = os.environ.get(f"BLINKA_FT2232H_{interface_id}", "1")

    if url.startswith("ftdi:"):
        return url

    return f"ftdi://ftdi:ft2232h/{interface_id + 1}"
