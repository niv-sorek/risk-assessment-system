from src import utils


class Component:
    def __init__(self, vendor, product, version):
        self.product = product
        self.version = version
        self.vendor = vendor
        self.vulnerabilities = self.get_vulnerabilities()

    #  self.component_level = max(venerability.venerability_level for venerability in self.vulnerabilities)

    def get_vulnerabilities(self):
        # self.vulnerabilities = utils.get_vulnerabilities(self.vendor, self.product, self.version)
        print(str(v) for v in self.vulnerabilities)
        return utils.get_component_vulnerabilities(self)

    def __str__(self):
        return "Product: {0}".format(self.product)
