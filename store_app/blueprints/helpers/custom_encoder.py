import decimal
import datetime
from json import dumps


def sqlalchemy_enc(obj):
    """
    Custom encoder for encoding decimal and datetime objects to JSON per answer found
    at http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    :param obj: Object to encode
    :return: Object in JSON serializable format
    """
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, datetime.date):
        return obj.isoformat()


def simple_enc(key, values):
    """
    Pairs the given array of values with
    :param key: The key to associate the values with
    :param values: The values to put in a JSON array
    :return: the JSON key-value pair as a JSON string
    """
    try:
        return dumps({key: [v.dict() for v in values]}, default=sqlalchemy_enc)
    except:
        raise TypeError("Items must be dictionaries before encoding using this method")


def multi_enc(dictionary):
    """
    JSON encodes the given dictionary of key-value pairs
    :param dictionary: key-value pairs representing the data wishing to be JSON encoded
    :return: JSON string
    """
    newDict = {}
    try:
        for key, value in dictionary.iteritems():
            if isinstance(value, list):
                newDict.setdefault(key, [v.dict() for v in value if v is not None])
            elif value is None:
                newDict.setdefault(key)
            elif hasattr(value, 'dict'):
                newDict.setdefault(key, value.dict())
            else:
                newDict.setdefault(key, value)
        return dumps(newDict, default=sqlalchemy_enc)
    except Exception as e:
        print e
        raise e