#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')



def convertPhone(phone):
    # Remove all non number characters as first step
    phone = re.sub('\D', '', phone)

    if len(phone) == 10:
        phone = "+7" + phone
    elif len(phone) == 7:
        phone = "+7861" + phone
    elif len(phone) == 12:
        phone = "+7861" + phone[-7:]
    elif len(phone) == 11:
        phone = "+" + phone

    if len(phone) == 12:
        phone = phone[0:2] + ' ' + phone[2:5] + ' ' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]

    return phone

def key_type(element, keys):
    if element.tag == "tag" and 'k' in element.attrib:
        if element.attrib['k'] in ['phone', 'contact:phone']:
            s = re.split('[,;]', element.attrib['v'])
            data = []
            for i in s:
                data.append(convertPhone(i)) 
            print data
            print s
    return keys



def process_map(filename):
    data = {}
    for _, element in ET.iterparse(filename):
        data = key_type(element, data)

    return data



def test():
    keys = process_map('krasnodar.osm')
    pprint.pprint(keys)

if __name__ == "__main__":
    test()