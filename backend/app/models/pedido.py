from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    DateTime,
    Enum as SQLEnum,
    Numeric,
    String,
    func
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import EstadoPedido, enum_values

if TYPE_CHECKING:
    from app.models.detalle_pedido import DetallePedido
    from app.models.usuario import Usuario

class Pedido(Base):
    __tablename__ = 'pedidos'

    __table_args__= (
        CheckConstraint(
            "total >= 0", 
            name="ck_pedido_total_positivo"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    estado: Mapped[EstadoPedido] = mapped_column(
        SQLEnum(
            EstadoPedido,
            values_callable=enum_values,
            native_enum=False,
        ),
        default=EstadoPedido.PENDIENTE,
        nullable=False,
    )

    direccion_entregas: Mapped[str] = mapped_column(
        String (250),
        nullable=False
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(2, 10),
        default=0,
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column (
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="pedidos",
    )

    detalles: Mapped[list["DetallePedido"]] = relationship(
        "DetallePedido",
        back_populates="pedido",

        #Detalles depende del pedidos, si elimino pedido se eliminan sus detalles
        cascade="all, delete-orphan"
    )
    
