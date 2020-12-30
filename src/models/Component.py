from src import utils


class Component:
    def __init__(self, vendor, product, version=""):
        self.product = product
        self.version = version
        self.vendor = vendor
        self.vulnerabilities = utils.get_component_vulnerabilities(self, True)

    def __str__(self):
        s = "------------------\n" \
            "Vendor: {0}\tProduct: {1}\tVersion: {2}\n\tVulnerabilities:\n".format(self.vendor, self.product,
                                                                                   self.version)
        s = s + '\t\t' + '%-15s%5s%15s%22s%10s\n' % ('cve', 'exploit',
                                                     'fix', 'cvss_level',
                                                     'vullevel')
        for v in self.vulnerabilities:
            s = s + '\t\t{0}\n'.format(str(v))

        return s + '------------------\n'
