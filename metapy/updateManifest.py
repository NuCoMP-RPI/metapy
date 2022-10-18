import os
from os import listdir
from os.path import isfile, join

mypath = os.path.abspath(join(os.getcwd(), 'lib'))
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

manifest = open('./manifest.mf', 'w')
manifest.write('Manifest-version: 1.0\nClass-Path: ')
cp = ''

for i in range(len(onlyfiles)):
    if( i == len(onlyfiles) - 1):
        cp = cp + './lib/' + onlyfiles[i] + ' \n'
    else:
        cp = cp + './lib/' + onlyfiles[i] + ' \n '
manifest.write(cp + 'Main-Class: EntryPoint\n')
manifest.close()
print('manifest updated')
