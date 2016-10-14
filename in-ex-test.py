#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import rdflib
import requests
import sys


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



def main():

    def auth_tuple(user):
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
                        type=auth_tuple,
                        required=False
                        )
    
    parser.add_argument('-l', '--log',
                        help='''Path to file to store output. 
                                Defaults to stdout.''',
                        action='store',
                        required=False
                        )
                        
    parser.add_argument('config',
                        help='''Path to import/export config file.''',
                        action='store'
                        )
                        
    args = parser.parse_args()

    config =

'''
    # close file if one was opened
    if args.output:
        fh.close()
'''

if __name__ == "__main__":
    main()


