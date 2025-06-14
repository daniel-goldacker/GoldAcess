from fastapi import FastAPI, Form, Header
from auth import authenticate, generate_token, verify_token

app = FastAPI()

@app.post("/api/auth")
def api_auth(username: str = Form(...), password: str = Form(...)):
    user = authenticate(username, password)
    if user:
        token = generate_token(user)
        return {"status": "ok", "token": token}
    return {"status": "fail", "message": "Credenciais inválidas"}

@app.get("/api/verify")
def api_verify(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        return {"valid": False, "reason": "Formato inválido"}
    token = authorization.split(" ")[1]
    return verify_token(token)
