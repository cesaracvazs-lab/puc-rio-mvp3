from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from dto.paciente_dto import PacienteCreate, PacienteListResponse, PacienteResponse, PacienteUpdate
from service import paciente_service

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("", response_model=PacienteListResponse)
def listar_pacientes(
    nome: Optional[str] = Query(default=None),
    email: Optional[str] = Query(default=None),
    endereco: Optional[str] = Query(default=None),
    situacao: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    order_by: str = Query(default="nome", pattern="^(nome|ultima_visita)$"),
    order_direction: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paciente_service.listar_pacientes(
        db,
        nome=nome,
        email=email,
        endereco=endereco,
        situacao=situacao,
        page=page,
        page_size=page_size,
        order_by=order_by,
        order_direction=order_direction,
    )


@router.post("", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    return paciente_service.criar_paciente(db, paciente)


@router.get("/{paciente_id}", response_model=PacienteResponse)
def buscar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return paciente_service.obter_paciente(db, paciente_id)


@router.put("/{paciente_id}", response_model=PacienteResponse)
def atualizar_paciente(
    paciente_id: int,
    paciente: PacienteUpdate,
    db: Session = Depends(get_db),
):
    return paciente_service.atualizar_paciente(db, paciente_id, paciente)


@router.delete("/{paciente_id}")
def excluir_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente_service.excluir_paciente(db, paciente_id)
    return {"message": "Paciente removido com sucesso."}
