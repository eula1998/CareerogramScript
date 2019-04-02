class DBParser:
    def __init__(self, filename):
        self.filename = filename
        self.tags = {}

    def addToDict(self, s, dict):
        if s not in dict:
            dict[s] = 0
        dict[s] = dict[s] + 1

    def splitTags(self, s, change):
        s = s.lower()
        s = "".join(list(map(change, s)))
        s = s.split('|')
        s = [str.lstrip().rstrip() for str in s]
        return s

    def parseTags(self, t, change, translate):
        t = self.splitTags(t, change)
        for i in range(len(t)):
            t[i] = t[i].replace("-", " ")
            t[i] = translate(t[i])
            self.addToDict(t[i], self.tags)
        return t
