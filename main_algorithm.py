# from src.models.Organisation import Organisation
#
# x = Organisation('src/resources/Components.json')
#
# #x.read_users_from_json_file('src/resources/Components.json')
# print(x)
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
import pycurl
from io import BytesIO

b_obj = BytesIO()
crl = pycurl.Curl()

# Set URL value
crl.setopt(crl.URL, 'https://cve.circl.lu/api/browse/microsoft')

# Write bytes that are utf-8 encoded
crl.setopt(crl.WRITEDATA, b_obj)

# Perform a file transfer
crl.perform()

# End curl session
crl.close()

# Get the content stored in the BytesIO object (in byte characters)
get_body = b_obj.getvalue()

# Decode the bytes stored in get_body to HTML and print the result
print('Output of GET request:\n%s' % get_body.decode('utf8'))