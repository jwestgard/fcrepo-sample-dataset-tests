#!/user/bin/env python3

import os
import sys


def get_children(p):
    print("checking {}...".format(p))
    if os.path.isfile(p):
        return None
    else:
        return [p.path for p in os.scandir(p)]


class file_walker:
    def __init__(self, root):
        self.to_check = [p.path for p in os.scandir(root)]

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.to_check:
            raise StopIteration()
        else:
            current = self.to_check.pop()
            children = get_children(current)
            if children:
                self.to_check.extend(children)
            return current


if __name__ == "__main__":
    print(len([f for f in file_walker(sys.argv[1])]))
