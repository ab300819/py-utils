import os, re

path = 'D:\\Source\\vtk\\lib'
files = os.listdir(path)

file_name = []

for f in files:
    path = os.path.join(path, f)
    if not os.path.isdir(path):
        file_name.append(f)

match = list(filter(lambda x: True if not re.findall(r'.*d\.lib', x) else False, file_name))

value = ''
for f in match:
    # value += f + ';'
    lib_name = re.search(r'(.*)\.lib', f)
    print('\t-l' + lib_name.group(1) + ' \\')
# print(value)
