from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float

@dataclass
class Order:
    id: int
    product_id: int
    quantity: int
    paid: bool = False
