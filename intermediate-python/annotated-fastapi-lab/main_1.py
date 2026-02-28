from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

def get_settings():
    return {"app_name": "Annotated Lab", "version": "1"}

@app.get("/settings")
def read_settings(settings: Annotated[dict, Depends(get_settings)]):
    return settings