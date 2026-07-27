from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.models.usuario import Usuario
from app.repositories.pedido_repository import pedido_repository
from app.schemas.pedido import (
    PedidoCreate,
    PedidoDireccionUpdate,
    PedidoEstadoUpdate,
)


class PedidoService:

   def crear(
    self,
    db: Session,
    datos: PedidoCreate,
) -> Pedido:

    try:
        usuario = db.get(
            Usuario,
            datos.usuario_id,
        )

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario indicado no existe",
            )

        pedido = Pedido(
            usuario_id=datos.usuario_id,
            direccion_entregas=datos.direccion_entregas,
        )

        pedido_repository.crear(
            db,
            pedido,
        )

        db.commit()
        db.refresh(pedido)

        return pedido

    except HTTPException:
        raise

    except IntegrityError as error:
        db.rollback()

        print("INTEGRITY ERROR:", repr(error))
        print("ERROR ORIGINAL:", error.orig)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.orig),
        ) from error

    except SQLAlchemyError as error:
        db.rollback()

        print("SQLALCHEMY ERROR:", repr(error))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    except Exception as error:
        db.rollback()

        print("ERROR GENERAL:", type(error).__name__, repr(error))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    def obtener_por_id(
        self,
        db: Session,
        pedido_id: int,
    ) -> Pedido:
        pedido = pedido_repository.obtener_por_id(
            db,
            pedido_id,
        )

        if pedido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido no encontrado",
            )

        return pedido

    def listar(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Pedido]:
        return pedido_repository.listar(
            db,
            skip,
            limit,
        )

    def listar_por_usuario(
        self,
        db: Session,
        usuario_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Pedido]:
        usuario = db.get(
            Usuario,
            usuario_id,
        )

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return pedido_repository.listar_por_usuario(
            db,
            usuario_id,
            skip,
            limit,
        )

    def actualizar_direccion(
        self,
        db: Session,
        pedido_id: int,
        datos: PedidoDireccionUpdate,
    ) -> Pedido:
        pedido = self.obtener_por_id(
            db,
            pedido_id,
        )

        pedido.direccion_entrega = datos.direccion_entrega

        try:
            pedido_repository.actualizar(
                db,
                pedido,
            )

            db.commit()
            db.refresh(pedido)

            return pedido

        except SQLAlchemyError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo actualizar la dirección del pedido",
            ) from error

    def actualizar_estado(
        self,
        db: Session,
        pedido_id: int,
        datos: PedidoEstadoUpdate,
    ) -> Pedido:
        pedido = self.obtener_por_id(
            db,
            pedido_id,
        )

        pedido.estado = datos.estado

        try:
            pedido_repository.actualizar(
                db,
                pedido,
            )

            db.commit()
            db.refresh(pedido)

            return pedido

        except SQLAlchemyError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo actualizar el estado del pedido",
            ) from error

    def eliminar(
        self,
        db: Session,
        pedido_id: int,
    ) -> None:
        pedido = self.obtener_por_id(
            db,
            pedido_id,
        )

        try:
            pedido_repository.eliminar(
                db,
                pedido,
            )

            db.commit()

        except SQLAlchemyError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo eliminar el pedido",
            ) from error


pedido_service = PedidoService()