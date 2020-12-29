class User:
    def __init__(self, user_id, suspicious, permissions, user_components):
        self.user_id = user_id
        self.suspicious = suspicious
        self.permissions = permissions
        self.max_component_level = max(component.component_level for component in user_components)
        self.user_venerability_level = 0

    def calculate_user_venerability_level(self):
        if self.suspicious:
            self.user_venerability_level = 10
        else:
            self.user_venerability_level = self.max_component_level * (self.exposure_rating / 5)

    def get_user_venerability_level(self):
        self.calculate_user_venerability_level()
        return self.user_venerability_level
