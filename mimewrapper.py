#!/usr/bin/env python3
"""Wrap an arbitrary binary file into a MIME document (.eml file) using metadata from a sidecar file for headers"""

import sys
import os
import email.mime

def main() -> int:
    input = sys.argv[1]
    output = os.path.splitext(sys.argv[1])[0] + '.eml'
    if os.path.isfile(os.path.splitext(sys.argv[1])[0] + '.headers'):
        sidecar = os.path.splitext(sys.argv[1])[0] + '.headers'
        headerlist = parse_sidecar_file(sidecar)
    elif os.path.isfile(sys.argv[1] + '.headers'):
        sidecar = sys.argv[1] + '.headers'
        headerlist = parse_sidecar_file(sidecar)
    else:
        print('No sidecar file found, interactive mode not implemented.')
        return 1
    msg = email.message.EmailMessage
    for h in headerlist:
        msg.add_header(h[0], h[1])  # set headers on output message
    msg.add_attachment(input)  # TODO may need to open and pass file object?
    with open(output, 'wb') as of:
        of.write(msg.as_bytes())
    return 0


def parse_sidecar_file(sidecar: str) -> list:
    with open(sidecar, 'r') as sidecarf:
        lines = sidecarf.read()
    headerlist = []
    for l in lines:
        if l[0] == '#':  # allow comments
            continue
        if (': ' in l) or (':\t' in l):
            header = l.split(':', 1)[0].strip()
            value = l.split(':', 1)[1].strip()
            headerlist.append( tuple((header, value)) )
    return headerlist


if __name__ == "__main__":
    sys.exit(main())
