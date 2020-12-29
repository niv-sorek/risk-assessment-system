class UserComponent:
    def __init__(self, component, update):
        self.component = component
        self.update = update
        self.level = self._calc_component_level()

    def _calc_component_level(self):
        return max(vul.vulnerability_level for vul in self.relevant_vulnerabilities())

    def relevant_vulnerabilities(self):
        vuls = []
        for v in self.component.vulnerabilities:
            if (v.fix.name == 'Patch' and v.fix.value > self.update) or v.fix.name == 'Update':
                vuls.append(v)
        return vuls
