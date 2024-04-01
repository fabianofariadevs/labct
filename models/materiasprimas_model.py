from labct.db import db


class MateriasPrimas(db.Model):
    __tablename__ = "materiasprimas"
    __table_args__ = {"extend_existing": True}

    id_mp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_mp = db.Column(db.String(75))
    unidade_mp = db.Column(db.Enum('KG', 'UN'))
    pesounitario_mp = db.Column(db.Numeric(10, 3))
    pesototal_mp = db.Column(db.Numeric(10, 3))
    custo_mp = db.Column(db.Numeric(10, 2))
    custoemkg_mp = db.Column(db.Numeric(10, 2))
    departamento_mp = db.Column(db.Enum('Carnes', 'Farinhas', 'Hortifruti', 'Mercearia', 'Misturas', 'Ovos', 'Queijos'))
    pedidomin_mp = db.Column(db.Numeric(10,3))
    gastomedio_mp = db.Column(db.Numeric(10, 3))
    gms_mp = db.Column(db.Numeric(10, 3))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) 

    estoque = db.relationship("Estoque", back_populates="materias_primas")
    usuarios = db.relationship("Usuarios", back_populates="materias_primas")
    inventariodados = db.relationship("InventarioDados", back_populates="materias_primas")
    receitasmateriasprimas = db.relationship("ReceitaMateriasPrimas", back_populates="materias_primas")

    def __init__(self, nome_mp, unidade_mp, pesounitario_mp, pesototal_mp, custo_mp, custoemkg_mp, departamento_mp, pedidomin_mp, gastomedio_mp, gms_mp, user_id):
        self.nome_mp = nome_mp
        self.unidade_mp = unidade_mp
        self.pesounitario_mp = pesounitario_mp
        self.pesototal_mp = pesototal_mp
        self.custo_mp = custo_mp
        self.custoemkg_mp = custoemkg_mp
        self.departamento_mp = departamento_mp
        self.pedidomin_mp = pedidomin_mp
        self.gastomedio_mp = gastomedio_mp
        self.gms_mp = gms_mp
        self.user_id = user_id