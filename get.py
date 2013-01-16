import urllib
import os
import requests
import json
import csv, cStringIO, codecs

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

def to_csv_row(event):
    return [
        event['id'],
        unicode(event['status']),
        unicode(event['community']['urlname']),
        unicode(event['city']),
        unicode(event.get('zip','')),
        unicode(event['country']),
        event['lat'],
        event['lon'],
        event['created'],
        event['updated'],
        unicode(event['helpers']),
        unicode(event['meetup_url']),
    ]

def csv_event_header():
    return [
        'id',
        'status',
        'community_urlname',
        'city',
        'zip',
        'country',
        'lat',
        'lon',
        'created',
        'updated',
        'helpers',
        'meetup_url'
    ]

def dump_event_csv(data):
    with open('dump.csv','w') as f:
        w = UnicodeWriter(f)
        w.writerow(csv_event_header())
        for x in data['results']:
            print 'writing id=%d' % x['id']
            w.writerow( to_csv_row(x) )
        f.close()

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        def to_utf8(x):
            if type(x) is unicode:
                return x.encode("utf-8")
            return x
        self.writer.writerow([to_utf8(s) for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__=='__main__':
    # print json.dumps(list_events(), indent=4)
    dump_event_csv(list_events())
    with open('communities.json', 'w') as out:
        json.dump(list_communities(), out, indent=4)


