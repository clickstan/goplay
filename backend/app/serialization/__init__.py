"""Defines a class named 'serialization_method' that points to the
serialization class configured in config.yaml as protocol['serialization']"""

__all__ = ['serialization_method']

import json, yaml

import pyamf
from pyamf.util import BufferedByteStream


_config = {}
with open('config.yaml', 'r') as stream:
    _config = yaml.load(stream)['protocol']
    
_serialization_method_name = _config.get('serialization')


class JSON:
    """This serialization method requires '\0' char as message end marker"""
    
    @staticmethod
    def loads(data):
        """returns a list of messages"""
        result = []
        for message in data.split('\0'):
            if message != '':
                try: message = json.loads(message)
                except:
                    print 'not json:', message
                    return
                result.append(message)
        return result
    
    @staticmethod
    def dumps(data):
        """returns a serialized message"""
        return json.dumps(data)+'\0'
    
    
class AMF3:
    
    @staticmethod
    def loads(data):
        """returns a list of messages"""
        stream = BufferedByteStream(data)
        result = list(pyamf.decode(stream=stream, encoding=3))
        stream.close()
        return result
    
    @staticmethod
    def dumps(data):
        """returns a serialized message"""
        stream = pyamf.encode(data, encoding=3)
        result = stream.getvalue()
        stream.close()
        return result
    
    
serialization_method = {'json' : JSON,
                        'amf3' : AMF3,
                        }[_serialization_method_name]