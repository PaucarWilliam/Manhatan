from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.categoria import Categoria
    from app.models.detalle_pedido import DetallePedido

class Producto(Base):
    __tablename__ = "productos"

    __table_args__ = (
        CheckConstraint(
            "precio > 0",
            name="ck_producto_precio_positivo",
        ),
        CheckConstraint(
            "stock >= 0",
            name="ck_producto_stock_no_negativo",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    precio: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    disponible: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id"),
        nullable=False,
    )

    categoria: Mapped["Categoria"] = relationship(
        "Categoria",
        #Mismo nombre referencial que en categoria.py
        back_populates="productos",
    )

    detalles_pedido: Mapped[list["DetallePedido"]] = relationship(
        "DetallePedido",
        back_populates="producto",
    )