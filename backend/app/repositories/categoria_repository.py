from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate

class CategoriaRepository:
    def listar(
        self,
        db: Session,
    ) -> list[Categoria]:

        #Crea una consulta
        consulta = select(Categoria).order_by(
            Categoria.id
        )
        #Ejecuta consulta y devuelve entidades Categoria
        categorias = db.scalars(consulta).all()

        return list(categorias)

    def buscar_por_id(
        self,
        db: Session,
        categoria_id: int,
    ) -> Categoria | None:

        return db.get(
            Categoria,
            categoria_id,
        )

    def buscar_por_nombre(
        self,
        db: Session,
        nombre: str,
    ) -> Categoria | None:

        consulta = select(Categoria).where(
            Categoria.nombre == nombre
        )

        return db.scalars(consulta).first()

    def crear(
        self,
        db: Session,
        datos: CategoriaCreate,
    ) -> Categoria:

        categoria = Categoria(
            nombre=datos.nombre,
            descripcion=datos.descripcion,
        )

        #Prepara un nuevo registro
        db.add(categoria)
        #Confirma operación en BD
        db.commit()
        #Actualiza el objeto en BD, como su id
        db.refresh(categoria)

        return categoria

    def actualizar(
        self,
        db: Session,
        categoria: Categoria,
        datos: CategoriaUpdate,
    ) -> Categoria:

        #Conveirte en un diccionario de Python
        campos_actualizados = datos.model_dump(
            #Incluya solamente los campos que el cliente envió explícitamente.
            exclude_unset=True
        )

        for campo, valor in campos_actualizados.items():
            setattr(
                categoria,
                campo,
                valor,
            )

        db.commit()
        db.refresh(categoria)

        return categoria

    def eliminar(
        self,
        db: Session,
        categoria: Categoria,
    ) -> None:

        db.delete(categoria)
        db.commit()