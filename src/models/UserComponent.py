import json

import flask


class UserComponent:
    def __init__(self, component, update):
        self.component = component
        self.update = update

    def get_risk_level(self):
        if len(self.relevant_vulnerabilities()) > 0:
            return max(vul.vulnerability_level for vul in self.relevant_vulnerabilities())
        return 0

    def relevant_vulnerabilities(self):
        vuls = []
        for v in self.component.vulnerabilities:
            if (v.fix.name == 'Patch' and v.fix.value > self.update) or v.fix.name == 'Update':
                vuls.append(v)
        return vuls

    def __str__(self) -> str:
        return '{0} last updated: {1}'.format(str(self.component), self.update)

    def reprJSON(self):
        return dict(component=self.component, update=self.update,
                    relevant_vulnerabilities=self.relevant_vulnerabilities(), level=self.get_risk_level())

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.component == other.component and self.update == other.update
