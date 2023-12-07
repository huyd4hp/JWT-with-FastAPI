from fastapi import APIRouter
from fastapi.responses import JSONResponse
from core.schemas.user import UserCreate, UserView
from core.models.database import engine
from core.api.endpoints.auth import ReturnResponse
from sqlalchemy.orm import sessionmaker
from core.models.database import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, Request
from core.api.dependencies.security import hash_password, checkPassword
from dotenv import load_dotenv
import os
from core.api.endpoints.auth import decodeToken

load_dotenv()
SALT = os.getenv("SALT")

router = APIRouter()


@router.get("/users/", tags=["users"], status_code=status.HTTP_200_OK)
async def all_users(request: Request):
    accessToken = request.cookies.get("accessToken")
    if accessToken:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            users = session.query(User).all()
            lstUser = []
            for user in users:
                dUser = dict()
                dUser["username"] = user.username
                dUser["password"] = user.password
                if user.email != None:
                    dUser["email"] = user.email
                dUser["role"] = str(user.role).split(".")[1]
                lstUser.append(dUser)
            return ReturnResponse.HTTP_200_OK(
                message="successfully",
                data={
                    "count": len(users),
                    "users": lstUser,
                },
            )

    else:
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")


@router.get("/users/{user_id}", tags=["user_info"])
async def user_info(user_id, request: Request):
    accessToken = request.cookies.get("accessToken")
    if accessToken:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                userview = UserView(
                    username=user.username,
                    password=user.password,
                    role=user.role,
                )
                return ReturnResponse.HTTP_200_OK(
                    message="successfull",
                    data=userview.json(),
                )

            else:
                return ReturnResponse.HTTP_404_NOT_FOUND("User not found")

    else:
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")


@router.post("/users/", tags=["new user"], status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, request: Request):
    accessToken = request.cookies.get("accessToken")
    if accessToken:
        user = decodeToken(accessToken)
        if user["role"] == "Customer":
            return ReturnResponse.HTTP_403_FORBIDDEN("Không đủ quyền hạn")
        else:
            Session = sessionmaker(bind=engine)
            with Session() as session:
                newUser = User(
                    username=user.username,
                    password=hash_password(user.password, SALT),
                    role=user.role,
                )
                session.add(newUser)
                try:
                    session.commit()
                    return ReturnResponse.HTTP_201_CREATED("Successfully")

                except SQLAlchemyError as error:
                    return ReturnResponse.HTTP_400_BAD_REQUEST(
                        "Kiểm tra thông tin đã nhập"
                    )
                finally:
                    session.close()
    else:
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")


@router.delete("/users/{user_id}", tags=["delete user"])
async def del_user(user_id, request: Request):
    accessToken = request.cookies.get("accessToken")
    if accessToken:
        user = decodeToken(accessToken)
        if user["role"] != "Customer":
            Session = sessionmaker(bind=engine)
            with Session() as session:
                user = session.query(User).filter_by(id=user_id).first()
                if user:
                    session.delete(user)
                    session.commit()
                    return ReturnResponse.HTTP_200_OK("User deleted successfully")
                else:
                    return ReturnResponse.HTTP_404_NOT_FOUND("User not found")
        else:
            return ReturnResponse.HTTP_403_FORBIDDEN("Không đủ quyền hạn")
    else:
        return ReturnResponse.HTTP_401_UNAUTHORIZED("Đăng nhập sử dụng dịch vụ")
