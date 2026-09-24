from datetime import date
from typing import Optional

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from dao import paciente_dao
from dto.paciente_dto import PacienteCreate, PacienteUpdate
from models import Paciente
from service.alerta_retorno_client import calcular_retorno


def buscar_endereco_por_cep(cep: str) -> dict:
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido. Informe um valor com 8 dígitos.")

    try:
        resposta = requests.get(
            f"https://viacep.com.br/ws/{cep_limpo}/json/",
            timeout=10,
        )
        resposta.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="Falha ao consultar o serviço ViaCEP.") from exc

    dados = resposta.json()
    if "erro" in dados:
        raise HTTPException(status_code=404, detail="CEP não encontrado na API do ViaCEP.")
    return dados


def preencher_endereco(paciente_schema, dados_cep: dict):
    for campo, campo_cep in {
        "logradouro": "logradouro",
        "bairro": "bairro",
        "cidade": "localidade",
        "estado": "uf",
    }.items():
        if not getattr(paciente_schema, campo):
            setattr(paciente_schema, campo, dados_cep.get(campo_cep) or "")
    return paciente_schema


def listar_pacientes(db: Session, **filtros):
    pacientes, total = paciente_dao.listar(db, **filtros)
    page_size = filtros["page_size"]
    return {
        "items": pacientes,
        "total": total,
        "page": filtros["page"],
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total else 0,
    }


def criar_paciente(db: Session, paciente_schema: PacienteCreate) -> Paciente:
    if paciente_dao.buscar_por_email(db, paciente_schema.email):
        raise HTTPException(status_code=400, detail="Já existe um paciente cadastrado com este e-mail.")

    dados_cep = buscar_endereco_por_cep(paciente_schema.cep)
    paciente_schema = preencher_endereco(paciente_schema, dados_cep)
    dados_paciente = paciente_schema.model_dump()
    dados_paciente["cep"] = dados_cep.get("cep") or paciente_schema.cep
    paciente = Paciente(**dados_paciente)
    paciente = paciente_dao.salvar(db, paciente)

    if paciente.ultima_visita:
        calcular_retorno(paciente.id, date.fromisoformat(paciente.ultima_visita), paciente.situacao)

    return paciente


def atualizar_paciente(db: Session, paciente_id: int, paciente_schema: PacienteUpdate) -> Paciente:
    paciente = paciente_dao.buscar_por_id(db, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    dados = paciente_schema.model_dump(exclude_unset=True)
    if "email" in dados and dados["email"] != paciente.email:
        paciente_com_email = paciente_dao.buscar_por_email(db, dados["email"])
        if paciente_com_email and paciente_com_email.id != paciente_id:
            raise HTTPException(status_code=400, detail="Já existe um paciente cadastrado com este e-mail.")

    if "cep" in dados:
        dados_cep = buscar_endereco_por_cep(dados["cep"])
        paciente_schema = preencher_endereco(paciente_schema, dados_cep)
        dados.update({
            "cep": dados_cep.get("cep") or dados["cep"],
            "logradouro": paciente_schema.logradouro,
            "bairro": paciente_schema.bairro,
            "cidade": paciente_schema.cidade,
            "estado": paciente_schema.estado,
        })

    for campo, valor in dados.items():
        if valor is not None:
            setattr(paciente, campo, valor)

    paciente = paciente_dao.salvar(db, paciente)

    if paciente.ultima_visita and ("ultima_visita" in dados or "situacao" in dados):
        calcular_retorno(paciente.id, date.fromisoformat(paciente.ultima_visita), paciente.situacao)

    return paciente


def obter_paciente(db: Session, paciente_id: int) -> Paciente:
    paciente = paciente_dao.buscar_por_id(db, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return paciente


def excluir_paciente(db: Session, paciente_id: int) -> None:
    paciente = obter_paciente(db, paciente_id)
    paciente_dao.excluir(db, paciente)
