from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.dependencies import obtener_db
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)
from app.services.categoria_service import (
    categoria_service,
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"],
)

@router.get(
    "",
    response_model=list[CategoriaResponse],
)
def listar_categorias(
    db: Session = Depends(obtener_db),
) -> list[CategoriaResponse]:

    return categoria_service.listar(db)

@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse,
)
def obtener_categoria(
    categoria_id: int,
    db: Session = Depends(obtener_db),
) -> CategoriaResponse:

    return categoria_service.obtener_por_id(
        db,
        categoria_id,
    )

@router.post(
    "",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_categoria(
    datos: CategoriaCreate,
    db: Session = Depends(obtener_db),
) -> CategoriaResponse:

    return categoria_service.crear(
        db,
        datos,
    )

@router.put(
    "/{categoria_id}",
    response_model=CategoriaResponse,
)
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaUpdate,
    db: Session = Depends(obtener_db),
) -> CategoriaResponse:

    return categoria_service.actualizar(
        db,
        categoria_id,
        datos,
    )

@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_categoria(
    categoria_id: int,
    db: Session = Depends(obtener_db),
) -> Response:

    categoria_service.eliminar(
        db,
        categoria_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )