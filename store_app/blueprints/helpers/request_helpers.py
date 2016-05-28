from string import split
ALLOWED_EXT = ['jpg', 'JPG', 'png']


def convertToInt(num):
    try:
        num = int(num)
        if num > 2145483647 or num < 0:
            num = 0
    except:
        num = 0
    return num

def allowed_filename(filename):
    return filename.split('.', 1)[1] in ALLOWED_EXT

def isNullOrUndefined(s):
    return s == 'null' or s == 'undefined' or s is None