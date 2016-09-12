#!/usr/bin/env python3

from io import StringIO
import os
from rdflib import Graph
import requests
import sys

INPUTFILE = sys.argv[1]
OUTDIR = sys.argv[2]
AUTH = ('fedoraAdmin', 'secret3')
HEADERS = {'Accept': 'application/n-triples',
           'Prefer': 'return=minimal'
           }

with open(INPUTFILE, 'r') as f:
    for line in f:
        (patent_uri, image_uri) = line.strip('\n').split('\t')
        uuid = os.path.split(patent_uri)[1]
        response = requests.get(patent_uri, auth=AUTH, headers=HEADERS)
        g = Graph()
        g.parse(StringIO(response.text), format="turtle")
        outpath = os.path.join(OUTDIR, uuid)
        with open(outpath, 'wb') as f2:
            f2.write(g.serialize(format='n3'))

