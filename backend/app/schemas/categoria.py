from pydantic import BaseModel, ConfigDict, Field

#Campos compartidos
class CategoriaBase(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=80,
    )

    descripcion: str | None = Field(
        default=None,
        max_length=500
    )

#Lo que el usuario envía al crear una cateogría
class CategoriaCreate(CategoriaBase):
    pass

#Campos que se pueden actualizar
class CategoriaUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=80,
    )
    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )
    activa: bool | None = None


#Respuesta JSON
class CategoriaResponse(CategoriaBase):
    id: int
    activa: bool

    #Conveierte objeto SQLAlchemy en JSON
    model_config = ConfigDict(
        from_attributes=True,
    )