#!/usr/bin/env python3
# Fetches the infoboxes from the Factorio Wiki and outputs a dot-file from them

from sys import stderr
import random
from os.path import isfile
import json
from urllib import request
import re
from colorsys import hsv_to_rgb

query = "https://wiki.factorio.com/api.php?action=query&generator=prefixsearch&gpssearch=:Infobox:&prop=revisions&rvprop=content"
# A valid WikiMedia API request

severity = 4
"""
1 - Error
2 - Warning
3 - Info
4 - Debug
"""

form = 'dot'
"""
Implemented values:
  - markdown
  - tsv
  - dot
"""

factoriodir = '.' # Assuming we are in the factorio directory

def proccontents(contents, title):
    item_match = re.search(r"^Infobox:(?P<name>[\w\s\d\.-]+)$", title) # Shouldn't contain " (research)".
    if item_match:
        item_mdict = item_match.groupdict()
        item = item_mdict['name']
        if form == 'dot': print('    "{item}" [href="https://wiki.factorio.com/{item}"]'
                .format(item=item))
        #image_match = re.search(r"\|image\s*=\s*(?P<image>.*)\n", contents)
        #if image_match:
        #    image_mdict = image_match.groupdict()
        #    image = "https://wiki.factorio.com/images/"+image_mdict['image']
        #else:
        #    image = "https://wiki.factorio.com/images/"+re.sub(r"\s", "_", item)+".png"
        #if form == 'dot': print('    "{item}" [image="{image}"]'.format(item=item, image=image))
        iname_match = re.search(r"\|internal-name\s*=\s*(?P<iname>.*)\n", contents)
        if iname_match:
            iname_mdict = iname_match.groupdict()
            iname = iname_mdict['iname']
            image_file = factoriodir+"/data/base/graphics/icons/"+iname+".png"
            if isfile(image_file):
                image = image_file
                if form == 'dot': print('    "{item}" [image="{image}",label=""]'
                        .format(item=item, image=image_file))
            else:
                image = None
                if severity >= 2: print("Warning: Icon",image_file," doesn't exists", file=stderr)
        else:
            if severity >= 2: print("Warning: No internal name found for ",item,
                    "(means no icon available)", file=stderr)
        recipe_match = re.search(r"\|recipe = Time, (?P<time>[\d\.]+)(?P<ingredients>( \+ ([\w\s]+), ([\d\.]+))*)\n",
                contents)
        if recipe_match:
            if form == 'markdown': print("### Recipe")
            recipe_mdict = recipe_match.groupdict()
            time = recipe_mdict['time']
            ingredients = recipe_mdict['ingredients']
            if form == 'markdown': print("- Time needed: "+time+" ticks")
            if form == 'markdown': print("- Ingredients:")
            ingredient_matches = re.finditer(r" \+ (?P<ingredient>[\w\s]+), (?P<amount>[\d\.]+)(?= \+|$)",
                    ingredients)
            for ingredientNum, ingredient_match in enumerate(ingredient_matches):
                ingredient_mdict = ingredient_match.groupdict()
                ingredient = ingredient_mdict['ingredient']
                amount = ingredient_mdict['amount']
                if form == 'markdown': print("  * "+amount+" "+ingredient)
                if form == 'tsv': print(item, ingredient, amount, sep="\t")
                if form == 'dot':
                    random.seed(ingredient)
                    r, g, b = hsv_to_rgb(random.random(), 1, 0.5);
                    print('      "{ingredient}" -> "{item}" [label={amount},weight={weight},color="{color}"];'.
                            format(item=item, ingredient=ingredient, amount=amount, weight=1/int(amount), color=("#%02X%02X%02X" % (r*0xFF, g*0xFF, b*0xFF))))
            if form == 'markdown': print("- Product: "+item)
            if form == 'markdown': print()
        else:
            if severity >= 2: print("Warning: No recipe found for", item, file=stderr)
    else:
        if severity >= 2: print("Warning: Skipping page: ", title, file=stderr)

def procpage(page):
    #print(page)
    contents = page['revisions'][0]['*']
    title = page['title']
    if form == 'markdown':
        print("## "+title)
        print("### Contents")
        print("```")
        print(contents)
        print("```")
    proccontents(contents, title)

def callapi(supplementary=""):
    raw = request.urlopen(query+"&format=json"+supplementary).read()
    resp = json.loads(raw.decode('utf-8'))
    #print(json.dumps(resp, indent=4))
    for pnum in resp['query']['pages']:
        procpage(resp['query']['pages'][pnum])
    if 'continue' in resp:
        ckey = resp['continue']['continue'].split('|')[0]
        cvalue = resp['continue'][ckey]
        if severity >= 3: print("Info: Recursive call starting at ", cvalue, file=stderr)
        callapi("&"+ckey+"="+str(cvalue))

if form == 'markdown': print("# Infoboxes")
if form == 'tsv': print("Item", "Ingredient", "Amount", sep="\t")
if form == 'dot': print("digraph "" {")
if form == 'dot': print("    rankdir=LR;")
if form == 'dot': print('    node [imagepath="{fpath}/data/base/graphics/icons/"];'.format(fpath=factoriodir))
#if form == 'dot': print('    edge [];')
callapi()
if form == 'dot': print("}")

