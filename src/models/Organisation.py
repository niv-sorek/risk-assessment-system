import json

from src.models.Component import Component
from src.models.Fix import Fix
from src.models.User import User
from src.models.Vulnerability import Vulnerability
from src.utils import ComplexEncoder


class Organisation:
    def __init__(self, json_file):
        self.name = ''
        self.users = []
        self.components = []
        self.json = self.read_from_json_file(json_file)
        with open('src/resources/Components.json', 'w') as file:
            file.write(self.__str__())

    def __str__(self) -> str:
        return json.dumps(self, cls=ComplexEncoder, indent=4)

    def get_user_by_id(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                return u

    def reprJSON(self):
        return dict(name=self.name, users=self.users, components=self.components)

    def read_from_json_file(self, json_file):
        """
        :param json_file: file in JSON format to read the users from it
        """
        with open(json_file, 'r') as file:
            data = json.loads(file.read())
        self.name = data['name']
        self.read_components_from_json(data['components'])
        self.read_users_from_json(data['users'])
        # print(self.components)
        return data

    def read_components_from_json(self, components_json):
        self.components.clear()
        for c in components_json:
            component = Component(c['id'], c['vendor'], c['product'], c.get("version", 0), c.get('last_updated', ""))

            for vul in c['vulnerabilities']:
                component.vulnerabilities.append(Vulnerability(vul['cve'],
                                                               Fix(vul['fix']['name'], vul['fix']['value']),
                                                               vul.get('E', None),
                                                               vul.get('AC', None),
                                                               vul.get('AV', None),
                                                               vul.get('RL', None),
                                                               vul.get('UI', None),
                                                               vul.get('PR', None)))
            self.components.append(component)

    def read_users_from_json(self, users_json):
        self.users.clear()
        for u in users_json:
            created_user = User(u['id'], u['suspicious'], u['permissions'])
            for c in u['user_components']:
                # if len(c['vendor']) > 0 and len(c['product']) > 0:  # if legal vendor_name and product_name
                found_component = next((x for x in self.components if  # search if component already exists
                                        x.id == c['id']), None)
                if found_component is not None:
                    created_user.add_component(found_component, c['update'])
            self.users.append(created_user)
