# Secretaria de Saúde DF - Sistema de Agendamento

Aplicativo web para agendamento de consultas médicas, desenvolvido para a Secretaria de Saúde do Distrito Federal. O sistema utiliza **HTML/JS puro no frontend** e **Flask com PostgreSQL no backend**.

---

## 🎯 Funcionalidades

- Cadastro de pacientes e médicos
- Login com autenticação JWT
- Agendamento de consultas com data e hora
- Listagem de agendamentos por paciente e médico
- Cadastro de especialidades e regiões administrativas

---

## 🧱 Tecnologias Utilizadas

### Frontend (Web)
- HTML5 + CSS3 + JavaScript puro
- Forms dinâmicos com `fetch`
- Armazenamento local com `localStorage`

### Backend (API Flask)
- Python 3.11+ com Flask
- Flask-JWT-Extended para autenticação
- Flask-SQLAlchemy + PostgreSQL
- Flask-CORS habilitado
- Estrutura modular com Blueprints e Services

---

## ▶️ Como executar o projeto localmente

### 1. Clonar o repositório
```bash
https://github.com/seu-usuario/secretaria-saude-df.git
cd secretaria-saude-df
```

### 2. Backend - API Flask
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Criar banco e rodar aplicação
export DATABASE_URL=postgresql://usuario:senha@localhost/saude_df
export SECRET_KEY=sua_chave
export JWT_SECRET_KEY=sua_chave_jwt
python run.py
```

### 3. Frontend - HTML/JS
Use a extensão Live Server (VSCode) ou:
```bash
cd frontend
python -m http.server
```
Acesse: `http://127.0.0.1:5500`

---

## 🛠 Estrutura do Projeto
```
backend/
├── app/
│   ├── models/            # Modelos SQLAlchemy
│   ├── routes/            # Blueprints (rotas)
│   ├── services/          # Lógicas de negócio
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
├── run.py
├── requirements.txt

frontend/
├── index.html
├── LoginPaciente.html
├── CadastroPaciente.html
├── agendamento.html
├── consultaMedica.html
└── style.css
```

---

## 👥 Perfis de Usuário

### Paciente
- Cadastro com CPF, e-mail e senha
- Login e agendamento de consultas
- Visualização de agendamentos futuros

### Médico
- Cadastro com nome, CRM, especialidade e região
- Login e visualização de consultas marcadas

### Admin (via API/postman)
- Cadastro de especialidades e regiões administrativas

---

## ⚖️ LGPD
- Os dados são armazenados de forma segura com autenticação JWT
- Apenas as informações necessárias são coletadas

---

## 📫 Suporte
- Email: example@df.gov.br
- Telefone: (61) 99999 - 0000

---

**Secretaria de Saúde do Distrito Federal**
*Sistema em conformidade com a LGPD*
