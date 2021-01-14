import json
import pickle

from src import utils


class Component:
    def __init__(self, vendor, product, version=""):
        self.product = product
        self.version = version
        self.vendor = vendor
        self.vulnerabilities = utils.get_component_vulnerabilities(self, False)

    def update_vulnerabilities(self):
        self.vulnerabilities = utils.get_component_vulnerabilities(self, False)

    def __str__(self):
        s = "Vendor: {0}\tProduct: {1}\tVersion: {2}\n\tVulnerabilities:".format(self.vendor, self.product,
                                                                                 self.version)
        for v in self.vulnerabilities:
            s = s + '\n\t\t{0}'.format(str(v))

        return s

    def reprJSON(self):
        return dict(vendor=self.vendor, product=self.product, version=self.version)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.vendor == other.vendor and self.product == other.product and self.version == other.version
