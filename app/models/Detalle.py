from app import db

class Detalle(db.Model):
    __tablename__ = 'Detalle'

    idDetalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidadProductos = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(db.Numeric(5, 2), nullable=False)
    subtotalDetalle = db.Column(db.Numeric(5, 2), nullable=False)
    idCarrito = db.Column(db.Integer, db.ForeignKey('Carrito.idCarrito'), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('Producto.idProducto'), nullable=False)

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'idDetalle': self.idDetalle,
            'cantidadProductos': self.cantidadProductos,
            'precioUnitario': float(self.precioUnitario),
            'subtotalDetalle': float(self.subtotalDetalle),
            'idCarrito': self.idCarrito,
            'idProducto': self.idProducto
        }