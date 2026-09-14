from sqlalchemy import Boolean, Column, Integer, String, Text

from database import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=True)
    cep = Column(String(15), nullable=False)
    logradouro = Column(String(200), nullable=False)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    ultima_visita = Column(String(10), nullable=True)
    situacao = Column(String(30), default="Ativo", nullable=False)
    observacoes = Column(Text, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
