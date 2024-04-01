# COMPRAS #################################################################################################

from labct.db import db
from datetime import datetime, timezone

class Compras(db.Model):
    __tablename__ = "compras"
    __table_args__ = {"extend_existing": True}

    id_compras = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_compras = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    estado_compras = db.Column(db.Enum('Pendente', 'Entregue'))

    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="compras")
    comprasdados = db.relationship("ComprasDados", back_populates="compras")