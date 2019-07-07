from xml.sax.saxutils import XMLFilterBase
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl as Attributes
from itertools import count

class MarcXmlSplitter(XMLFilterBase):
    uri = "http://www.loc.gov/MARC21/slim"
    
    def __init__(self, parent = None, handlers = None):
        XMLFilterBase.__init__(self, parent)
        if handlers is None:
            self.handlers = (ContentHandler() for i in count())
        self.handlers = handlers
        self.processed = 0
        self.new_handler()

    def new_handler(self):
        handler = next(self.handlers)
        XMLFilterBase.setContentHandler(self, handler)

    def startElement(self, name, attrs):
        if name == "record":
            if self.processed > 0:
                self.new_handler()
                XMLFilterBase.startDocument(self)
                XMLFilterBase.startPrefixMapping(self, "", self.uri)
                XMLFilterBase.startElement(self, "collection", Attributes({}))
        if name != "collection":
            XMLFilterBase.startElement(self, name, attrs)

    def endElement(self, name):
        if name == "record":
            XMLFilterBase.endElement(self, name)
            XMLFilterBase.endElement(self, "collection")
            XMLFilterBase.endPrefixMapping(self, "")
            XMLFilterBase.endDocument(self)
            self.processed += 1
        elif name != "collection":
            XMLFilterBase.endElement(self, name)

    def endDocument(self):
        pass

    
