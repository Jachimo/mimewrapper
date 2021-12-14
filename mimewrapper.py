#!/usr/bin/env python3
"""Wrap an arbitrary binary file into a MIME document (.eml file) using metadata from a sidecar file for headers"""
import logging
import sys
import os
import email.mime
import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description='Wrap a file in a MIME document using specified metadata.')
    parser.add_argument('input', type=str, help='Specify input file to wrap into MIME')
    parser.add_argument('-s', '--sidecar', type=str, help='Specify metadata sidecar file (default: input.headers')
    parser.add_argument('-o', '--output', type=str, nargs='?', help='Specify output file (default: input.eml')
    parser.add_argument('--debug', help='Enable debug mode (very verbose)', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not args.output:
        args.output = os.path.splitext(args.input) + '.eml'  # default output filename

    if not args.sidecar:
        if os.path.isfile(os.path.splitext(args.input)[0] + '.headers'):
            args.sidecar = os.path.splitext(args.input)[0] + '.headers'
        elif os.path.isfile(args.input + '.headers'):
            args.sidecar = args.input + '.headers'
        else:
            print('No sidecar file found, interactive mode not implemented.')
            return 1

    headerlist = parse_sidecar_file(args.sidecar)

    msg = email.message.EmailMessage
    for h in headerlist:
        msg.add_header(h[0], h[1])  # set headers on output message
    with open(args.input, 'rb') as inputf:
        msg.add_attachment(inputf)
    with open(args.output, 'wb') as outputf:
        outputf.write(msg.as_bytes())
    return 0


def parse_sidecar_file(sidecar: str) -> list:
    with open(sidecar, 'r') as sidecarf:
        lines = sidecarf.read()
    headerlist = []
    for l in lines:
        if l[0] == '#':  # allow comments by placing # in 1st column
            continue
        elif l[:5] == 'Date:':
            # TODO special handling of date (parse and convert to RFC format)
        elif (': ' in l) or (':\t' in l):
            header = l.split(':', 1)[0].strip()
            value = l.split(':', 1)[1].strip()
            headerlist.append(tuple((header, value)))  # TODO are double () really needed?
    return headerlist


if __name__ == "__main__":
    sys.exit(main())
