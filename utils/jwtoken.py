import datetime

from jose import jwt

# todo use envirment varible here
# from env import JWT_SECRET_KEY


async def make_token(id: int, expdate: int):
    day = datetime.datetime.today() + datetime.timedelta(days=expdate)
    exp = int(datetime.datetime.timestamp(day))
    # todo                       replace env here  ↓
    token = jwt.encode({"id": id, "exp": exp}, "khalil")

    return token


async def check_token(token: str | bytes) -> bool | dict:
    try:
        isvalid = jwt.decode(token, "khalil")
        return isvalid
    except:
        return False


async def isAuthanticated(token: str | bytes):
    isauth = await check_token(token)
    if type(isauth) == dict:
        return True
    return False
