import streamlit as st

def api_docs():
    st.title("📘 Documentação API")

    st.markdown("""
    Esta API fornece endpoints para autenticação e verificação de tokens usando JWT.
    Você pode integrá-la com seus sistemas para garantir acesso seguro aos seus serviços.

    ---

    ## 🔐 `POST /api/auth`
    Endpoint para autenticar um usuário e gerar um token JWT.

    ### Parâmetros (form-data):
    - `username`: *string* – Nome de usuário
    - `password`: *string* – Senha do usuário

    ### Respostas:
    - `200 OK`:
        ```json
        {
            "status": "ok",
            "token": "<jwt_token>"
        }
        ```
    - `401 UNAUTHORIZED`:
        ```json
        {
            "status": "fail",
            "message": "Credenciais inválidas"
        }
        ```

    ### Exemplo (cURL):
    ```bash
    curl -X POST http://localhost:8000/api/auth \\
      -F "username=admin" \\
      -F "password=1234"
    ```

    ### Exemplo (Python):
    ```python
    import requests

    response = requests.post("http://localhost:8000/api/auth", data={
        "username": "admin",
        "password": "1234"
    })

    print(response.json())
    ```

    ---

    ## ✅ `GET /api/verify`
    Verifica se um token JWT enviado no cabeçalho `Authorization` é válido.

    ### Cabeçalho:
    - `Authorization: Bearer <token>`

    ### Respostas:
    - `200 OK`:
        ```json
        {
            "valid": true,
            "user": { ... }
        }
        ```
    - `401 UNAUTHORIZED`:
        ```json
        {
            "valid": false,
            "reason": "Formato inválido"
        }
        ```

    ### Exemplo (cURL):
    ```bash
    curl -X GET http://localhost:8000/api/verify \\
      -H "Authorization: Bearer <seu_token_aqui>"
    ```

    ---

    👨‍💻 **Dica:** Use o token retornado do `/api/auth` como cabeçalho `Authorization` em chamadas protegidas.

    """)

