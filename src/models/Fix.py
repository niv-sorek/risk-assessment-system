import pickle
from datetime import datetime


class Fix:
    def __init__(self, name, value):
        self.value = value
        if self.value is None:
            value = 0
        self.name = name

    def __str__(self):
        s = self.name
        if self.name == "Patch":
            s = s + ' (' + datetime.fromtimestamp(int(self.value)).strftime('%Y-%m-%d') + ')'
        else:
            s = s + ' (' + str(self.value) + ')'
        return s

    def reprJSON(self):
        return dict(value=self.value,
                    name=self.name,
                    )
