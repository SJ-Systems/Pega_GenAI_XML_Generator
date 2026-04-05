from fastapi import FastAPI
from pydantic import BaseModel

from app.generator import generate_xml
from app.retriever import retrieve
from app.classifier import detect_rule_type

app = FastAPI()

class RequestModel(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/generate-xml")
def generate(data: RequestModel):
    prompt = data.prompt

    rule_type = detect_rule_type(prompt)
    context = retrieve(prompt)

    xml = generate_xml(prompt, context, rule_type)

    return {"xml": xml}
import os

port = int(os.environ.get("PORT", 10000))
