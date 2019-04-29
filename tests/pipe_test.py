import ft, datetime
from pprint import pprint

data = ft.load_csv(open("tests/mid_e_verb_morph.csv"))

print "ft.summary(data): "
pprint(ft.summary(data))
print "*"*50
dex = ft.indexBy("suf", data, pipe=lambda s: s[0] if s else s)
pprint(dex)
print "^^^Indexed by first letter of suf^^^"
print "Counts"
pprint(ft.histo(dex))
