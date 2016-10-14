#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import rdflib
import requests
import sys


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


def get_child_nodes(node, auth):
    ''' Get the children based on LDP containment. '''
    if is_binary(node, auth):
        metadata = [node + "/fcr:metadata"]
        return metadata
    else:
        response = requests.get(node, auth=auth)
        if response.status_code == 200:
            graph = rdflib.Graph()
            graph.parse(data=response.text, format="text/turtle")
            predicate = rdflib.URIRef('http://www.w3.org/ns/ldp#contains')
            children = [str(obj) for obj in graph.objects(
                            subject=None, predicate=predicate
                            )]
            return children
        else:
            print("Error communicating with repository.")
            sys.exit(1)


def get_directory_contents(localpath):
    ''' Get the children based on the directory hierarchy. '''
    if os.path.isfile(localpath):
        return None
    else:
        return [p.path for p in os.scandir(localpath)]


class Config():
    def __init__(self, configfile):
        print("Loading configuration options from import/export config file...")
        with open(configfile, 'r') as f:
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


class Walker:
    ''' Walk a set of Fedora resources. '''
    def __init__(self, root):
        self.to_check = [root]
      
    def __iter__(self):
        return self


class FcrepoWalker(Walker):
    ''' Walk resources in a live repository. '''
    def __init__(self, root, auth):
        Walker.__init__(self, root)
        self.auth = auth
    
    def __next__(self):
        if not self.to_check:
            raise StopIteration()
        else:
            current = self.to_check.pop()
            children = get_child_nodes(current, self.auth)
            if children:
                self.to_check.extend(children)
            return current


class LocalWalker(Walker):
    ''' Walk serialized resources on disk. '''
    def __init__(self, root):
        Walker.__init__(self, root)
        
    def __next__(self):
        if not self.to_check:
            raise StopIteration()
        else:
            current = self.to_check.pop()
            children = get_directory_contents(current)
            if children:
                self.to_check.extend(children)
                return None
            else:
                return current


class Resource():
    ''' Object representing a resource, either local or in fcrepo. '''
    def __init__(self, path, config):
        if path.startswith(config.repo):
            print("this is an fcrepo resource")
        elif path.startswith(config.bin):
            print("this is a local binary")
        elif path.startswith(config.desc):
            print("this is a local rdf resource")
        else:
            print("ERROR reading resource at {0}.".format(path))
    
        
        
        
        
    '''   
    def local_to_fcrepo(self, config):
        if self.fullpath.endswith('fcr%3Ametadata.ttl'):
            self.resourcetype = 'rdf'
            # replace end with fcr:metadata and remove descdir
        elif self.fullpath.endswith('.binary'):
            # remove extension and bindir
            self.resourcetype = 'nonrdf'
        else:
            self.resourcetype = 'rdf'
            # remove descdir and extension
        result = config.fcrepo
        
        pass 
    
    def fcrepo_to_local(self, config):
        pass '''
        

def main():

    def credentials(user):
        '''Custom '''
        auth = tuple(user.split(':'))
        if len(auth) == 2:
            return auth
        else:
            raise argparse.ArgumentTypeError(
                '''Credentials must be given in the form user:password.'''
                )

    parser = argparse.ArgumentParser(
                        description='''Compare two sets of Fedora resources, 
                        either in fcrepo or serialized on disk.'''
                        )
        
    parser.add_argument('-u', '--user',
                        help='''Repository credentials in the form 
                                username:password.''',
                        action='store',
                        type=credentials,
                        required=False
                        )
    
    parser.add_argument('-l', '--log',
                        help='''Path to file to store output. 
                                Defaults to stdout.''',
                        action='store',
                        required=False
                        )
                        
    parser.add_argument('configfile',
                        help='''Path to import/export config file.''',
                        action='store'
                        )
                        
    args = parser.parse_args()

    config = Config(args.configfile)
    
    if config.mode == 'export':
        trees = [FcrepoWalker(config.repo, args.user)]
    elif config.mode == 'import':
        trees = [LocalWalker(config.bin), LocalWalker(config.desc)]
        
    for walker in trees:
        for resource in walker:
            if resource:
                print(resource)
                r = Resource(resource, config)


    '''
    # close file if one was opened
    if args.output:
        fh.close()
    '''

if __name__ == "__main__":
    main()


