import json
import pickle

import flask

from src.models.UserComponent import UserComponent


class User:
    def __init__(self, user_id, suspicious, permissions):
        self.user_id = user_id
        self.suspicious = suspicious
        self.permissions = permissions  # permissions
        self.user_components = []

    def __str__(self) -> str:
        return 'id: {0}\tsuspicious: {1}\tpermissions: {2} - Level {4}\n{3}\n'.format(self.user_id,
                                                                                      "true" if self.suspicious else "false",
                                                                                      self.permissions,
                                                                                      self.user_components,
                                                                                      self.get_user_vulnerability_level())

    def __repr__(self) -> str:
        return str(self)

    def add_component(self, component, update):
        self.user_components.append(UserComponent(component, update))

    def get_max_component_level(self):
        return max(user_component.get_risk_level() for user_component in self.user_components)

    def get_user_vulnerability_level(self):
        if self.suspicious:
            return 10
        else:
            return self.get_max_component_level() * (self.permissions / 5)

    def reprJSON(self):
        return dict(id=self.user_id, suspicious=self.suspicious, user_components=self.user_components,
                    level=self.get_user_vulnerability_level())
