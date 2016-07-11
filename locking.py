keys = 1


def get_key():
    global keys
    while keys < 1:
        pass
    keys -= 1
    return True


def unlock():
    global keys
    keys += 1
