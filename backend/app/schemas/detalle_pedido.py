from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# SOLO SE ESTARIA ENVIANDO LO QUE EL PRODUCTO Y LA CANTIDAD SINO POR LO CONTRARIO SE ESTARIA ABRIENDO UNA BRECA A QUE PUEDA MODIFICAR EL PRECIO DESDE POSTAMN O FRONTEND.

class DetallePedidoCreate(BaseModel):
    pedido_id: int = Field(
        gt =0
    )

    producto_id: int = Field(
        gt=0,
    )

    cantidad: int = Field(
        gt = 0
    )

class DetallePedidoUpdate(BaseModel):
    cantidad: int = Field(
        gt = 0,
    )

class DetallePedidoResponse(BaseModel):
    id: int
    pedido_id:int
    producto_id:int
    cantidad:int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(
        from_attributes= True,
    )