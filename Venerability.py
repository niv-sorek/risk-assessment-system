
class Venerability:
    def __init__(self, name, level):
        self.venerability_name = name
        self.number_of_exploit = 0
        self.cvss_level = level
        self.venerability_level = self.cvss_level

     # def count_exploits(self):
     #     self.number_of_exploit =

    def calculate_venerability_level(self):
        if self.number_of_exploit is 0:
            self.venerability_level = self.cvss_level * 0.5
        if self.number_of_exploit in range(0, 3):
            self.venerability_level = self.cvss_level * 0.8
        if self.number_of_exploit in range(3, 8):
            self.venerability_level = self.cvss_level * 0.9

    def get_venerability_level(self):
        self.calculate_venerability_level()
        return self.venerability_level





