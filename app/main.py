from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import build_index, retrieve
from app.generator import generate_xml

app = FastAPI()

class RequestModel(BaseModel):
    prompt: str

@app.on_event("startup")
def startup():
    build_index()

@app.get("/")
def home():
    return {"status": "RAG API running"}

@app.post("/generate-xml")
def generate(data: RequestModel):
    context = retrieve(data.prompt)
    xml = generate_xml(data.prompt, context)

    return {
        "xml": xml
    }
