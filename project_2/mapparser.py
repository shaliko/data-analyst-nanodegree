#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
{
 'bounds': 1,
 'member': 20552,
 'meta': 1,
 'nd': 586928,
 'node': 504105,
 'note': 1,
 'osm': 1,
 'relation': 902,
 'tag': 582681,
 'way': 100577
}
"""
import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    
    for ev, element in ET.iterparse(filename):
        tag = element.tag

        if tag not in tags.keys():
            tags[tag] = 1
        else:
            tags[tag] += 1
            
    return tags


def test():

    tags = count_tags('krasnodar.osm')
    pprint.pprint(tags)
    # assert tags == {'bounds': 1,
    #                  'member': 3,
    #                  'nd': 4,
    #                  'node': 20,
    #                  'osm': 1,
    #                  'relation': 1,
    #                  'tag': 7,
    #                  'way': 1}

    

if __name__ == "__main__":
    test()