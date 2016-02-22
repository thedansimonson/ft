"""
Free Tables: A Conduit for the Magic of Python
    Dan Simonson - 2013

Python data types are awesome. You can do pretty much anything with them.
One particularly useful arrangement is a list of dictionaries, something
I started referring to as a "free table."

This is a library for manipulating free tables.

Conventions:
data: If an argument is called data, a free table is expected there.

datum/point: A dictionary of a free table. 

dex: If an argument is called dex, then it should be a dex--a dictionary
whose values are free tables. These are what are returned by the totally
awesome and ever useful indexBy function.

prop: If an argument is called prop, it's a property. This usually should
be an entry in every datum in data. It isn't always, sometimes intended for
retaining consistency. 

FAQ:
+ Why don't you make an ftable class?
    No. That defeats the whole point of free tables. They're supposed to be
    pliable and easily manipulable using Python syntax. They're a convention,
    not a type. I only see the imposition of a class upon the structure as
    a hinderance.

    If you think I'm wrong, you're welcome to prove me so.

"""
import csv
from pprint import pprint

version = "0.2.3"

########
# Meta #
########
def future(): 
    "A lot of functions are defined as personal notes."
    raise Exception("This is a planned feature, but not yet implemented.")

def validate(data):
    """Ensures data actually is an ftable and not bullshit.

    More tests to come.
    """
    
    #data should be a list
    if list(data) != data:
        raise Exception("data is not a list.")

    #all entries in the list should be dictionaries
    if not all([dict(d) == d for d in data]):
        raise Exception("Non-dictionary in list")

    #all entries in the list should have the same set of keys
    #this is checked in two ways. first--making sure they have the same number
    #of keys.



###########
# indexBy #
###########
indexBy_doc = """
    The sweet baby jesus of the ft library. Many ft functions are built on top
    of indexBy; it's by far the most versatile abstraction in the library.

    Would have been called bin, but that's a keyword.

    Essentially, it creates a dictionary from data where the keys are 
        {d[prop] for d in data}
    e.g. the set of values prop holds. 
    The values of those keys are the data points that had that value. 
    
    Essentially, it bins data, and returns a dictionary of those bins. 

    Args:
        prop = the property being indexed
        data = the data being binned
        pipe = a function that preprocesses 

    Returns:
        dex = a dictionary whose keys are values of prop in data and 
            values are ftables of those datapoints
    """

def indexBy0(prop, data, pipe = lambda x: x):
    "A simple version of index by that ended up performing surprisingly well."
    dex = {}
    s = lambda d: pipe(d[prop]) #the 's' is for sucks!
    for d in data:
        if s(d) in dex: dex[s(d)].append(d)
        else: dex[s(d)] = [d]
    return dex

def indexBy4(prop, data, pipe = lambda x: x):
    """
        Optimization attempt
    """
    s = lambda d: pipe(d[prop]) #the 's' is for sucks!
    
    pvals = list(set([s(e) for e in data]))
    dex = {v: [] for v in pvals}

    for d in data: dex[s(d)].append(d)
    return dex

def indexBy2(prop, data, pipe = lambda x: x):
    """
    a faster attempt at the indexBy algorithm
    
    (it's actually slower)
    """
    dex = {}
    s = lambda d: pipe(d[prop])
    comp = lambda d: dex[s(d)].append(d) if s(d) in dex else \
                    dex.update([(s(d), [d])])
    map(comp,data)
    return dex

def indexBy3(property, table):
    """
    OLD SCHOOL ASS VERSION from ftables.py
     Create a dictionary out of a free table whose index values 
     depend on property. 
      @param property - the property to sort by
      @param table - a free table
      
      @returns - a dictionary, whose keys are possible values of 
                   property and values are free tables
    """
    pvals = list(set([e[property] for e in table]))
    result = dict([(v, []) for v in pvals])
    [result.update([(e[property], result[e[property]]+[e])]) for e in table]
    return result

#select optimized version here
indexBy = indexBy0
indexBy.__doc__ = indexBy_doc 

########################
# Sorting and Indexing #
########################


################
# Manipulation #
################

def tag(data, label, f, args = []):
    """
    For all d in data, d[label] = using(d[args[0]]...)
    """
    for d in data: d[label] = f(*[d[arg] for arg in args])
    return data


def merge(data, differs = "All"):
    """
    Combines multiple data items whose differs are identical.
    Collapses properties which are auxiliary into lists w/ that property
    as a key.
    (Useful for removing duplicates)

    For example:
        crap = [{"a": 5, "b": 6, "c": 3},
                {"a": 6, "b": 6, "c": 3},
                {"a": 8, "b": 4, "c": 3}]
        crap = merge(crap, differs = ["b","c"])
        print crap
        #[{"a": [5,6], "b": 6, "c": 3}
        # {"a": [8],   "b": 4, "c": 3}]

    Args:
        data - data to be merged. 
        differs - keys which are used to differentiate dicts. by default, all 
                  are used, making it remove duplicates by default.
    """
    if differs == "All": 
        differs = list(data[0])
        indiffers = set([])
    else:
        indiffers = list(set(list(data[0])) - set(differs))

    #tag all data with a temporary tuple 
    #based on the differs, each tag is "unique" as the user cares about
    #uniqueness
    temp = "merge_key"
    tupleate = lambda *args: tuple(args)
    data = tag(data, temp, tupleate, differs)

    #where the accumulation happens. 
    dex = indexBy(temp, data)
    accumulator = []
    pprint(dex)

    for key in dex:
        butter = dict(zip(differs, key)) #heheheh
        
        for indiffer in indiffers:
            #accumulate the indistinguishable things
            #(pull the cream off the top)
            cream = [d[indiffer] for d in dex[key]]
            butter[indiffer] = cream

        accumulator.append(butter)
    
    #data should remain untouched, in theory
    for d in data: del d[temp]

    #data is totally replaced with a slightly altered version.
    #creepy, huh?
    return accumulator


###############
# Count Stuff #
###############

def histo(dex):
    "Turns a dex into a histogram."
    return {k: len(dex[k]) for k in dex}


def summary(data):
    "HISTOGRAM EVERYTHING"
    keys = list(data[0])
    return {k: histo(indexBy(k, data)) for k in keys}


#####################
# Hello and Goodbye #
#####################
# These functions turn all kinds of data into free tables and turn free 
# tables into other arrangements of data. 


# File IO

def pickle_load(fstream):
    """
    Is this even necessary?
    """
    raise Exception("Just use pickle.load")

def pickle_dump(fstream):
    """
    Or this.
    """
    raise Exception("Just pickle.dump it you big dumbo")

# CSV HANDING #

dialect_table = [{"dialect": "basic", 
                  "cell_delimiter": ",",
                  "row_delimiter": "\n",
                  "text_delimiter": "\"",
                  "pipe": str},
                {"dialect": "basic_utf-8", 
                  "cell_delimiter": ",",
                  "row_delimiter": "\n",
                  "text_delimiter": "\"",
                  "pipe": lambda v: unicode(v).encode("utf-8")}
                ]

dialect_dex = indexBy("dialect", dialect_table)

def load_csv(fstream, dialect = dialect_dex["basic"][0]):
    """
    Loads the csv from fstream as a free table.
    Doesn't support "\\n" multi-line quotes
    Probably fails if tables are too big -- because it just splits everything.
    Doesn't really do quotes either.

    Honestly, this kinda sucks.

    I swear I wasn't sober or in a good mood.

    I just wanted it working.

    Leave me alone.
    
    Notes: 
        + Takes the first row as a row of keys.
    """
    """
    # old version
    reader = csv.reader(fstream)
    key = reader.next()
    """
    
    rower = dialect["row_delimiter"]
    texter = dialect["text_delimiter"]
    celler = dialect["cell_delimiter"]
    piper = dialect["pipe"]

    def row_reader(row):
        return map(piper, row.split(celler))

    rows = fstream.read().split(rower)
    keys, rows = row_reader(rows[0]), map(row_reader,rows[1:])
    data = [{k: v for k,v in zip(keys, r)} for r in rows if len(r) == len(keys)]
    return data


def dump_csv(data, fstream, keys = [], dialect=dialect_dex["basic"][0]):
    """
    Saves data as csv in fstream.

    I haven't tested this.
    """
    if not keys: keys = sorted(list(data[0]))
    
    celler = dialect["cell_delimiter"]
    rower = dialect["row_delimiter"]
    piper = dialect["pipe"]
    
    rows = [keys]+[[piper(d[k]) for k in keys] for d in data]
    rows = [celler.join(r) for r in rows]
    output = rower.join(rows)

    fstream.write(output)
    return True #why not?

    


def load_json(fstream):
    """
    handy
    """
    future()

def dump_json(data, fstream):
    """
    str(dict) lol
    """
    future()

