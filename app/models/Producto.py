from app import db

class Producto(db.Model):
    __tablename__ = 'Producto'

    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreProducto = db.Column(db.String(255), nullable=False)
    descripcionProducto = db.Column(db.Text)
    precio = db.Column(db.Numeric(5, 2), nullable=False)
    disponibilidad = db.Column(db.Integer, nullable=False)
    descuento = db.Column(db.Numeric(5, 2))
    imagenProductoPrincipal = db.Column(db.String(255))
    imagenProductoAdicionales = db.Column(db.String(255))
    vecesGuardadoEnCarrito = db.Column(db.Integer, default=0)
    idCategoria = db.Column(db.Integer, db.ForeignKey('Categoria.idCategoria'))

    # Relación con Detalle (un producto puede estar en muchos detalles)
    detalles = db.relationship('Detalle', backref='producto', lazy=True)

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'idProducto': self.idProducto,
            'nombreProducto': self.nombreProducto,
            'descripcionProducto': self.descripcionProducto,
            'precio': float(self.precio),
            'disponibilidad': self.disponibilidad,
            'descuento': float(self.descuento) if self.descuento else None,
            'imagenProductoPrincipal': self.imagenProductoPrincipal,
            'imagenProductoAdicionales': self.imagenProductoAdicionales,
            'vecesGuardadoEnCarrito': self.vecesGuardadoEnCarrito,
            'idCategoria': self.idCategoria
        }