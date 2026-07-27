from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.detalle_pedido import DetallePedido

class DetallePedidoRepository:
    def crear(
            self,
            db:Session,
            detalle: DetallePedido,
    ) -> DetallePedido:
        db.add(detalle)
        db.flush()
        return detalle

    def obtener_por_id(
            self,
            db:Session,
            detalle_id:int,
    ) -> DetallePedido | None:
        return db.get(
            DetallePedido,
            detalle_id,
        )

    def listar(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100 # tien un limite de listado eso debemos corregir despues
    ) -> list[DetallePedido]:
        consulta = (
            select(DetallePedido)
            .order_by(DetallePedido.id.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(
            db.scalars(consulta).all()
        )

    def listar_por_pedido(
            self,
            db:Session,
            pedido_id: int,
    ) -> list[DetallePedido]:
        consulta = (
            select(DetallePedido)
            .where(
                DetallePedido.pedido_id == pedido_id
            )
            .order_by(DetallePedido.id)
        )

        return list(
            db.scalars(consulta).all()
        )

    def actualizar(
        self,
        db: Session,
        detalle: DetallePedido,
    ) -> DetallePedido:
        db.flush()

        return detalle

    def eliminar(
        self,
        db: Session,
        detalle: DetallePedido,
    ) -> None:
        db.delete(detalle)
        db.flush()

    def calcular_total_pedido(
        self,
        db: Session,
        pedido_id: int,
    ) -> Decimal:
        consulta = (
            select(
                func.coalesce(
                    func.sum(DetallePedido.subtotal),
                    0,
                )
            )
            .where(
                DetallePedido.pedido_id == pedido_id
            )
        )

        total = db.scalar(consulta)

        return Decimal(str(total))


detalle_pedido_repository = DetallePedidoRepository()