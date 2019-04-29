import ft, datetime
from pprint import pprint
from copy import deepcopy

# load_csv test

data = ft.load_csv(open("tests/mid_e_verb_morph.csv"))

# PIPE test
print "ft.summary(data): "
pprint(ft.summary(data))
print "*"*50
dex = ft.indexBy("suf", data, pipe=lambda s: s[0] if s else s)
pprint(dex)
print "^^^Indexed by first letter of suf^^^"
print "Counts"
pprint(ft.histo(dex))


# Singleton test
foo = ft.singletons("i", range(1,10))
foodex = ft.indexBy("i", foo)
print "Singletons"
pprint(foodex)

# Merge test
premerged_data = deepcopy(data)
merged_data = ft.merge(data, differs=["tns","prs","num","mud"])
print
print "Merge result:"
pprint(merged_data)
print
print "Compare to assert non-destructiveness of merge:"
print "NO FORMAL TEST FOR THIS YET..."
pprint(zip(premerged_data,merged_data))
print
data = premerged_data

# Flatdex Test
flat = ft.flatdex(premerged_data, "suf")
print "Flat Test"
pprint(flat)
print

# Multidex Test
multitest = [{"foo": [1,2,3]}, 
             {"foo": [2,3,4]}]
multidex = ft.multidex(multitest, "foo")
pprint(multidex)
