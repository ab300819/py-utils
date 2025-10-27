#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

import json
import requests as rq


def get_access_license():
    return {}


def create_client(accessKeyId, accessSecret):
    return AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')


def get_describe_domain_record(domain):
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)

    return request


def update_domain_record():
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RecordId("18856")
    request.set_RR("ddns")
    request.set_Type("A")
    request.set_Value("127.0.0.1")

    return request


if __name__ == "__main__":
    licese = get_access_license()
    client = create_client(license['accessKeyId'], license['accessSecret'])

    record_response = client.do_action_with_exception(
        get_describe_domain_record(license['domain']))
