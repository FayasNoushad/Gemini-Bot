from vars import AUTH, AUTH_USERS

def auth(id):
    if AUTH:
        if id in AUTH_USERS:
            return True
        else:
            return False
    else:
        return True
