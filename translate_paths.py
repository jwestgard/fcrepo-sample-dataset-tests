#!/usr/bin/env python3

import os
import sys

PATH = sys.argv[1]
CONFIGFILE = sys.argv[2]


class Config():
    def __init__(self, configfile):
        print("Loading configuration options from import/export config file...")
        with open(CONFIGFILE, 'r') as f:
            opts = [line for line in f.read().split('\n')]
        for line in range(len(opts)):
            if opts[line] == '-m':
                self.mode = opts[line + 1]
            elif opts[line] == '-r':
                self.repo = opts[line + 1]
            elif opts[line] == '-d':
                self.desc = opts[line + 1]
            elif opts[line] == '-b':
                self.bin = opts[line + 1]
            elif opts[line] == '-x':
                self.ext = opts[line + 1]


class Resource():
    def __init__(self, path, config):
        self.origpath = path
        
        if path.startswith('http://'):
            self.type = 'remote'
        else:
            self.type = 'local'
        
        for prefix in [config.repo, config.desc, config.bin]:
            if path.startswith(prefix):
                self.relpath = path.lstrip(prefix)
                if self.origpath.endswith(self.relpath):
                    self.base = path[:-len(self.relpath)]
                break
        else:
            self.relpath = None
            self.base = None
            print('Error in path!')
        
        if self.type == 'local':
            self.altpath = config.repo + self.relpath


def main():
    c = Config(CONFIGFILE)
    r = Resource(PATH, c)
    print("orig", r.origpath)
    print("relpath", r.relpath)
    print("base", r.base)
    print("alt", r.altpath)
    


if __name__ == "__main__":
    main()
