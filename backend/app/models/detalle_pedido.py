from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.pedido import Pedido
    from app.models.producto import Producto

class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    __table_args__ = (
        CheckConstraint(
            "cantidad > 0",
            name="ck_detalle_cantidad_positiva",
        ),
        CheckConstraint(
            "precio_unitario > 0",
            name="ck_detalle_precio_positivo",
        ),
        CheckConstraint(
            "subtotal > 0",
            name="ck_detalle_subtotal_positivo",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False,
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False,
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    pedido: Mapped["Pedido"] = relationship(
        "Pedido",
        back_populates="detalles",
    )

    producto: Mapped["Producto"] = relationship(
        "Producto",
        back_populates="detalles_pedido",
    )