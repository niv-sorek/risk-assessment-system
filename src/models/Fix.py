from datetime import datetime


class Fix:
    def __init__(self, name, value):
        self.value = value
        self.name = name

    def __str__(self):
        s = self.name
        if self.name == "Patch":
            s = s + ' (' + datetime.fromtimestamp(int(self.value)).strftime('%Y-%m-%d') +')'
        else:
            s = s + ' (' + self.value+')'
        return s
