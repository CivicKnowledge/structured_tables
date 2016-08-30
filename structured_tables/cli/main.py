# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

import sys

def main(sys_args):
    import argparse
    from structured_tables import __meta__
    from structured_tables import TermParser, dump_records, generate_records, convert_to_dict
    import csv

    parser = argparse.ArgumentParser(
        prog='struct_tab',
        description='Simple Structured Table format parser. '.format(__meta__.__version__))

    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('-t', '--terms', default=False, action='store_true',
                        help='Parse a file and print out the stream of terms')
    g.add_argument('-r', '--records', default=False, action='store_true',
                        help='Parse a file and print out a strean of reacords')
    g.add_argument('-j', '--json', default=False, action='store_true',
                        help='Parse a file and print out a JSON representation')
    g.add_argument('-y', '--yaml', default=False, action='store_true',
                        help='Parse a file and print out a YAML representation')


    parser.add_argument('file', type=file,  help='Path to a CSV file with STF data.')


    args = parser.parse_args(sys_args[1:])



    csv_reader = csv.reader(args.file)

    term_gen = TermParser(csv_reader)

    if args.terms:
        for t in term_gen:
            print t

        sys.exit(0)

    root = generate_records(term_gen)

    if args.records:
        dump_records(root)

    dicts = convert_to_dict(root)

    if args.json:
        import json
        print json.dumps(dicts, indent=4)

    if args.yaml:
        import yaml
        print yaml.dumps(dicts, indent=4)