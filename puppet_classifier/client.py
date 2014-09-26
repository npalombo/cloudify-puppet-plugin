__author__ = 'npalombo'

import urlparse
import requests

"""
Helper functions and classes for the Puppet REST API using the requests module.
"""

def handle_response(response):
    """
    Check response code and content type. Raise exception for errors, otherwise return text or json.
    """
    if response.status_code >= 400:
        raise handle_response_exception(response)
    else:
        content_type = response.headers.get('content-type')
        if content_type is not None and content_type.startswith('application/json'):
            return response.status_code, response.json()
        else:
            return response.status_code, response.text

def handle_response_exception(response):
    """
    Parse out the details of the exception from the response object.
    """
    message = 'Response Exception - url: %s, method: %s, status code: %s, text: %s' % \
        (response.url, response.request.method, response.status_code, response.text)
    return Exception(message)

class HTTPClient(object):
    """
    Wrapper class for HTTP methods.
    """

    def __init__(self, endpoint_url, cert=None, key=None, cacert=None):
        """
        endpoint_url is a string with the URL to the Puppet Classifier API. Can be HTTP or HTTPS.
        If HTTPS, then cert, key, and cacert must be specified. They will be string values that
        contain the path to the cert, key, and cacert files. Those files must be retrieved from
        the Puppet master. The way to get them is to configure and run the the Puppet agent on the
        host where this HTTP client will be running. The command is `puppet agent --test`. The
        files should then be located as follows:
            key: /var/lib/puppet/ssl/private_keys/precise32.pem
            cert: /var/lib/puppet/ssl/certs/precise32.pem
            cacert: /var/lib/puppet/ssl/certs/ca.pem
        """
        self.VERSION = 'v1'
        self.endpoint_url = endpoint_url
        self.cert = None
        if cert is not None and key is not None:
            self.cert = (cert, key)
        self.cacert = cacert

    def urljoin(self, path):
        """
        Helper to make URLs
        """
        data = list(urlparse.urlsplit(self.endpoint_url))
        pieces = [self.VERSION] + path.split('/')
        path = '/'.join(s.strip('/') for s in pieces)
        data[2] = path
        return urlparse.urlunsplit(data)

    def _get(self, path, params=None):
        """
        GET method
        """
        url = self.urljoin(path)
        return requests.get(url, params=params, cert=self.cert, verify=self.cacert)

    def _post(self, path, body):
        """
        POST method
        """
        url = self.urljoin(path)
        return requests.post(url, data=body, cert=self.cert, verify=self.cacert)

    def _delete(self, path):
        """
        DELETE method
        """
        url = self.urljoin(path)
        return requests.delete(url, cert=self.cert, verify=self.cacert)

