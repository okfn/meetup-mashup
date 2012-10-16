import urllib
import os
import requests
import json

container_name = 'OpenKnowledgeFoundation'
container_id = 14142

def get_json(method, parameters):
    api_key = os.environ.get('MEETUP_API_KEY')
    assert api_key is not None, 'No MEETUP_API_KEY defined in environment.'
    assert method[0] is '/', 'Endpoint must be prefixed with "/" eg. "/ew/communities"'
    url_parameters = urllib.urlencode(parameters)
    url = 'https://api.meetup.com%s?key=%s&%s' % (method,api_key,url_parameters)
    r = requests.get(url)
    return json.loads(r.text)

def list_communities():
    return get_json( '/ew/communities', {'container_id':container_id} )

def list_events():
    return get_json( '/ew/events', {'container_id':container_id} )

if __name__=='__main__':
    print json.dumps(list_events(), indent=4)

