import threading
from fastapi import FastAPI, Form, Header, status
from fastapi.responses import JSONResponse
from bussines.token import generate_token, verify_token, store_request_logs
from bussines.user import authenticate

app = FastAPI()

@app.post("/api/auth")
def api_auth(username: str = Form(...), password: str = Form(...)):
    try: 
        user = authenticate(username, password)
        
        if user:
            if user.is_active: 
                if user.profile.generate_token:
                    token = generate_token(user)
                    status_code = status.HTTP_200_OK 
        
                    return JSONResponse(
                        status_code=status_code,
                        content={"status": "ok", "token": token}
                    )
                else:
                    status_code = status.HTTP_403_FORBIDDEN

                    return JSONResponse(
                        status_code=status_code,
                        content={"status": "fail", "message": "Usuário não liberado para solicitação de tokens"}
                    )
            else:
                status_code = status.HTTP_403_FORBIDDEN
                return JSONResponse(
                    status_code=status_code,
                    content={"status": "fail", "message": "Usuário ainda não está liberado! Aguarde liberação de um administrador."}
                )                

        status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse(
            status_code=status_code,
            content={"status": "fail", "message": "Credenciais inválidas"}
        )
    finally:
        threading.Thread(target=store_request_logs, args=(status_code,), daemon=True).start()

@app.get("/api/verify")
def api_verify(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        return  JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"valid": False, "reason": "Formato inválido"}
            )
    token = authorization.split(" ")[1]
    return verify_token(token)
