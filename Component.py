

class Component:
    def __init__(self, vulnerabilities):
        self.vulnerabilities = vulnerabilities
        self.component_level = max(venerability.venerability_level for venerability in self.vulnerabilities)

    def get_component_level(self):
        return self.component_level
