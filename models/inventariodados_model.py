# INVENTARIO DADOS ###################################################################################
from labct.db import db
from datetime import datetime, timezone

class InventarioDados(db.Model):
    __tablename__ = "inventariodados"
    __table_args__ = {"extend_existing": True}

    id_invtdados = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_invt = db.Column(db.Integer, db.ForeignKey('inventario.id_invt'), nullable=False)
    data_invt = db.Column(db.DateTime, default=datetime.now(timezone.utc),nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), nullable=False)
    nome_mp = db.Column(db.String(75), nullable=False)
    unidade_mp = db.Column(db.Enum('KG', 'UN'))
    quantidade_estq = db.Column(db.Numeric(10,3), db.ForeignKey('estoque.quantidade_estq'), nullable=False)
    quantidade_invtdados = db.Column(db.Numeric(10, 3))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="inventariosdados")
    materias_primas = db.relationship("MateriasPrimas", back_populates="inventariodados")
    inventario = db.relationship("Inventario", back_populates="inventariosdados")
    estoque = db.relationship("Estoque", back_populates="inventariosdados")
