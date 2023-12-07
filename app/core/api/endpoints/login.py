from fastapi import APIRouter, Request, status
from core.api.endpoints.auth import ReturnResponse, encodeUser, verify_user, decodeToken
from core.api.endpoints.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from core.schemas.user import LoginField
from datetime import timedelta
from fastapi.responses import Response


router = APIRouter()


@router.get("/", tags=["root"], status_code=status.HTTP_200_OK)
def welcome(request: Request, response: Response):
    try:
        accessToken = request.cookies.get("accessToken")
        if accessToken:
            user = decodeToken(accessToken)
            return ReturnResponse.HTTP_200_OK(f"Welcome! {user['username']}")
        else:
            return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")
    except:
        response.delete_cookie("accessToken")
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")


@router.post("/login/", tags=["login"], status_code=status.HTTP_200_OK)
def login(form: LoginField, response: Response):
    user = verify_user(form)
    if user:
        accessToken = encodeUser(
            data={
                "username": user.username,
                "role": str(user.role).split(".")[1],
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        print(accessToken)
        response.set_cookie(
            key="accessToken",
            value=accessToken,
            httponly=True,
        )
        return ReturnResponse.HTTP_200_OK("Đăng nhập thành công")

    else:
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Sai thông tin đăng nhập")


@router.get("/logout", tags=["logout"], status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response):
    accessToken = request.cookies.get("accessToken")
    if accessToken:
        response.delete_cookie(key="accessToken")
        return ReturnResponse.HTTP_200_OK("Đăng nhập để tiếp tục sử dụng")
    else:
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")
