import sys
import os
import urllib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

BASE_URL = "https://beacon.nist.gov/rest/record/"

class BeaconError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class Beacon(object):

    def __init__(self):
        self.last_timestamp = None

    def current_record(self, timestamp=None):
        """
        current_record: get the record closest in time to this timestamp
        """
        if not timestamp:
            timestamp = self.last_timestamp

        if not timestamp:
            raise BeaconError("No timestamp specified")

        url = BASE_URL + timestamp
        return self._call(url)


    def previous_record(self, timestamp=None):
        """
        previous_record: get the record preceding the timestamp
        """
        if not timestamp:
            timestamp = self.last_timestamp

        if not timestamp:
            raise BeaconError("No timestamp specified")

        url = BASE_URL + "previous/" + timestamp
        return self._call(url)

    def next_record(self, timestamp=None):
        """
        next_record: get the record following the timestamp
        """
        if not timestamp:
            timestamp = self.last_timestamp

        if not timestamp:
            raise BeaconError("No timestamp specified")

        url = BASE_URL + "next/" + timestamp
        return self._call(url)

    def last_record(self):
        """
        last_record: get the most recent random record
        """
        url = BASE_URL + "last"
        return self._call(url)

    def start_chain_record(self, timestamp=None):
        """
        start_chain_record: NOTE I'm not entirely sure what this does, the NIST docs are unenlightening
        """
        if not timestamp:
            timestamp = self.last_timestamp

        if not timestamp:
            raise BeaconError("No timestamp specified")
        url = BASE_URL + "start-chain/" + timestamp
        return self._call(url)

    def _call(self, url):
        """
        utility function, does the actually https call and parse the results
        """
        u = urllib.urlopen(url)
        result = u.read()
        
        data = {}
        record = ET.fromstring(result)
        for child in record:
            data[child.tag] = child.text

        self.last_timestamp = data.get('timeStamp', None)

        if not data.get('timeStamp', None):
            raise BeaconError("No data returned. Perhaps the government is down.")

        return data

def random_nums(n):
    """
    a generator for convenience
    """
    b = Beacon()
    yield b.last_record()
    for i in range(n-1):
        yield b.previous_record()




if __name__ == '__main__':
    b = Beacon()
    print b.previous_record('1380418860')
