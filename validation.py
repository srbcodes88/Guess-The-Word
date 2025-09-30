SPECIALS = set('$%@*')

def validate_user(username, password):
    if len(username) < 5 or not username.isalnum():
        return False, "Username must be at least 5 alphanumeric characters"
    if len(password) < 5:
        return False, "Password must be at least 5 characters"
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    if not any(c in SPECIALS for c in password):
        return False, f"Password must contain at least one special character from {''.join(SPECIALS)}"
    return True, "Valid"

