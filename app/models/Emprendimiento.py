from app import db

class Emprendimiento(db.Model):
    __tablename__ = 'Emprendimiento'

    idEmprendimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreEmprendimiento = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    ubicacion = db.Column(db.String(150), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), nullable=False)

    def to_dict(self):
        return {
            'idEmprendimiento': self.idEmprendimiento,
            'nombreEmprendimiento': self.nombreEmprendimiento,
            'descripcion': self.descripcion,
            'ubicacion': self.ubicacion,
            'telefono': self.telefono,
            'idUsuario': self.idUsuario
        }
