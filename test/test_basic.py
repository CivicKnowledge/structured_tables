import unittest


class MyTestCase(unittest.TestCase):

    def test_terms(self):
        from os.path import dirname, join
        from structured_tables import TermParser, DictAssembler
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:
            r = csv.reader(f)
            for t in TermParser(r):
                print t

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

    def test_datapackage(self):
        from os.path import dirname, join
        from structured_tables import TermParser, RecordGenerator, convert
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'datapackage.csv')

        with open(fn) as f:

            rg = RecordGenerator(TermParser(csv.reader(f)))

            rg.run()

            rg.dump()

            print json.dumps(convert(rg._root), indent=4)



if __name__ == '__main__':
    unittest.main()
