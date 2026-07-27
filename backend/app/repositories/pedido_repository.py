from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pedido import Pedido


class PedidoRepository:

    def crear(
        self,
        db: Session,
        pedido: Pedido,
    ) -> Pedido:
        db.add(pedido)
        db.flush()

        return pedido

    def obtener_por_id(
        self,
        db: Session,
        pedido_id: int,
    ) -> Pedido | None:
        return db.get(
            Pedido,
            pedido_id,
        )

    def listar(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Pedido]:
        consulta = (
            select(Pedido)
            .order_by(Pedido.fecha_creacion.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(
            db.scalars(consulta).all()
        )

    def listar_por_usuario(
        self,
        db: Session,
        usuario_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Pedido]:
        consulta = (
            select(Pedido)
            .where(
                Pedido.usuario_id == usuario_id
            )
            .order_by(Pedido.fecha_creacion.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(
            db.scalars(consulta).all()
        )

    def actualizar(
        self,
        db: Session,
        pedido: Pedido,
    ) -> Pedido:
        db.flush()

        return pedido

    def eliminar(
        self,
        db: Session,
        pedido: Pedido,
    ) -> None:
        db.delete(pedido)
        db.flush()


pedido_repository = PedidoRepository()