#!/usr/bin/env python3


def hello_worker(env, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    
    body = env['QUERY_STRING']
    body = body.split('&')
    body = '\n'.join(body)

    start_response(status, headers)
    return [body]

"""
from wsgiref.simple_server import make_server
httpd =  make_server('0.0.0.0', 8000, hello_worker)
httpd.serve_forever()
"""
