"""
FastAPI で「FENと正解手順（SAN）」をJSONで返すAPI。

◆ 使い方
1) 依存関係をインストール
   pip install fastapi uvicorn
   # or: pip install "fastapi[standard]"

2) 起動
   uvicorn main:app --reload --port 8000

3) エンドポイント
   GET  /health          -> 稼働確認
   GET  /puzzle          -> 固定の問題(JSON)
   POST /echo            -> リクエストで送った {fen, moves[]} をそのまま返す
   GET  /docs            -> Swagger UI

必要に応じて STATIC_PUZZLE を差し替えてください。
"""
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware


class Puzzle(BaseModel):
    fen: str
    moves: List[str]  # SAN の配列。例: ["Rxd7", "Kxd7", ...]


app = FastAPI(title="Chess Puzzle API", version="1.0.0")

# CORS (フロントエンドから叩けるように全許可。必要に応じて制限してください)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ユーザー指定の固定問題（必要なら差し替え/複数管理OK）
STATIC_PUZZLE = Puzzle(
    fen="r3k2r/pb1p1pp1/4p3/2Q1P2p/6P1/1B3q1P/P4P1R/3R2K1 w kq - 0 22",
    moves=["Rxd7", "Kxd7", "Ba4", "Bc6", "Qd6", "Qc8", "Bc6"],
)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/puzzle", response_model=Puzzle)
def get_puzzle():
    """固定のチェス問題を返す"""
    return STATIC_PUZZLE


@app.post("/echo", response_model=Puzzle)
def echo_puzzle(p: Puzzle):
    """受け取った {fen, moves[]} をそのまま返す（動作確認・配線テスト用）"""
    return p


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
