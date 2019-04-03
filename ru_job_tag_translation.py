translation = {
    "b.s." : "bachelor",
    "b.s" : "bachelor",
    "bs"    : "bachelor",
    "m.s."  : "masters",
    "ms"    : "masters",
    "bachelor's" : "bachelor",
    "bachelors" : "bachelor",
}

categories = {

}

def translate(s):
    if s in translation:
        return translation[s]
    return s

def categorize(s):
    if s in categories:
        return categories[s]
    return None
