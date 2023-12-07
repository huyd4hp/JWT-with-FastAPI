from datetime import timedelta
from fastapi.responses import JSONResponse
from core.schemas.user import LoginField
from core.models.database import User, engine
from sqlalchemy.orm import sessionmaker
import jwt
from fastapi import status
from core.api.dependencies.security import checkPassword


class ReturnResponse:
    def HTTP_401_UNAUTHORIZED(message):
        return JSONResponse(
            content={
                "status": 401,
                "message": message,
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def HTTP_200_OK(message, data=None):
        if data == None:
            return JSONResponse(
                content={
                    "status": 200,
                    "message": message,
                },
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={
                    "status": 200,
                    "message": message,
                    "data": data,
                },
                status_code=status.HTTP_200_OK,
            )

    def HTTP_404_NOT_FOUND(message):
        return JSONResponse(
            content={
                "status": 404,
                "message": message,
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    def HTTP_403_FORBIDDEN(message):
        return JSONResponse(
            content={
                "status": 403,
                "message": message,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    def HTTP_400_BAD_REQUEST(message):
        return JSONResponse(
            content={
                "status": 400,
                "message": message,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def HTTP_201_CREATED(message):
        return JSONResponse(
            content={
                "status": 201,
                "message": message,
            },
            status_code=status.HTTP_201_CREATED,
        )


SECRET_KEY = "asfdh123as12312saf123@cmn12"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_user(form: LoginField):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        user = session.query(User).filter_by(username=form.username).first()
        if user and checkPassword(
            form.password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return user
    return None


def encodeUser(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decodeToken(token: str):
    user = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    return user
