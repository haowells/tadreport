#!/usr/bin/env python
# coding=utf-8
__author__ = 'haowells@gmail.com'

import os
import sys
import logging
import ConfigParser

import requests
from pymongo import MongoClient
from lib import tadrest
#import pydevd
#pydevd.settrace('192.168.47.1', port=4567, stdoutToServer=True, stderrToServer=True)

################################################################################
abspath = os.path.abspath(sys.argv[0])
dirname, basename = os.path.split(abspath)
base, dummy = os.path.splitext(basename)
cfgname = '.'.join([base, 'conf'])
logname = '.'.join([base, 'log'])
logdir = os.path.join(dirname, 'logs')
cfgdir = os.path.join(dirname, 'cfg')
for dir in (logdir, cfgdir):
    if not os.path.exists(dir):
        os.makedirs(dir)

logfile = os.path.join(logdir, logname)
cfgfile = os.path.join(cfgdir, cfgname)
################################################################################


################################################################################
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logfile,
                filemode='w')

#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
################################################################################

################################################################################
cf = ConfigParser.ConfigParser()
cf.optionxform = str   ### 区分大小写
cf.read(cfgfile)

taddm_api = dict(cf.items('TADDM_API'))
#api_all_type = dict(cf.items('TADDM_API_TYPE'))
api_moc = cf.get('TADDM_API_TYPE', 'api_model_object_class')
taddm_api.update({'api_type': api_moc})

#sync_cdm_l = cf.options('SYNC_CDM')
sync_cdm_d = cf.items('SYNC_CDM')



################################################################################

client = MongoClient()
taddmdb = client.taddm

#tadrest.rest_call(cdm_class='AixUnitaryComputerSystem', cdm_depth=1, **taddm_api)

for cdm, depth in sync_cdm_d:
    coll = taddmdb[cdm]
    coll.drop()
    for ret in tadrest.rest_call(cdm_class=cdm, cdm_depth=depth, **taddm_api):
        parms=dict(guid=ret.get("_id"), cdm=ret.get("_class"))
        logging.info("CDM Class %(cdm)s -> %(guid)s", parms)
        coll.save(ret)





