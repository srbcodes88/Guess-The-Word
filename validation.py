SPECIALS = set('$%@*')

def validate_user(username, password):
    if len(username) < 5 or not username.isalnum():
        return False
    if len(password) < 5:
        return False
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in SPECIALS for c in password):
        return False
    return True
