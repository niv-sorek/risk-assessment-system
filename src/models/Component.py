from src import utils


class Component:
    def __init__(self, id, vendor, product, version="", last_updated="", vulnerabilities=[]):
        self.id = id
        self.last_updated = last_updated
        self.vulnerabilities = vulnerabilities
        self.product = product
        self.version = version
        self.vendor = vendor
        if len(vulnerabilities) == 0:
            self.update_vulnerabilities()

    def update_vulnerabilities(self):
        self.vulnerabilities = utils.get_component_vulnerabilities(self, True)

    def __str__(self):
        s = "{0}${1}${2}".format(self.vendor, self.product, self.version)

        return s

    def reprJSON(self):
        return dict(
            id=self.id,
            vendor=self.vendor,
            product=self.product,
            version=self.version,
            last_updated=self.last_updated,
            vulnerabilities=self.vulnerabilities)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.vendor == other.vendor and self.product == other.product and self.version == other.version
