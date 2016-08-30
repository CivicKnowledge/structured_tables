import unittest


class MyTestCase(unittest.TestCase):


    def test_records(self):

        from os.path import dirname, join
        from structured_tables import TermParser, RecordGenerator, convert
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:
            r = csv.reader(f)
            tp = TermParser(r)

            rg = RecordGenerator(tp)

            rg.run()

            rg.dump()

            print rg._root

            import json

            print json.dumps(convert(rg._root), indent = 4)

    def test_json(self):
        from os.path import dirname, join
        from structured_tables import TermParser, dump_records, generate_records, convert_to_dict
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:

            root = generate_records(TermParser(csv.reader(f)))

            dump_records(root)

            print json.dumps(convert_to_dict(root), indent=4)

    def test_includes(self):
        from os.path import dirname, join
        from structured_tables import TermParser, dump_records, generate_records, convert_to_dict
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'include1.csv')

        with open(fn) as f:
            root = generate_records(TermParser(csv.reader(f), dirname(fn)))

            dump_records(root)

            print json.dumps(convert_to_dict(root), indent=4)


if __name__ == '__main__':
    unittest.main()
