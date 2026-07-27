from enum import Enum

class RolUsuario(str, Enum):
    CLIENTE = "cliente"
    ADMINISTRADOR = "admin"


class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

def enum_values(enum_class: type[Enum]) -> list[str]:
    #Indica a SQLAlchemy que debe guardar los valores del enum y no los nombres internos de sus elementos
    return [elemento.value for elemento in enum_class]