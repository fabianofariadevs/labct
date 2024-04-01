
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, func
from labct.db import db


# ESTOQUE #####################################################################################

class Estoque(db.Model):
    __tablename__ = "estoque"
    __table_args__ = {"extend_existing": True}

    id_estq = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_mp = db.Column(db.Integer, ForeignKey('materiasprimas.id_mp'), nullable=False)
    #materiaprima = db.relationship("MateriasPrimas", foreign_keys=[id_mp])

    nome_mp = db.Column(db.String(75))
    unidade_mp = db.Column(db.Enum('KG','UN'))
    gms_mp = db.Column(db.Numeric(10, 3))
    pedidomin_mp = db.Column(db.Numeric(10,3))

    quantidade_estq = db.Column(db.Numeric(10,3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    materias_primas = relationship("MateriasPrimas", back_populates="estoque")
    usuarios = db.relationship("Usuarios", back_populates="estoque")
    inventariosdados = db.relationship("InventarioDados", back_populates="estoque")

    def __init__(self, id_mp, nome_mp, unidade_mp, gms_mp, pedidomin_mp, quantidade_estq, user_id):
        self.id_mp = id_mp
        self.nome_mp = nome_mp
        self.unidade_mp = unidade_mp
        self.gms_mp = gms_mp
        self.pedidomin_mp = pedidomin_mp
        self.quantidade_estq = quantidade_estq
        self.user_id = user_id