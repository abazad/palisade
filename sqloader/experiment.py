'''
Created on 01.08.2013

@author: bova
'''
f = open('1.txt', 'r')

with open('stat.txt', 'r') as fs:
    bytes_to_seek = int(fs.readline())

f.seek(bytes_to_seek)
while True:
    lines = f.readlines(20)
    if not lines:
        break
    for line in lines:
        print line
        print f.tell()

bytes_to_seek=f.tell()

with open('stat.txt', 'w+') as fs:
    fs.write('%d' % bytes_to_seek)
    
