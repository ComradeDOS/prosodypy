from twisted.words.xish.xmlstream import XmlStream

class FakeStream(XmlStream):
    def __init__(self, stream_xmlns='jabber:client', *args, **kwargs):
        XmlStream.__init__(self, *args, **kwargs)
        self.connectionMade()
        self.dataReceived('<stream xmlns="%s">' % (stream_xmlns,))
        self.resulted_element = None

    def dispatch(self, element, event=None):
        if event is not None:
            return
        self.resulted_element = element

xmlstream = FakeStream()

def parse_string(stanza):
    xmlstream.dataReceived(stanza)
    result = xmlstream.resulted_element
    assert result is not None
    xmlstream.resulted_element = None
    return result

