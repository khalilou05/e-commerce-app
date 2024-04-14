import datetime

from jose import jwt

from settings import jwt_exp_date_token, jwt_secret_key


async def make_token(id: int):
    day = datetime.datetime.today() + datetime.timedelta(days=jwt_exp_date_token)
    exp = int(datetime.datetime.timestamp(day))
    token = jwt.encode({"id": id, "exp": exp}, jwt_secret_key)

    return token


async def check_token(token: str | bytes) -> bool | dict:
    try:
        isvalid = jwt.decode(token, jwt_secret_key)
        return isvalid
    except:
        return False


async def isAuthanticated(token: str | bytes):
    isauth = await check_token(token)
    if type(isauth) == dict:
        return True
    return False
