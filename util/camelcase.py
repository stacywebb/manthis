import re
from string import capitalize #@UnresolvedImport

def camelcase(value):
    value = str(value)
    return "".join([capitalize(w) for w in re.split(re.compile("[\W_]*"), value)])