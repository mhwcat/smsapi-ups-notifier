from unicodedata import name
from smsapi.client import SmsApiPlClient
from smsapi.exception import SmsApiException
from config import *
import logging
from enum import Enum
from datetime import datetime
import argparse
import sys


class UpsAction(Enum):
    UP = "UP"
    DOWN = "DOWN"


def build_message(ups_action: UpsAction, site_name: str):
    now = datetime.now()
    now_formatted = now.strftime('%Y-%M-%d %H:%M:%S')

    return site_name + ": " + "UPS Power " + ups_action.name + " at " + now_formatted


def main(ups_action: UpsAction, site_name: str):
    client = SmsApiPlClient(access_token=SMSAPI_TOKEN)
    try:
        for number in PHONE_NUMBERS:
            message = build_message(ups_action, site_name)
            client.sms.send(to=number, message=message)

            logging.info("Sent sms to %s with message '%s'", number, message)
    except SmsApiException as e:
        logging.error(e.message, e.code)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Send SMS message via SMSAPI on UPS power change.")
    parser.add_argument("site", type=str, help="Name of site where power changed (e.g. Office)")
    parser.add_argument("state", type=str, choices=["UP", "DOWN"], help="Power state to inform about")
    args = parser.parse_args(sys.argv[1:])

    main(UpsAction(args.state), args.site)