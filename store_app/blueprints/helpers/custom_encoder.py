import decimal, datetime


def sqlencoder(obj):
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
