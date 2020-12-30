from src import utils


class Component:
    def __init__(self, vendor, product, version):
        self.product = product
        self.version = version
        self.vendor = vendor
        self.vulnerabilities = self.get_vulnerabilities()

    #  self.component_level = max(venerability.venerability_level for venerability in self.vulnerabilities)

    def get_vulnerabilities(self):
        self.vulnerabilities = utils.get_component_vulnerabilities(self)
        print(str(v) for v in self.vulnerabilities)
        return utils.get_component_vulnerabilities(self)

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
