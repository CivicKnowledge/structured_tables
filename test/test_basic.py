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

    def test_terms(self):
        from os.path import dirname, join
        from structured_tables import TermGenerator
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:
            terms = list(TermParser(csv.reader(f), path=fn))

            self.assertEqual(270, len(terms))

            #for i, t in enumerate(terms):
            #    print i, t

            self.assertEqual('conformsto', terms[0].record_term)
            self.assertEqual('metadata.csv', terms[0].value)

            self.assertEqual('metadata.csv', terms[51].file_name)
            self.assertEqual('<no_term>', terms[51].parent_term)
            self.assertEqual('declareterm', terms[51].record_term)
            self.assertEqual('Column.Description', terms[51].value)

            self.assertEqual('example1.csv', terms[108].file_name)
            self.assertEqual('column', terms[108].parent_term)
            self.assertEqual('0', terms[108].record_term)
            self.assertEqual('int', terms[108].value)

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

        print json.dumps(term_interp.declare_dict, indent=4)


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
                print t

            root = link_terms(term_gen)

            flt = flatten_dict(convert_to_dict(root))

            #for k, v in sorted(flt.items()):
            #    print k, v


    def test_records(self):

        from os.path import dirname, join
        from structured_tables import TermGenerator
        import csv
        import json

        fn = join(dirname(__file__), 'data', 'example1.csv')

        with open(fn) as f:
            r = csv.reader(f)
            tp = TermGenerator(r)

            rg = RecordGenerator(tp)

            rg.run()

            rg.dump()

            print rg._root

            import json

            print json.dumps(convert(rg._root), indent = 4)

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
                print k, v

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
                print t.valid, t

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
