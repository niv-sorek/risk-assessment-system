
class User:
    def __init__(self, is_suspicious, components, exposure_rating):
        self.is_suspicious = is_suspicious
        self.exposure_rating = exposure_rating
        self.max_component_level = max(component.component_level for component in components)
        self.user_venerability_level = 0

    def calculate_user_venerability_level(self):
        if self.is_suspicious:
            self.user_venerability_level = 10
        else:
            self.user_venerability_level = self.max_component_level * (self.exposure_rating / 5)

    def get_user_venerability_level(self):
        self.calculate_user_venerability_level()
        return self.user_venerability_level

