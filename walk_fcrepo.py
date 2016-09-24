#!/usr/bin/env python3

import argparse
import rdflib
import requests
import sys


# using link headers, determine whether a resource is rdf or non-rdf
def is_binary(node, auth):
    response = requests.head(url=node, auth=auth)
    if response.links['type']['url'] == 'http://www.w3.org/ns/ldp#NonRDFSource':
        return True
    else:
        return False


# get the children of a resource based on ldp containment
def get_children(node, auth):
    print("checking {}...".format(node))
    if is_binary(node, auth):
        return None
    else:
        response = requests.get(node, auth=auth)
        graph = rdflib.Graph()
        graph.parse(data=response.text, format="text/turtle")
        predicate = rdflib.URIRef('http://www.w3.org/ns/ldp#contains')
        children = [str(obj) for obj in graph.objects(subject=None,
                                                      predicate=predicate)]
        return children


# iterator to walk an fcrepo repository based on ldp containment
class fcrepo_walker:
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
            children = get_children(current, self.auth)
            if children:
                self.to_check.extend(children)
            return current


def main():
    parser = argparse.ArgumentParser(
        description='Walking a Fedora repository.'
        )
    # Path to the repo config (endpoint, credentials, and WebAC paths)
    parser.add_argument('-u', '--user',
                        help='Username and password.',
                        action='store',
                        required=False
                        )
    # Path to the data set (metadata and files)
    parser.add_argument('root',
                        help='Path to root node from which to begin walk.',
                        action='store'
                        )
    # Path to the data set (metadata and files)
    parser.add_argument('output',
                        help='Path to file to store output.',
                        action='store'
                        )
    
    args = parser.parse_args()
    if args.user:
        auth = tuple(args.user.split(':'))
    
    with open(args.output, 'w') as f:
        for resource in fcrepo_walker(args.root, auth):
            f.write(resource + '\n')


if __name__ == "__main__":
    main()




