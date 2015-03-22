#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower        = re.compile(r'^([a-z]|_)*$')
lower_colon  = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addresschars = re.compile(r'addr:(\w+)')
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

street_expected = ["улица", "бульвар", "проспект", "площадь", "переулок", "шоссе", "набережная", "проезд", "обход", "трасса", "аллея"]
street_start_with = 'улица'
street_mapping = { 
            "ул.": "улица",
            "пр.": "проспект",
            "пл." : "площадь"
          }

def is_street_name(key):
    return (key == "addr:street")

def is_postcode_name(key):
    return (key == "addr:postcode")

def audit_street(street_name):
    m = street_type_re.search(street_name.strip())
    m = street_name.split(' ')
    if len(m) > 1:
        street_type = m[0]
        if street_type.encode('utf-8').lower() not in street_expected:
            #print "{} => {}".format(street_name.encode('utf-8'), update_street_name(street_name.encode('utf-8')))
            street_name = update_street_name(street_name.encode('utf-8'))

    return street_name

def update_street_name(name):
    # Short to long version
    for n in street_mapping.keys():
      if n in name:
        name = name.replace(n,dict[n])
  
    chunks = name.split(' ')
    lower_chunks = [item.lower() for item in chunks]

    # If street name without expected value we will add common prefix 'улица'
    if len(set(street_expected) & set(lower_chunks)) == 0:
      name = street_start_with + ' ' + name
    
    # if common prefix 'улица' in the end of street name, we will more it on first place
    if chunks[-1] == 'улица':
      name = chunks[-1] + ' ' + ' '.join(chunks[0:-1])

    return name

def convertPhone(phone):
    # Krasnodar Postal code(s) https://en.wikipedia.org/wiki/Krasnodar
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

def audit_postcode(postcode):
    # Krasnodar dialing code https://en.wikipedia.org/wiki/Krasnodar
    # Remove all non number characters as first step
    postcode = re.sub('\D', '', postcode)
    if int(postcode) < 350000 or (int(postcode) > 359999 and postcode.rfind('385') == -1):
      #print "Error post code => {} converted to 350000".format(int(postcode))      
      # Set main  Krasnodar postcode for wrong entry
      postcode = 350000

    return postcode

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node = { 'created': {}, 'type': element.tag }
        for k in element.attrib:
            try:
                v = element.attrib[k]
            except KeyError:
                continue
            if k == 'lon' or k == 'lat':
                continue
            if k in CREATED:
                node['created'][k] = v
            else:
                node[k] = v
        try:
            node['pos'] = [ float(element.attrib['lat']), float(element.attrib['lon']) ]
        except KeyError:
            pass
        
        for stag in element.iter('tag'):
            if 'address' not in node.keys():
                node['address'] = {}
            k = stag.attrib['k']
            v = stag.attrib['v']
            
            if k.startswith('addr:'):
                # Wrangle street name
                if is_street_name(k):
                  v = audit_street(v) # Audit and fix broken street names
                if is_postcode_name(k):
                  v = audit_postcode(v)

                if len(k.split(':')) == 2:
                    content = addresschars.search(k)
                    if content:
                        node['address'][content.group(1)] = v
            if k.startswith('phone') or k.startswith('contact:phone'):
              data = []
              s = re.split('[,;]', v)
              for i in s:
                  data.append(convertPhone(i))
              node[k] = ', '.join(data)
            else:
                node[k] = v

        if element.tag == "way":
            node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    data = process_map('krasnodar.osm', False)