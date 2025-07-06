# GoldAcess

**GoldAcess** é um sistema de autenticação, autorização e gestão de usuários com interface web, desenvolvido em Python. Ele permite controlar acessos com base em perfis (roles), gerenciar tokens JWT e visualizar informações analíticas sobre uso e segurança.

## 🚀 Funcionalidades

- 🔐 Login com autenticação JWT  
- 👤 Cadastro e gerenciamento de usuários  
- 🛡️ Perfis e permissões de acesso  
- 📊 Painel analítico com informações de uso e status HTTP  
- 🧾 Documentação da API embutida  
- 📁 Interface web com Streamlit  

## 🧰 Tecnologias Usadas

- Python 3.10+  
- Streamlit (interface frontend)  
- SQLite ou PostgreSQL (via SQLAlchemy)  
- JWT (JSON Web Token)  
- `requests`, `pydantic`, `sqlalchemy`, `streamlit-authenticator`  

## ▶️ Como Executar o Sistema

1. Clone o projeto:
   ```bash
   git clone https://github.com/seu-usuario/GoldAcess.git
   cd GoldAcess
   cd src
   ```

2. Instale as dependências:
   ```bash
    pip install -r requirements.txt
    ```
3. Execute a aplicação:

   ```bash
    streamlit run main.py
    ```

## ▶️ Como Executar a API

Para iniciar a API em modo de desenvolvimento com recarga automática, execute o seguinte comando no terminal:

```bash
cd GoldAcess
cd src
uvicorn api:app --reload --port 8000
```

## 🔧 Variáveis de Ambiente

Essas variáveis são utilizadas para configurar autenticação, perfis e segurança dos tokens JWT.

| Variável                                       | Descrição                                                                 |
|-----------------------------------------------|---------------------------------------------------------------------------|
| `NAME_ADMIN`                                   | Nome de usuário do administrador padrão (criado automaticamente).        |
| `PASSWORD_ADMIN`                               | Senha do administrador padrão.                                           |
| `TOKEN_EXP_MINUTES_ADMIN`                      | Tempo de expiração do token do admin, em minutos (`0` = sem expiração).  |
| `PROFILE_PADRAO`                               | Nome do perfil padrão atribuído a novos usuários.                        |
| `PROFILE_SISTEMA`                              | Perfil interno do sistema para operações administrativas.                |
| `TOKEN_EXP_MINUTES_AUTOMATIC_USER_CREATION`    | Expiração do token de usuários criados automaticamente.                  |
| `SECRET_KEY`                                   | Chave secreta usada para assinar/verificar tokens JWT.                   |
| `ALGORITHMS_CRYPTOGRAPHY`                      | Algoritmo de criptografia usado nos tokens JWT (ex: `HS256`).            |

## 🧪 Exemplo de `.env`

```env
NAME_ADMIN=admin
PASSWORD_ADMIN=admin
TOKEN_EXP_MINUTES_ADMIN=0

PROFILE_PADRAO=Padrão
PROFILE_SISTEMA=Sistema
TOKEN_EXP_MINUTES_AUTOMATIC_USER_CREATION=0

SECRET_KEY=d7jXZGnfWknDAj0RA1L7v7sOxUx2qU0omq7dBZURPz1Vo1Twf1
ALGORITHMS_CRYPTOGRAPHY=HS256
```

## 🔒 Segurança
Geração e expiração de tokens JWT

Autenticação via API

Controle de acesso baseado em perfis e permissões

## 📈 Análises
Gráficos de uso de tokens

Análise de status HTTP das requisições