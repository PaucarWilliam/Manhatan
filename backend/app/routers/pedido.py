from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from collections.abc import Generator

from app.database import SessionLocal


from app.dependencies import obtener_db
from app.schemas.pedido import (
    PedidoCreate,
    PedidoDireccionUpdate,
    PedidoEstadoUpdate,
    PedidoResponse,
)
from app.services.pedido_service import pedido_service


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_pedido(
    datos: PedidoCreate,
    db: Session = Depends(obtener_db),
):
    return pedido_service.crear(
        db,
        datos,
    )


@router.get(
    "",
    response_model=list[PedidoResponse],
)
def listar_pedidos(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    db: Session = Depends(obtener_db),
):
    return pedido_service.listar(
        db,
        skip,
        limit,
    )


@router.get(
    "/usuario/{usuario_id}",
    response_model=list[PedidoResponse],
)
def listar_pedidos_por_usuario(
    usuario_id: int,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    db: Session = Depends(obtener_db),
):
    return pedido_service.listar_por_usuario(
        db,
        usuario_id,
        skip,
        limit,
    )


@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse,
)
def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(obtener_db),
):
    return pedido_service.obtener_por_id(
        db,
        pedido_id,
    )


@router.patch(
    "/{pedido_id}/direccion",
    response_model=PedidoResponse,
)
def actualizar_direccion_pedido(
    pedido_id: int,
    datos: PedidoDireccionUpdate,
    db: Session = Depends(obtener_db),
):
    return pedido_service.actualizar_direccion(
        db,
        pedido_id,
        datos,
    )


@router.patch(
    "/{pedido_id}/estado",
    response_model=PedidoResponse,
)
def actualizar_estado_pedido(
    pedido_id: int,
    datos: PedidoEstadoUpdate,
    db: Session = Depends(obtener_db),
):
    return pedido_service.actualizar_estado(
        db,
        pedido_id,
        datos,
    )


@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_pedido(
    pedido_id: int,
    db: Session = Depends(obtener_db),
):
    pedido_service.eliminar(
        db,
        pedido_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )