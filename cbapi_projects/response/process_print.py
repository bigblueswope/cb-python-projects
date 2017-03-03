#!/usr/bin/env python
#query = cb.select(Process).where("sensor_id:22122").and_("process_name:cmd.exe").and_(r"cmdline:&&")

import sys
from cbapi.response.models import Process, Binary
from cbapi.example_helpers import build_cli_parser, get_cb_response_object
from cbapi.errors import ObjectNotFoundError


def main():
    parser = build_cli_parser("Print processes")

    args = parser.parse_args()
    args.profile="fs"
    cb = get_cb_response_object(args)

    for proc in cb.select(Process).where("sensor_id:22122 process_name:cmd.exe cmdline:&&"):
        print proc

if __name__ == "__main__":
    sys.exit(main())
