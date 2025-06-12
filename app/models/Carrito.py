from app import db

class Carrito(db.Model):
    __tablename__ = 'Carrito'

    idCarrito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    montoTotal = db.Column(db.Numeric(10, 2), nullable=False)

    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), nullable=False)

    # Relación opcional (si tenés el modelo Usuario)
    usuario = db.relationship('Usuario', backref=db.backref('carritos', lazy=True))

    def to_dict(self):
        return {
            'idCarrito': self.idCarrito,
            'subtotal': float(self.subtotal),
            'montoTotal': float(self.montoTotal),
            'idUsuario': self.idUsuario
        }
