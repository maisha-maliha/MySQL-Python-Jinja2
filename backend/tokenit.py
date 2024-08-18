import jwt
import datetime

# create token with user_id and user_name
def tokenit(user_id, user_name):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    payload = {
        "user_id": user_id,
        "user_name": user_name,
        "exp": expiration_time 
    }
    token = jwt.encode(payload,"HI-SECRET", algorithm='HS256')
    return token

# decode the token
def decodetokenn(token):
    payload = jwt.decode(token, "HI-SECRET",algorithms=['HS256'])
    return payload