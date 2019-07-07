from .marc import MarcXmlSplitter

from xml.parsers import expat
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.saxutils import prepare_input_source
from io import StringIO
from pathlib import Path
import unittest

class RecordCounter(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.records = 0

    def endElement(self, name):
        if name == "record":
            self.records += 1

class TestMarcXmlSplitter(unittest.TestCase):
    def setUp(self):
        with open("xmlutils/testfiles/unov.xml", "r") as xmlfile:
            self.test_records = xmlfile.read()

    def testCountRecords(self):
        records = StringIO(initial_value=self.test_records)
        
        counters = list()
        def counter_generator():
            while True:
                counter = RecordCounter()
                counters.append(counter)
                yield counter
        
        splitter = MarcXmlSplitter(parent=make_parser(), handlers=counter_generator())
        splitter.parse(records)

        for counter in counters:
            self.assertEqual(counter.records, 1)

if __name__ == '__main__':
    unittest.main()
