from app import db

class Categoria(db.Model):
    __tablename__ = 'Categoria'

    idCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreCategoria = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'idCategoria': self.idCategoria,
            'nombreCategoria': self.nombreCategoria,
            'descripcion': self.descripcion
        }
