from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"ok": True, "msg": "hello from Render"}
