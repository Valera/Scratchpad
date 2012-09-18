#!/usr/bin/env python3

import os, os.path, hashlib

def dict_append(dic, key, new_elem):
    if key in dic:
        dic[key].append(new_elem)
    else:
        dic[key] = [new_elem]

class MyFile:

    def __init__(self, name, path, parent_dir):
        self.name = name
        self.path = path
        self.parent_dir = parent_dir
        self.size = os.path.getsize(path)

    def __repr__(self):
        return '<MyFile path="{0}">'.format(self.path)

class MyDir:

    def __init__(self, path, subdir_names, files):
        self.path = path
        self.subdir_names = subdir_names
        self.files = files

    def link_subdirs(self):
        self.subdirs = [ dirpool.pop(os.path.join(self.path, subdir_name))
                            for subdir_name in self.subdir_names]
        for sub in self.subdirs:
            sub.link_subdirs()

    def process_dir(self):
        for subdir in self.subdirs:
            subdir.process_dir()
        similar = {}
        total_size = 0
        for myfile in files:
            total_size += myfile.size + 1
            if myfile.path in collidingFiles:
                for collFile in collidingFiles[myfile.path]:
                    if collFile.parent_dir != self.path:
                        similar[collFile.parent_dir] = similar.get(collFile.parent_dir, 0) + collFile.size + 1
        for key in similar:
            similar[key] /= total_size
        self.similar = similar

top = 'test'
#filepool = {}
dirpool = {}
filesBySize = {}
for dirpath, dirnames, filenames in os.walk(top):
    print(dirpath, filenames)
    files = []
    for f in filenames:
        myfile = MyFile(f, os.path.join(dirpath, f), dirpath)
        dict_append(filesBySize, myfile.size, myfile)
        files.append(myfile)
    dirpool[dirpath] = MyDir(dirpath, dirnames, files)
topDir = dirpool[top]
dirpool[top].link_subdirs()
del dirpool[top]
print("dirpool:", dirpool)
assert(dirpool == {})

collidingFiles = {}
for size, files in filesBySize.items():
    if len(files) > 1:
        md5sums = {}
        for myfile in files:
            with open(myfile.path, 'rb') as f:
                dict_append(md5sums, hashlib.md5(f.read()).hexdigest(), myfile)
        print('md5sums:', md5sums)
        for md5, files1 in md5sums.items():
            if len(files1) > 1:
                for myfile in files1:
                    f = files1[:]
                    f.remove(myfile)
                    collidingFiles[myfile.path] = f
                print('equal files:', files1)
del filesBySize # We do not need it anymore, and it can consume much memory.

print(collidingFiles)

# TODO: восходить по списку директорий
topDir.process_dir()
print('sim:', topDir.similar)





