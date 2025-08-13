# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 開発中は "*" でもOK。本番はフロントのドメインだけに絞る。
# 例: ["https://your-frontend.onrender.com", "http://localhost:3000"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"ok": True, "msg": "My name is donta. I am chess player."}

@app.get("/ping")
def ping():
    return {"pong": True}
