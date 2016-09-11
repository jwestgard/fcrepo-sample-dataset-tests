#!/usr/bin/env python3

import sys
import re
import requests

auth = ('fedoraAdmin', 'secret3')


def load_checksums(checksumfile):
    ''' create dictionary of filenames and sha1 checksums from file '''
    result = {}
    with open(checksumfile, 'r') as f1:
        for line in f1:
            match = re.match(r'^SHA1\((.+?)\)= (.+?)$', line)
            if match:
                result[match.group(1)] = match.group(2)
    return result


def get_metadata(image_uri):
    ''' get image filename from Fedora object metadata '''
    response = requests.get('{0}/fcr:metadata'.format(image_uri), auth=auth)
    file_match = re.search(r'ebucore:filename \"(.+?)\"', response.text)
    sha1_match = re.search(r'premis:hasMessageDigest <urn:sha1:(.+?)>',
                           response.text
                           )
    if file_match and sha1_match:
        return file_match.group(1), sha1_match.group(1)


def main():
    ''' loop over URIs in supplied file and verify checksums in Fedora '''
    checksums = load_checksums(sys.argv[1])
    checksum_count = len(checksums)
    verified_count = 0
    
    print()
    print("CHECKSUM VERIFICATION")
    print("=" * 110)
    
    with open(sys.argv[2], 'r') as uri_file:
        for n, line in enumerate(uri_file):
            (patent_uri, image_uri) = line.rstrip('\n').split('\t')
            (filename, checksum) = get_metadata(image_uri)
            if checksum == checksums[filename]:
                verified_count += 1
                print("{0:3}. Verified {1}: {2} = {3}".format(
                    n+1, filename, checksum, checksums[filename]
                    ))
            else:
                print("{0:3}. Mismatch! {0}: {1} != {2}".format(
                    n+1, filename, checksum, checksums[filename]
                    ))
    print("=" * 110)
    print("Test complete: {0}/{1} successfully verified.".format(
                                                verified_count, checksum_count
                                                ))
    print()

if __name__ == "__main__":
    main()
