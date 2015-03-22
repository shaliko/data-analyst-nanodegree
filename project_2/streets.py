#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "krasnodar.osm"
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)


expected = ["улица", "бульвар", "проспект", "площадь", "переулок", "шоссе", "набережная", "проезд", "обход", "трасса", "аллея"]
start_with = 'улица'

mapping = { 
            "ул.": "улица",
            "пр.": "проспект",
            "пл." : "площадь"
          }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name.strip())
    m = street_name.split(' ')
    if len(m) > 1:
        street_type = m[0]
        if street_type.encode('utf-8').lower() not in expected:
            print "{} => {}".format(street_name.encode('utf-8'), update_name(street_name.encode('utf-8'), mapping))

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

def update_name(name, mapping):
    # Short to long version
    for n in mapping.keys():
      if n in name:
        name = name.replace(n,dict[n])
  
    chunks = name.split(' ')
    lower_chunks = [item.lower() for item in chunks]

    # If street name without expected value we will add common prefix 'улица'
    if len(set(expected) & set(lower_chunks)) == 0:
      name = start_with + ' ' + name
    
    # if common prefix 'улица' in the end of street name, we will more it on first place
    if chunks[-1] == 'улица':
      name = chunks[-1] + ' ' + ' '.join(chunks[0:-1])

    return name

if __name__ == '__main__':
    audit(OSMFILE)