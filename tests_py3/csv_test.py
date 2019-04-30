from pprint import pprint
import ft

print(ft.version,"csv test")

raw_input = open("tests/mid_e_verb_morph.csv")
data = ft.load_csv(raw_input)
pprint(data)
fstream = open("tests/csv_test_0.csv", "w")
ft.dump_csv(data, fstream)

raw_input = open("tests/tough_table.csv")

csv_dialect = ft.dialect_dex["basic"][0]
csv_dialect["cell_delimiter"] = "|"

data = ft.load_csv(raw_input, dialect = csv_dialect)
pprint(data)
fstream = open("tests/csv_test_1.csv", "w")
ft.dump_csv(data, fstream)

