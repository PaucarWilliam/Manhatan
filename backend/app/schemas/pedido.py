from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoPedido


class PedidoCreate(BaseModel):
    usuario_id: int = Field(
        gt=0,
    )

    direccion_entregas: str = Field(
        min_length=5,
        max_length=250,
    )


class PedidoDireccionUpdate(BaseModel):
    direccion_entregas: str = Field(
        min_length=5,
        max_length=250,
    )


class PedidoEstadoUpdate(BaseModel):
    estado: EstadoPedido


class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    estado: EstadoPedido
    direccion_entregas: str
    total: Decimal
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )