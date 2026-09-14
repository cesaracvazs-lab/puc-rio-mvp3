from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Query, Session

from models import Paciente


def buscar_por_id(db: Session, paciente_id: int) -> Optional[Paciente]:
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()


def buscar_por_email(db: Session, email: str) -> Optional[Paciente]:
    return db.query(Paciente).filter(Paciente.email == email).first()


def listar(
    db: Session,
    nome: Optional[str],
    email: Optional[str],
    endereco: Optional[str],
    situacao: Optional[str],
    page: int,
    page_size: int,
    order_by: str,
    order_direction: str,
):
    consulta: Query = db.query(Paciente)

    if nome:
        consulta = consulta.filter(Paciente.nome.ilike(f"%{nome}%"))
    if email:
        consulta = consulta.filter(Paciente.email.ilike(f"%{email}%"))
    if endereco:
        consulta = consulta.filter(
            or_(
                Paciente.logradouro.ilike(f"%{endereco}%"),
                Paciente.bairro.ilike(f"%{endereco}%"),
                Paciente.cidade.ilike(f"%{endereco}%"),
                Paciente.estado.ilike(f"%{endereco}%"),
            )
        )
    if situacao:
        consulta = consulta.filter(Paciente.situacao.ilike(f"%{situacao}%"))

    coluna_ordenacao = getattr(Paciente, order_by)
    consulta = consulta.order_by(
        coluna_ordenacao.desc() if order_direction == "desc" else coluna_ordenacao.asc()
    )

    total = consulta.count()
    pacientes = consulta.offset((page - 1) * page_size).limit(page_size).all()
    return pacientes, total


def salvar(db: Session, paciente: Paciente) -> Paciente:
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


def excluir(db: Session, paciente: Paciente) -> None:
    db.delete(paciente)
    db.commit()
