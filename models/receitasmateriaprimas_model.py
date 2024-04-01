####################################################################################
from labct.db import db

class ReceitaMateriasPrimas(db.Model):
    __tablename__ = "receitamateriasprimas"
    __table_args__ = {"extend_existing": True}

    id_rct = db.Column(db.Integer, db.ForeignKey('receitas.id_rct'), primary_key=True)
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), primary_key=True)
    nome_mp = db.Column(db.String(75))
    quantidade = db.Column(db.Numeric(10,2))
    unidade = db.Column(db.Enum('Unidade(s)', 'Grama(s)', 'Kilogramo(s)', 'Colher(es)', 'Xícara(s)'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="receitasmateriasprimas")
    materias_primas = db.relationship("MateriasPrimas", back_populates="receitasmateriasprimas")
    receitas = db.relationship("Receitas", back_populates="receitasmateriasprimas")