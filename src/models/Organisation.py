import json

from src.models.Component import Component
from src.models.User import User
from src.utils import ComplexEncoder


class Organisation:
    def __init__(self, json_file):
        self.name = ''
        self.users = []
        self.components = set()
        self.json = self.read_from_json_file(json_file)

    def __str__(self) -> str:
        return json.dumps(self, cls=ComplexEncoder, indent=4)

    def get_user_by_id(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                return u

    def reprJSON(self):
        return dict(name=self.name, users=self.users)

    def read_from_json_file(self, json_file):
        """
        :param json_file: file in JSON format to read the users from it
        """
        with open(json_file, 'r') as file:
            data = json.loads(file.read())
        self.read_users_from_json(data['users'])
        self.name = data['name']
        return data

    def read_components_from_json(self, components_json):
        for c in components_json:
            self.components.add(Component(c['vendor'], c['product'], c['version']))

    def read_users_from_json(self, users_json):
        self.users.clear()
        for u in users_json:
            created_user = User(u['id'], u['suspicious'], u['permissions'])
            for c in u['user_components']:
                if len(c['vendor']) > 0 and len(c['product']) > 0:  # if legal vendor_name and product_name
                    found_component = next((x for x in self.components if  # search if component already exists
                                            x.vendor == c['vendor'] and
                                            x.product == c['product'] and
                                            x.version == c['version']), None)
                    if found_component is None:
                        found_component = Component(c['vendor'], c['product'], c['version'])

                    self.components.add(found_component)
                    created_user.add_component(found_component, c['update'])
            self.users.append(created_user)
