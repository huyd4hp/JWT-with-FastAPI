from fastapi import FastAPI
from core.api.endpoints.users import router as UserRouter
from core.api.endpoints.login import router as LoginRouter

import uvicorn


from core.models.database import initialDatabase


app = FastAPI(title="Auth User with JWT")
app.include_router(UserRouter)
app.include_router(LoginRouter)
if __name__ == "__main__":
    initialDatabase()
    uvicorn.run(app, host="localhost", port=8080)
