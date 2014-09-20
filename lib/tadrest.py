#!/usr/bin/env python
# coding=utf-8
__author__ = 'linhao'

import requests
import logging
#import pydevd
#pydevd.settrace('192.168.47.1', port=4567, stdoutToServer=True, stderrToServer=True)

def rest_call(api_host=None, api_port=9430, api_user='administrator', api_password='collation',
         api_feed='json', api_type=None, cdm_class=None, cdm_depth=None, position=1, collection=None):
    #mql = 'select displayName,BIOSManufacturer from ComputerSystem'
    #mql = 'select CPU.numCPUs,CPU.CPUType,CPU.CPUSpeed from AixUnitaryComputerSystem'

    url = 'http://%s:%s/%s/%s' % (api_host, api_port, api_type, cdm_class)
    json_len = 1
    while json_len > 0:
        mql_dict = {'feed': api_feed, 'depth': cdm_depth, 'position': position}
        r = requests.get(url, auth=(api_user, api_password), params=mql_dict)
        position += 1
        clength = int(r.headers.get('Content-Length', 0))
        logging.debug(r.url)
        logging.debug(r.status_code)
        logging.debug("Content-Length: %d", clength)
        json_len = len(r.json())
        if json_len > 0:
            ret_json = r.json()[0]
            ret_json.update(_id=ret_json.get('guid'))
            logging.debug(ret_json)
            #print ret_json
            yield ret_json
        #collection.save(ret_json)
