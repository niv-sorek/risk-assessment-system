import json

from src.models.Component import Component
from src.models.User import User


class Organisation:
    def __init__(self, name):
        self.name = name
        self.users = set()
        self.components = set()

    def __str__(self) -> str:
        return '{0}\n Components: {1}\tUsers: {2}\n{3}\n'.format(self.name, len(self.components), len(self.users),
                                                                 self.users)

    def read_data_from_json_file(self, json_file):
        with open(json_file, 'r') as file:
            data = json.loads(file.read())
        self.read_users_from_json(data['users'])
        #    self.read_components_from_json(data['components'])

    def read_components_from_json(self, components_json):
        for c in components_json:
            self.components.add(Component(c['vendor'], c['product'], c['version']))

    def read_users_from_json(self, users_json):
        for u in users_json:
            created_user = User(u['id'], u['suspicious'], u['permissions'])
            for c in u['user_components']:
                if len(c['vendor']) > 0 and len(c['product']) > 0: # if legal vendor_name and product_name
                    self.components.add(Component(c['vendor'], c['product'], c['version']))
                    found_component = next((x for x in self.components if
                                            x.vendor == c['vendor'] and
                                            x.product == c['product'] and
                                            x.version == c['version']), None)
                    created_user.add_component(found_component, c['update'])
            self.users.add(created_user)
