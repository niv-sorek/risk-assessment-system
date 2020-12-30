# from Component import Component
# from User import User
# import pandas as pd
#
# #need to install 'xlrd'
# file_name = "/Users/lirshindalman/Documents/Book2.xlsx"
# xl = pd.read_excel(file_name,  sheet_name=0)
# components_names = xl['name'].tolist()
# components_vendors = xl['vendor'].tolist()
# components = []
# users = []
# #create components list
# for i in range(len(components_names)):
#     components.append(Component(components_names[i], components_vendors[i]))
#
# xl = pd.ExcelFile(file_name)
# #create users list
# for i in range(1, len(xl.sheet_names)):
#     user_components = []
#     xl = pd.read_excel(file_name, sheet_name=i)
#     components_names = xl['name'].tolist()
#     components_vendors = xl['vendor'].tolist()
#     for y in range(len(components_names)):
#         for x in components:
#             if x.name == components_names[y]:
#                 if x.vendor == components_vendors[y]:
#                     user_components.append(x)
#     users.append(User(xl['suspicious'], user_components, xl['exposure_rating']))
#
#
#
#
