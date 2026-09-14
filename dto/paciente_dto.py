from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PacienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    email: str = Field(..., min_length=3, max_length=150)
    telefone: Optional[str] = Field(default=None, max_length=20)
    cep: str = Field(..., min_length=8, max_length=15)
    logradouro: Optional[str] = Field(default=None, max_length=200)
    numero: Optional[str] = Field(default=None, max_length=20)
    complemento: Optional[str] = Field(default=None, max_length=100)
    bairro: Optional[str] = Field(default=None, max_length=100)
    cidade: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, max_length=2)
    ultima_visita: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    situacao: str = Field(default="Ativo", max_length=30)
    observacoes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=150)
    email: Optional[str] = Field(default=None, min_length=3, max_length=150)
    telefone: Optional[str] = Field(default=None, max_length=20)
    cep: Optional[str] = Field(default=None, min_length=8, max_length=15)
    logradouro: Optional[str] = Field(default=None, max_length=200)
    numero: Optional[str] = Field(default=None, max_length=20)
    complemento: Optional[str] = Field(default=None, max_length=100)
    bairro: Optional[str] = Field(default=None, max_length=100)
    cidade: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, max_length=2)
    ultima_visita: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    situacao: Optional[str] = Field(default=None, max_length=30)
    observacoes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PacienteResponse(PacienteBase):
    id: int
    ativo: bool = True


class PacienteListResponse(BaseModel):
    items: List[PacienteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
