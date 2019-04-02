translation = {


}

# categories
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
