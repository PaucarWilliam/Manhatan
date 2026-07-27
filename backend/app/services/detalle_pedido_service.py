from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
from app.models.producto import Producto
from app.repositories.detalle_pedido_repository import (
    detalle_pedido_repository,
)
from app.schemas.detalle_pedido import (
    DetallePedidoCreate,
    DetallePedidoUpdate,
)


class DetallePedidoService:

    def obtener_pedido(
        self,
        db: Session,
        pedido_id: int,
    ) -> Pedido:
        pedido = db.get(
            Pedido,
            pedido_id,
        )

        if pedido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El pedido indicado no existe",
            )

        return pedido

    def obtener_producto(
        self,
        db: Session,
        producto_id: int,
    ) -> Producto:
        producto = db.get(
            Producto,
            producto_id,
        )

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El producto indicado no existe",
            )

        return producto

    def crear(
        self,
        db: Session,
        datos: DetallePedidoCreate,
    ) -> DetallePedido:
        pedido = self.obtener_pedido(
            db,
            datos.pedido_id,
        )

        producto = self.obtener_producto(
            db,
            datos.producto_id,
        )

        # Esta propiedad debe coincidir con tu modelo Producto.
        precio_unitario = Decimal(
            str(producto.precio)
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        subtotal = (
            precio_unitario * datos.cantidad
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        detalle = DetallePedido(
            pedido_id=datos.pedido_id,
            producto_id=datos.producto_id,
            cantidad=datos.cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
        )

        try:
            detalle_pedido_repository.crear(
                db,
                detalle,
            )

            pedido.total = (
                detalle_pedido_repository.calcular_total_pedido(
                    db,
                    datos.pedido_id,
                )
            )

            db.commit()
            db.refresh(detalle)

            return detalle

        except IntegrityError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error.orig),
            ) from error

        except SQLAlchemyError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            ) from error

    def obtener_por_id(
        self,
        db: Session,
        detalle_id: int,
    ) -> DetallePedido:
        detalle = detalle_pedido_repository.obtener_por_id(
            db,
            detalle_id,
        )

        if detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de pedido no encontrado",
            )

        return detalle

    def listar(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DetallePedido]:
        return detalle_pedido_repository.listar(
            db,
            skip,
            limit,
        )

    def listar_por_pedido(
        self,
        db: Session,
        pedido_id: int,
    ) -> list[DetallePedido]:
        self.obtener_pedido(
            db,
            pedido_id,
        )

        return detalle_pedido_repository.listar_por_pedido(
            db,
            pedido_id,
        )

    def actualizar(
        self,
        db: Session,
        detalle_id: int,
        datos: DetallePedidoUpdate,
    ) -> DetallePedido:
        detalle = self.obtener_por_id(
            db,
            detalle_id,
        )

        detalle.cantidad = datos.cantidad

        detalle.subtotal = (
            detalle.precio_unitario * datos.cantidad
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        try:
            detalle_pedido_repository.actualizar(
                db,
                detalle,
            )

            pedido = self.obtener_pedido(
                db,
                detalle.pedido_id,
            )

            pedido.total = (
                detalle_pedido_repository.calcular_total_pedido(
                    db,
                    detalle.pedido_id,
                )
            )

            db.commit()
            db.refresh(detalle)

            return detalle

        except IntegrityError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error.orig),
            ) from error

        except SQLAlchemyError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            ) from error

    def eliminar(
        self,
        db: Session,
        detalle_id: int,
    ) -> None:
        detalle = self.obtener_por_id(
            db,
            detalle_id,
        )

        pedido_id = detalle.pedido_id

        try:
            detalle_pedido_repository.eliminar(
                db,
                detalle,
            )

            pedido = self.obtener_pedido(
                db,
                pedido_id,
            )

            pedido.total = (
                detalle_pedido_repository.calcular_total_pedido(
                    db,
                    pedido_id,
                )
            )

            db.commit()

        except SQLAlchemyError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            ) from error


detalle_pedido_service = DetallePedidoService()