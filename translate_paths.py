#!/usr/bin/env python3

import os
import requests
import sys

PATH = sys.argv[1]
CONFIGFILE = sys.argv[2]
auth = tuple(sys.argv[3].split(':'))


def is_binary(node, auth):
    ''' Using link headers, determine whether a resource is rdf or non-rdf. '''
    response = requests.head(url=node, auth=auth)
    if response.status_code == 200:
        if response.links['type']['url'] == \
            'http://www.w3.org/ns/ldp#NonRDFSource':
            return True
        else:
            return False
    else:
        print("Error communicating with repository.")
        sys.exit(1)


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
    def __init__(self, resourcepath, config):
        self.origpath = resourcepath
        
        if self.origpath.startswith('http://'):
            self.location = 'remote'
            if is_binary(self.origpath, auth):
                self.type = 'binary'
            else:
                self.type = 'rdf'
            self.relpath = self.origpath[len(config.repo):]
            
        else:
            self.location = 'local'
            if os.path.splitext(self.origpath)[1] == '.binary':
                self.type = 'binary'
                self.relpath = self.origpath[len(config.bin):]
            else:
                self.type = 'rdf'
                self.relpath = self.origpath[len(config.desc):]
                
        
'''        for prefix in [config.repo, config.desc, config.bin]:
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
            self.altpath = config.repo + self.relpath '''


def main():
    c = Config(CONFIGFILE)
    r = Resource(PATH, c)
    
    print(r.origpath)
    print(r.location)
    print(r.type)
    print(r.relpath)
    


if __name__ == "__main__":
    main()
