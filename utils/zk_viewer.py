#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

from kazoo.client import KazooClient

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s %(funcName)s%(lineno)d %(levelname)s: %(message)s')

zk = KazooClient(hosts='', timeout=10, logger=logging)
zk.start()

data, stat = zk.get('/')
print(data)
print(stat)

children = zk.get_children('/')
print(children)

zk.stop()
zk.close()
