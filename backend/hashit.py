import bcrypt

# hash password
def hashpassword(password):
    hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashpass

# validate password
def comparehashedpassword(password, hashedpass):
    check = bcrypt.checkpw(password.encode('utf-8'), hashedpass.encode('utf-8'))
    return check