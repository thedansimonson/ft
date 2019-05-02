import ft, datetime
from pprint import pprint 

data = ft.load_csv(open("tests/mid_e_verb_morph.csv"))

print("ft.summary(data): ")
pprint(ft.summary(data))


print("Speed tests...")
data = data * 50
tests = {ft.indexBy: []}
for i in range(1,10000):
    for f in tests: 
        start = datetime.datetime.now()
        datadex = f("mud", data)
        stop = datetime.datetime.now()
        tests[f].append((stop-start).total_seconds())

for f in tests:
    print(f, float(sum(tests[f]))/len(tests[f]))

    
