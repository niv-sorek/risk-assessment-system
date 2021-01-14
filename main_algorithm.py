from src.models.Organisation import Organisation

x = Organisation("My Org")
x.read_users_from_json_file('src/resources/Components.json')
print(x)
'''
1. Read From JSON all components & calculate components Risk + add to list
2. Read from JSON all users & create a list of Components
3. Loop over UserComponents (List) to match with Component (By unique ID) 
4. Calculate user's level by its UserComponents


// Later:
6. React Client
7. HTTPServer

'''
# TODO
