#!/usr/bin/env python3

''' Compares two sets of Fedora 4 resources that reside either in a Fedora                 
    repository or in serialized form on disk.  
    
    The script compares the two sets of resources based on their relative paths,
    comparing both binary checksums and RDF graphs.
    
    Usage:  ./diff-fcrepo.py /path/to/repo1 http://host:port/path/to/repo2 
            -o outfile.txt -u username:password
    
    It is also possible to compare two Fedoras, or two serialized repositories.
    
    '''

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
        return None
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


class Resource_walker:
    ''' Walk an fcrepo repository either online (in LDP) or serialized. '''

    def __init__(self, root, auth):
        self.to_check = [root]
        self.auth = auth
      
    def __iter__(self):
        return self
        
    def __next__(self):
        if not self.to_check:
            raise StopIteration()
        else:
            current = self.to_check.pop()
            if current.startswith('http'):
                children = get_child_nodes(current, self.auth)
            else:
                children = get_directory_contents(current)
            if children:
                self.to_check.extend(children)
            return current


class Resource():
    ''' Object representing a resource, either local or in fcrepo. '''
    def __init__(self, root, path):
        self.path = path
        self.relpath = os.path.relpath(path, root)
        


def main():

    parser = argparse.ArgumentParser(description='''Walk an LDP repository, 
                                                    writing resource URIs to 
                                                    list.'''
                                                    )
        
    # Repository credentials
    parser.add_argument('-u', '--user',
                        help='''Repository credentials in the form 
                                username:password.''',
                        action='store',
                        required=False
                        )
    
    # File in which to store the URIs found
    parser.add_argument('-o', '--output',
                        help='''Path to file to store output. 
                                Defaults to stdout.''',
                        action='store',
                        required=False
                        )
                        
    # Paths to the two root dirs to walk
    parser.add_argument('root1',
                        help='Path to first root from which to begin walk.',
                        action='store'
                        )
    parser.add_argument('root2',
                        help='Path to second root from which to begin walk.',
                        action='store'
                        )
                        
    args = parser.parse_args()
    
    
    # split the user/password as the auth tuple, or create empty variable
    if args.user:
        auth = tuple(args.user.split(':'))
    else:
        auth = None
    
    
    # if an output file has been specified open for writing, else use stdout
    if args.output:
        fh = open(args.output, 'w')
    else:
        fh = sys.stdout

    
    # loop over each resource set
    for root in (args.root1, args.root2):
        print()
        print('checking {0}'.format(root))
        counter = 0
        
        # for each resource in the tree
        for path in Resource_walker(root, auth):
            r = Resource(root, path)
            print(r.path, r.relpath)
            
            fh.write(path + '\n')
            counter += 1
            
            if args.output:
                print("resources checked: {0}".format(counter), end='\r')
        
        # line feed to preserve counter 
        print()



  
    # loop over one set
    # look for resource in other set
    # if a binary, compare checksums
    # if rdf, compare sets of triples
    # loop over other set and perform all checks
    
    
    
    
        
        
        
    
    
    # close file if one was opened
    if args.output:
        fh.close()


if __name__ == "__main__":
    main()





