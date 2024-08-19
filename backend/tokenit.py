import jwt
import datetime
import config

# create token with user_id and user_name
def tokenit(user_id, user_name):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    payload = {
        "user_id": user_id,
        "user_name": user_name,
        "exp": expiration_time 
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token

# decode the token
def decodetokenn(token):
    payload = jwt.decode(token, config.SECRET_KEY ,algorithms=['HS256'])
    return payload