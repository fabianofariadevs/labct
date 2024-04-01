# INVENTARIO HISTORICO #######################################################################

from datetime import datetime, timezone
from labct.db import db

class Historico(db.Model):
    __tablename__ = "historico"
    __table_args__ = {"extend_existing": True}

    id_hst = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_change = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    id_mp = db.Column(db.Integer, nullable=False)
    

    nome_mp = db.Column(db.String(75))

    ultimaquantidade_hst = db.Column(db.Numeric(10, 3))
    novaquantidade_hst = db.Column(db.Numeric(10, 3))
    difference_hst = db.Column(db.Numeric(10, 3))
    modo_hst = db.Column(db.Enum('Registro Manual', 'Compra', 'Inventario'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="historico")