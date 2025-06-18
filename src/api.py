from fastapi import FastAPI, Form, Header, status
from fastapi.responses import JSONResponse
from bussines.token import generate_token, verify_token
from bussines.user import authenticate
from bussines.profile import get_profiles

app = FastAPI()

@app.post("/api/auth")
def api_auth(username: str = Form(...), password: str = Form(...)):
    user = authenticate(username, password)
    if user:
        profile = get_profiles(user.profile_id)

        if profile.generate_token:
            token = generate_token(user)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "ok", "token": token}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": "fail", "message": "Usuário não liberdo para solicitação de tokens"}
            )

    return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": "fail", "message": "Credenciais inválidas"}
            )

@app.get("/api/verify")
def api_verify(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        return  JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"valid": False, "reason": "Formato inválido"}
            )
    token = authorization.split(" ")[1]
    return verify_token(token)
