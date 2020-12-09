import requests
import crypto as cr
from requests.auth import HTTPBasicAuth
from monotonic import monotonic


def get_auth():
    return HTTPBasicAuth('lda5148', cr.decrypt(cr.lda5148_api))


def _wrap(url, expected_success_code, func):
    """ A little wrapper around an API call that prints the JSON response and displays the time elapsed. """
    print('> Calling: ' + url)
    t0 = monotonic()
    r = func()
    t1 = monotonic()
    print('  Time elapsed: {0:.3f} s'.format(t1 - t0))
    if r.status_code != expected_success_code:
        print('  An error has occurred: {0} (code {1})'.format(r.json()['message'], r.status_code))
    else:
        print('  JSON response: {0}'.format(r.json()))
    return r


def do_ping(base_api_url):
    url = base_api_url + '/ping'
    return _wrap(url, 200, lambda: requests.get(url, auth=get_auth()))


def do_upload(base_api_url, file_name):
    url = base_api_url + '/upload'
    return _wrap(url, 201, lambda: requests.post(url, auth=get_auth(), files={'file': open(file_name, 'rb')}))


def do_attach(base_api_url, id, file_name):
    url = base_api_url + '/attach/{0}'.format(id)
    return _wrap(url, 201, lambda: requests.post(url, auth=get_auth(), files={'file': open(file_name, 'rb')}))


local_base_url = 'http://localhost:5000/api'
staging_base_url = 'http://gisvms70.gis.goodyear.com:5001/api'
production_base_url = 'http://gisvms70.gis.goodyear.com:5000/api'  # To be used with care!


if __name__ == '__main__':
    # Set the target API address here (see all possible addresses above)
    base_api_url = local_base_url

    # Do a simple PING
    do_ping(base_api_url)

    # Upload & ingest a JSON data file
    r = do_upload(base_api_url, '../_samples/output.json')

    # Attach a dummy file to whatever first geometry was stored.
    _ref, _id = next(iter(r.json()['a_id_map'].items()))
    do_attach(base_api_url, _id, '../_samples/dummy.txt')


