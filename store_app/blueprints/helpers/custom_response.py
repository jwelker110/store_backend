from flask import Response
from json import dumps
from custom_encoder import sqlencoder


class Resp(Response):

    def __init__(self, response=None, status=200, headers=None,
                 mimetype="application/json", content_type="application/json; UTF-8"):
        super(Response, self).__init__(response=response,
                                       status=status,
                                       headers=headers,
                                       mimetype=mimetype,
                                       content_type=content_type)


def simple_enc(key, values):
    """
    Pairs the given array of values with
    :param key: The key to associate the values with
    :param values: The values to put in a JSON array
    :return: the JSON key-value pair as a JSON string
    """
    try:
        return dumps({key: [v.dict() for v in values]}, default=sqlencoder)
    except:
        raise TypeError("Items must be dictionaries before encoding using this method")


def multi_enc(dictionary):
    """
    JSON encodes the given dictionary of key-value pairs
    :param dictionary: key-value pairs representing the data wishing to be JSON encoded
    :return: JSON string
    """
    keys = dictionary.keys()
    newDict = {}
    try:
        for k in keys:
            values = []
            for v in dictionary[k]:
                values.append(v.dict())
            newDict.setdefault(k, values)
        return dumps(newDict, default=sqlencoder)
    except Exception as e:
        print e
        raise TypeError("Items must be dictionaries before encoding using this method")
