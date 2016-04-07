
def convertToInt(num):
    try:
        num = int(num)
        if num > 2145483647 or num < 0:
            num = 0
    except:
        num = 0
    return num
