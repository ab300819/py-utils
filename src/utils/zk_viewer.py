#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'mason'

from kazoo.client import KazooClient


class ZkNode(object):
    def __init__(self, path, data, stat):
        if path == '':
            self.__node = path
        elif path == '/':
            self.__node = path
        else:
            self.__node = path.split('/')[-1]
        self.__path = path
        self.__data = data
        self.__stat = stat
        self.__child = []

    def get_node(self):
        return self.__node

    def set_child(self, child):
        self.__child.append(child)

    def get_data(self):
        return self.__data

    def get_stat(self):
        return self.__stat

    def get_child(self):
        return self.__child


def zk_walk(zk, node, node_info, level=0):
    data, stat = zk.get(node)
    current_node = ZkNode(node, data.decode('utf-8'), stat)
    node_info.set_child(current_node)
    children = zk.get_children(node)
    if len(children) > 0:
        for sub in children:
            sub_node = node + '/' + sub if node != '/' else '/' + sub
            zk_walk(zk, sub_node, current_node, level + 1)


def print_node(node, level):
    if level == 0:
        print('/')
    path_list = node.split('/')
    if len(path_list) < 1:
        return
    path = ''
    for i in range(0, level):
        path += '-'
    path = path + path_list[-1]
    print(path)


zk = KazooClient(hosts='', timeout=10)
zk.start()

root_node = ZkNode('', '', '')
zk_walk(zk, '/', root_node)

zk.stop()
zk.close()
