from src.models.UserComponent import UserComponent


class User:
    def __init__(self, user_id, suspicious, permissions):
        self.user_id = user_id
        self.suspicious = suspicious
        self.permissions = permissions
        self.user_components = set()

    def __str__(self) -> str:
        return 'id: {0}\tsuspicious: {1}\tpermissions: {2}\n{3}\n'.format(self.user_id,
                                                                         "true" if self.suspicious else "false",
                                                                         self.permissions, self.user_components)

    def __repr__(self) -> str:
        return 'id: {0}\tsuspicious: {1}\tpermissions: {2}\n{3}\n'.format(self.user_id,
                                                                          "true" if self.suspicious else "false",
                                                                          self.permissions, self.user_components)

    def add_component(self, component, update):
        self.user_components.add(UserComponent(component, update))

    def get_max_component_level(self):
        return max(user_component.get_risk_level() for user_component in self.user_components)

    def get_user_vulnerability_level(self):
        if self.suspicious:
            return 10
        else:
            return self.get_max_component_level() * (self.permissions / 5)
