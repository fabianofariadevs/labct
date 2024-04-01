#RECEITAS##################################################################################################################################
from labct.db import db

class Receitas(db.Model):
    __tablename__ = "receitas"
    __table_args__ = {"extend_existing": True}

    id_rct = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_rct = db.Column(db.String(75))
    descricao_rct = db.Column(db.Text)
    preparo_rct = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="receitas")
    receitasmateriasprimas = db.relationship("ReceitaMateriasPrimas", back_populates="receitas")
    