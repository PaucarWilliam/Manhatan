from collections.abc import Generator

from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.detalle_pedido import (
    DetallePedidoCreate,
    DetallePedidoResponse,
    DetallePedidoUpdate,
)
from app.services.detalle_pedido_service import (
    detalle_pedido_service,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/detalles-pedido",
    tags=["Detalles de pedido"],
)


@router.post(
    "",
    response_model=DetallePedidoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_detalle_pedido(
    datos: DetallePedidoCreate,
    db: Session = Depends(get_db),
):
    return detalle_pedido_service.crear(
        db,
        datos,
    )


@router.get(
    "",
    response_model=list[DetallePedidoResponse],
)
def listar_detalles_pedido(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    return detalle_pedido_service.listar(
        db,
        skip,
        limit,
    )


@router.get(
    "/pedido/{pedido_id}",
    response_model=list[DetallePedidoResponse],
)
def listar_detalles_por_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
):
    return detalle_pedido_service.listar_por_pedido(
        db,
        pedido_id,
    )


@router.get(
    "/{detalle_id}",
    response_model=DetallePedidoResponse,
)
def obtener_detalle_pedido(
    detalle_id: int,
    db: Session = Depends(get_db),
):
    return detalle_pedido_service.obtener_por_id(
        db,
        detalle_id,
    )


@router.patch(
    "/{detalle_id}",
    response_model=DetallePedidoResponse,
)
def actualizar_detalle_pedido(
    detalle_id: int,
    datos: DetallePedidoUpdate,
    db: Session = Depends(get_db),
):
    return detalle_pedido_service.actualizar(
        db,
        detalle_id,
        datos,
    )


@router.delete(
    "/{detalle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_detalle_pedido(
    detalle_id: int,
    db: Session = Depends(get_db),
):
    detalle_pedido_service.eliminar(
        db,
        detalle_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )