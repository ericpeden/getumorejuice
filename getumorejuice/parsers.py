# converters, part of getumorejuice, converts specially formatted files to JSON
# Copyright (C) 2013  Eric Peden
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import string
from decimal import Decimal
from itertools import takewhile
import simplejson as json


def split_ingredient(line):
    amt, name = line.strip().split(" ", 1)
    if amt.endswith("%"):
        return {"percentage": Decimal(amt.rstrip("%"))/100, "name": name}
    else:
        return {"parts": Decimal(amt), "name": name}


def parse_recipe(text):
    lines = text.splitlines()
    title = lines[0]
    assert title and not lines[1], "Malformed recipe"
    
    rest = iter(lines[2:])
    
    ingredients = [split_ingredient(ing)
                   for ing in takewhile(string.strip, rest)]
    comments = list(rest)
    
    recipe = {
        "title": title,
        "ingredients": ingredients,
        "comments": comments
    }
    return recipe
    

def parse_ingredient(text):
    pass


def main():
    for path in sys.argv[1:]:
        if not os.path.exists(path):
            raise Exception("Could not find file/directory %s" % path)
            
        if os.path.isdir(path):
            files = [os.path.join(path, p) for p in os.listdir(path)]
        else:
            files = [path]
            
        ext2parser = {
            ".recipe": parse_recipe,
            ".ingredient": parse_ingredient,
        }
        
        for fpath in files:
            _, ext = os.path.splitext(fpath)
            try:
                parser = ext2parser[ext]
            except KeyError:
                continue
            else:
                with open(fpath) as f:
                    content = f.read()
                parser(content)

    
if __name__ == '__main__':
    main()