import unittest

def term_pairs(root):
    """Take a record root and return a set of singles and pairs of terms, to be used in
     a ConformsTo doc. """

    from structured_tables import  convert_to_dict

    flt = flatten_dict(convert_to_dict(root))

    def is_int(v):
        try:
            int(v)
            return True
        except:
            return False

    s = set()
    for k in flt.keys():
        parts = [x for x in k.split('.') if not is_int(x)]
        for i in range(len(parts)):
            t = parts[i:i + 2]
            if (i == 0 and len(t) == 1) or len(t) == 2:
                s.add(tuple(t))

    return sorted(s);

# From  https://medium.com/@amirziai/flattening-json-objects-in-python-f5343c794b10#.n3bfyujl8
def flatten_dict(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

class MyTestCase(unittest.TestCase):


    def test_web(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, TermInterpreter, CsvPathRowGenerator
        fn = join(dirname(__file__), 'data', 'example1-web.csv')

        with open(fn) as f:
            term_gen = list(TermGenerator(CsvPathRowGenerator(fn)))

            term_interp = TermInterpreter(term_gen)

            print term_interp.as_dict().keys()

            print term_interp.errors_as_dict()

    def test_terms(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, TermInterpreter
        from structured_tables import CsvPathRowGenerator, CsvDataRowGenerator, RowGenerator
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:
            str_data = f.read();

        with open(fn) as f:
            row_data = [row for row in csv.reader(f)]

        for rg_args in ( (CsvPathRowGenerator,fn),
                    (CsvDataRowGenerator,str_data, fn),
                    (RowGenerator,row_data, fn) ):

            with open(fn) as f:

                rg = rg_args[0](*rg_args[1:])

                print rg.__class__.__name__

                terms = list(TermGenerator(rg))

                #for i, t in enumerate(terms):
                #    print i, t

                self.assertEqual(141, len(terms))

                self.assertEqual('declare', terms[0].record_term)
                self.assertEqual('metadata.csv', terms[0].value)

                self.assertTrue(terms[48].file_name.endswith('example1.csv'))
                self.assertEqual('<no_term>', terms[48].parent_term)
                self.assertEqual('column', terms[48].record_term)
                self.assertEqual('geoname', terms[48].value)

                self.assertTrue(terms[100].file_name.endswith('example1.csv'))
                self.assertEqual('<no_term>', terms[100].parent_term)
                self.assertEqual('column', terms[100].record_term)
                self.assertEqual('percent', terms[100].value)

                rg = rg_args[0](*rg_args[1:])

                terms = TermInterpreter(TermGenerator(rg))

                self.assertListEqual(['creator', 'datafile', 'description', 'documentation', 'format', 'homepage',
                                      'identifier', 'note', 'obsoletes', 'spatial', 'spatialgrain', 'table',
                                      'time', 'title', 'version', 'wrangler'],
                                     sorted(terms.as_dict().keys()) )


    def test_declarations(this):
        from os.path import dirname, join
        from structured_tables import RowGenerator, TermGenerator, TermInterpreter
        from structured_tables import link_terms, convert_to_dict, DeclareTermInterpreter
        from structured_tables import NO_TERM, Term
        import csv, json

        fn = join(dirname(__file__), 'data', 'metadata.csv')

        term_gen = TermGenerator(RowGenerator(fn))

        term_interp = DeclareTermInterpreter(term_gen, False)

        d = term_interp.as_dict()
        term_interp.import_declare_doc(d)

        print(json.dumps(term_interp.declare_dict, indent=4))

    def test_interpretation(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, TermInterpreter, link_terms, convert_to_dict
        import csv
        import time

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:

            term_gen = list(TermGenerator(csv.reader(f), path=fn))

            term_interp = list(TermInterpreter(term_gen, False))

            files = set(t.file_name for t in term_interp)

            for fn in files:
                rows = max( t.row for t in term_interp if t.file_name == fn)
                cols = max( max(t.col, len(t.args)+2) for t in term_interp if t.file_name == fn)

                g = [[None]*cols]*(rows +2)

                for t in term_interp:
                    g[t.row][t.col-1] = t.value

            for t in term_interp:
                print(t)

            root = link_terms(term_gen)

            flt = flatten_dict(convert_to_dict(root))

            #for k, v in sorted(flt.items()):
            #    print k, v

    def test_errors(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, TermInterpreter, CsvPathRowGenerator
        fn = join(dirname(__file__), 'data', 'errors.csv')

        with open(fn) as f:

            term_gen = list(TermGenerator(CsvPathRowGenerator(fn)))

            term_interp = TermInterpreter(term_gen)

            print term_interp.as_dict().keys()

            self.assertEquals(1, term_interp.errors[0].term.row)


            print term_interp.errors_as_dict()




    def test_json(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, TermInterpreter, generate_records, convert_to_dict
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:

            tp = TermParser(csv.reader(f), path=fn)
            ti = TermInterpreter(tp)
            root = generate_records(ti)
            flt = flatten_dict(convert_to_dict(root))

            for k, v in flt.items():
                print( k, v)

            self.assertEquals(flt['creator.email'], 'HCIOHE@cdph.ca.gov')
            self.assertEquals(flt['creator.name'],  'Office of Health Equity')
            self.assertEquals(flt['datafile.0.url'], 'http://example.com/example1.csv')
            self.assertEquals(flt['documentation.1.title'], 'Data Bundles Packaging Specification')

            self.assertEquals(flt['table.column.14.name'], 'numerator')
            self.assertEquals(flt['table.column.9.valuetype'], 'label for region_code')

    def test_validate(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, generate_records, convert_to_dict
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:
            tp = TermParser(csv.reader(f), path=fn)

            for t in tp:
                pass
                print(t.valid, t)

    def test_includes(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator, generate_records, convert_to_dict
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'include1.csv')

        with open(fn) as f:
            root = generate_records(TermParser(csv.reader(f), path=fn))

            flt = flatten_dict(convert_to_dict(root))

            self.assertEquals(flt['note.0'], 'Include File 1')
            self.assertEquals(flt['note.1'], 'Include File 2')
            self.assertEquals(flt['note.2'], 'Include File 3')


if __name__ == '__main__':
    unittest.main()
