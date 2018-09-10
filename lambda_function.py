
import json
import os
import hashlib
from urllib.parse import urlparse

print('Loading function')
salt = os.environ['IMAGE_SALT']

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def get_signature(url):
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

def lambda_handler(event, context):
    ''' Take the url parameter sign it, and return a helpful response'''


    operation = event['httpMethod']
    payload = event['queryStringParameters']
    if payload['url']:
        url = payload['url']
        bit_to_sign = extract_signable_path(url)
        signature = get_signature(bit_to_sign)
        response = {
            'originalUrl': url,
            'signature': signature,
            'signed_url': add_signature(bit_to_sign, signature)
        }
        return respond(None, response)
    else:
        return respond(None, "missing url parameter")
