#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest


def create_client(accessKeyId,accessSecret):
    return AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

def get_describe_domain_record():
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName('happy')

def update_domain_record():
    pass

if __name__ == "__main__":
    pass