# INVENTARIO ###################################################################################
from labct.db import db
from datetime import datetime, timezone

class Inventario(db.Model):
    __tablename__ = "inventario"
    __table_args__ = {"extend_existing": True}

    id_invt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_invt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    estado_invt = db.Column(db.Enum('Aberto', 'Fechado'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)


    usuarios = db.relationship("Usuarios", back_populates="inventario")
    inventariosdados = db.relationship("InventarioDados", back_populates="inventario")