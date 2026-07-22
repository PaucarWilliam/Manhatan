from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


class CategoriaService:

    def __init__(
        self,
        repository: CategoriaRepository,
    ) -> None:
        self.repository = repository

    def listar(
        self,
        db: Session,
    ) -> list[Categoria]:
        return self.repository.listar(db)

    def obtener_por_id(
        self,
        db: Session,
        categoria_id: int,
    ) -> Categoria:
        categoria = self.repository.buscar_por_id(
            db,
            categoria_id,
        )

        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La categoría no existe",
            )

        return categoria

    def crear(
        self,
        db: Session,
        datos: CategoriaCreate,
    ) -> Categoria:
        categoria_existente = self.repository.buscar_por_nombre(
            db,
            datos.nombre,
        )

        if categoria_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una categoría con ese nombre",
            )

        return self.repository.crear(
            db,
            datos,
        )

    def actualizar(
        self,
        db: Session,
        categoria_id: int,
        datos: CategoriaUpdate,
    ) -> Categoria:
        categoria = self.obtener_por_id(
            db,
            categoria_id,
        )

        if datos.nombre is not None:
            categoria_existente = self.repository.buscar_por_nombre(
                db,
                datos.nombre,
            )

            if (
                categoria_existente is not None
                and categoria_existente.id != categoria_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe una categoría con ese nombre",
                )

        return self.repository.actualizar(
            db,
            categoria,
            datos,
        )

    def eliminar(
        self,
        db: Session,
        categoria_id: int,
    ) -> None:
        categoria = self.obtener_por_id(
            db,
            categoria_id,
        )

        self.repository.eliminar(
            db,
            categoria,
        )


categoria_service = CategoriaService(
    CategoriaRepository()
)