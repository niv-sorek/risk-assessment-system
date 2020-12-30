class UserComponent:
    def __init__(self, component, update):
        self.component = component
        self.update = update

    def get_risk_level(self):
        return max(vul.vulnerability_level for vul in self.relevant_vulnerabilities())

    def relevant_vulnerabilities(self):
        vuls = []
        for v in self.component.vulnerabilities:
            if (v.fix.name == 'Patch' and v.fix.value > self.update) or v.fix.name == 'Update':
                vuls.append(v)
        return vuls

    def __str__(self) -> str:
        return '{0} last updated: {1}'.format(str(self.component), self.update)

    def __repr__(self):
        return 'Component(%s, Update: %s)\n' % (self.component, self.update)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.component == other.component and self.update == other.update
