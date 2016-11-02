#!-*-encoding:utf-8 -*-

import pymongo as mg


def connect(host, port):
    client = mg.MongoClient(host, port)
    db = client.movies

    return db.movie


if __name__ == '__main__':
    mongodb = connect('localhost', 27017)

