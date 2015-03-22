#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "krasnodar.osm"

def audit_postcode(postcode, element):
    # Remove all non number characters as first step
    postcode = re.sub('\D', '', postcode)
    if int(postcode) < 350000 or (int(postcode) > 359999 and postcode.rfind('385') == -1):
      print "Error post code => {} converted to 350000".format(int(postcode))
      
      # Set main  Krasnodar postcode for wrong entry
      postcode = 350000

    return postcode

def is_postcode_name(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode_name(tag):
                    audit_postcode(tag.attrib['v'], elem)
    return True

if __name__ == '__main__':
    audit(OSMFILE)