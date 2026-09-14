from fastapi import FastAPI

from database import Base, engine
from endpoint.paciente_endpoint import router as paciente_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Controle de Pacientes",
    version="1.0.0",
    description="API principal para cadastro, busca, filtros, paginação e integração com ViaCEP.",
)


@app.get("/")
def home():
    return {"status": "API principal do Sistema de Controle de Pacientes funcionando."}


app.include_router(paciente_router)
