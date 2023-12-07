from pydantic import BaseModel


class UserView(BaseModel):
    username: str
    password: str
    email: str = None
    role: str

    def json(self):
        if self.email == None:
            return {
                "username": self.username,
                "password": self.password,
                "role": self.role,
            }
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role,
        }


class UserCreate(BaseModel):
    username: str
    password: str
    role: str

    def json(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }


class LoginField(BaseModel):
    username: str
    password: str
