from Venerability import Venerability

class Component:
    def __init__(self, name, vendor):
        self.name = name
        self.vendor = vendor
        self.vulnerabilities = []
        self.component_level= 0

    # def create_vulnerabilities_list(self):
    #     #pull vulnerabilities
    #     self.vulnerabilities =

    def calculate_component_level(self):
        self.component_level = max(venerability.venerability_level for venerability in self.vulnerabilities)

    def get_component_level(self):
        self.create_vulnerabilities_list()
        self.calculate_component_level()
        return self.component_level
