from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import RolUsuario, enum_values

if TYPE_CHECKING:
    from app.models.pedido import Pedido

class Usuario(Base):
    __tablename__='usuarios'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    password_hashed: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    rol: Mapped[RolUsuario] = mapped_column(
        SQLEnum(
            RolUsuario,
            values_callable=enum_values,
            native_enum=False
        ),
        default=RolUsuario.CLIENTE,
        nullable=False
    )

    activo:Mapped[Boolean] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    pedidos: Mapped[list["Pedido"]] = relationship(
        "Pedido",
        back_populates="usuario"
    )
