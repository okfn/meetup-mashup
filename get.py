import urllib
import os
import requests

def endpoint(method, parameters):
    api_key = os.environ.get('MEETUP_API_KEY')
    assert api_key is not None, 'No MEETUP_API_KEY defined in environment.'
    assert method[0] is '/', 'Endpoint must be prefixed with "/" eg. "/ew/communities"'
    url_parameters = urllib.urlencode(parameters)
    return 'https://api.meetup.com%s?key=%s&%s' % (method,api_key,url_parameters)

def list_communities():
    url = endpoint( '/ew/communities', {'urlname':'OpenKnowledgeFoundation'} )
    r = request.get(url)
    print vars(r)
    return r.text

if __name__=='__main__':
    print list_communities()

