from labct.db import db
from flask_login import UserMixin

# USERS #################################################################################################

class Usuarios(UserMixin, db.Model):

    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    materias_primas = db.relationship('MateriasPrimas', back_populates="usuarios" , lazy=True)
    fornecedores = db.relationship('Fornecedores', back_populates="usuarios" , lazy=True)
    estoque = db.relationship('Estoque', back_populates="usuarios" , lazy=True)
    historico = db.relationship('Historico', back_populates="usuarios", lazy=True)
    inventario = db.relationship('Inventario', back_populates="usuarios", lazy=True)
    inventariosdados = db.relationship('InventarioDados', back_populates="usuarios", lazy=True)
    compras = db.relationship('Compras', back_populates="usuarios", lazy=True)
    comprasdados = db.relationship('ComprasDados', back_populates="usuarios", lazy=True)
    receitas = db.relationship('Receitas', back_populates="usuarios", lazy=True)
    receitasmateriasprimas = db.relationship('ReceitaMateriasPrimas', back_populates="usuarios", lazy=True)