#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: es.py
@time: 2018-04-10 20:28
"""


from elasticsearch import Elasticsearch


class ES(object):
    def __init__(self, es_client):
        self.es_client = es_client  # type: Elasticsearch

    def delete_index(self, index):
        return self.es_client.indices.delete(index=index) if self.es_client.indices.exists(index=index) else None

    def create_index(self, index):
        return self.es_client.indices.create(index=index)

    def create_mapping(self, index, doc_type, body):
        return self.es_client.indices.put_mapping(doc_type=doc_type, body=body, index=index)

    def add_index(self, index, doc_type, body, id=None):
        return self.es_client.index(index=index, doc_type=doc_type, body=body, id=id)

    def refresh_index(self, index):
        return self.es_client.indices.refresh(index=index)

    def search_fulltext(self, index, doc_type, field, keywords):
        """
        全文检索
        :param index:
        :param doc_type:
        :param field:
        :param keywords:
        :return:
        """
        query_body = {
            'query': {'match': {field: keywords}},
            'highlight': {
                'pre_tags': ['<span class="text-primary">'],
                'post_tags': ['</span>'],
                'fields': {
                    field: {}
                }
            }
        }

        query_data = {
            'total': 0,
            'data': []
        }
    
        es_res = self.es_client.search(index=index, doc_type=doc_type, body=query_body)
        query_data['total'] = es_res['hits']['total']
        query_data['data'] = map(lambda x: {'label': x['highlight'][field][0], 'value': x['_source'][field]}, es_res['hits']['hits'])
        return query_data