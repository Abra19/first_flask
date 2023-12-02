def validate(user):
    errors = {}
    if not user:
        return {}
    if len(user.get('nickname')) <= 4:
        errors['nickname'] = "Nickname must be grater than 4 characters"
    if not user.get('email'):
        errors['email'] = "Can't be blank"
    return errors
