
import json
import os
import hashlib
from urllib.parse import urlparse
import re

print('Loading function')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'access-control-allow-headers': '*',
            'access-control-allow-methods': 'GET,OPTIONS'
        },
    }

def get_signature(url, salt):
    salted_url = salt + url
    encoded = salted_url.encode('utf-8')
    signature = hashlib.md5(encoded)
    return signature.hexdigest()

def extract_signable_path(url):
    url_parsed = urlparse(url)
    if (url_parsed.query):
        return url_parsed.path + '?' + url_parsed.query
    else:
        return url_parsed.path

def add_signature(url, signature):
    if "?" in url:
        return url + "&s=" + signature
    else:
        return url + "?s=" + signature

def get_source(url):
    url_parsed = urlparse(url)
    split = re.search('(media|static|uploads|sport).guim.co.uk', url_parsed.hostname)
    if split:
        return split.group(1)
    else:
        return 'media'

def generate_iguim_url(signed_path, source):
    return f'https://i.guim.co.uk/img/{source}{signed_path}'

def add_quality_parameter(path):
    if "quality=" in path:
        return path
    elif "?" in path:
        return f'{path}&quality=85'
    else:
        return f'{path}?quality=85'


def lambda_handler(event, context):
    ''' Take the url parameter sign it, and return a helpful response'''
    salt = os.environ['IMAGE_SALT']
    operation = event['httpMethod']
    payload = event['queryStringParameters']

    if payload['url']:
        url = payload['url']
        path_with_query = extract_signable_path(url)
        path_with_quality = add_quality_parameter(path_with_query)
        signature = get_signature(path_with_quality, salt)
        signed_path = add_signature(path_with_quality, signature)
        signed_url = generate_iguim_url(signed_path, get_source(url))
        response = {
            'originalUrl': url,
            'signature': signature,
            'signed_path': signed_path,
            'iguim_url': signed_url
        }
        return respond(None, response)
    else:
        return respond(None, "missing url parameter")
