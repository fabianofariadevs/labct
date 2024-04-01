from flask import Flask, render_template, request, redirect, url_for, session, g, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import pymysql
import os
from datetime import datetime

from babel.dates import format_date
from flask import abort  # Import abort function from Flask to handle HTTP errors
from sqlalchemy.exc import IntegrityError

from sqlalchemy import func


from decimal import Decimal

from config import Config
from labct.db import db, ma, login_manager, app


from models import fornecedores_model, materiasprimas_model, estoque_model, historico_model, inventario_model, inventariodados_model, compras_model, comprasdados_model, usuarios_model, config_model, receitas_model, receitasmateriaprimas_model

from flask_login import UserMixin,current_user, login_required, LoginManager, login_user
pymysql.install_as_MySQLdb()

with app.app_context():
    db.create_all()


# Initialize Flask-Login


#login_manager.init_app(app)
## MODELS AND SCHEMAS ###########################################################################################################################

class FornecedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = fornecedores_model.Fornecedores

    id_fornecedor = ma.auto_field()
    nome_fornecedor = ma.auto_field()
    tempo_entrega = ma.auto_field()
    prazo_pagamento = ma.auto_field()
    dia_pedido = ma.auto_field()
    nome_vendedor = ma.auto_field()
    contato_tel = ma.auto_field()
    email_vendedor = ma.auto_field()

class MateriasPrimasSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = materiasprimas_model.MateriasPrimas
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    pesounitario_mp = ma.auto_field()
    pesototal_mp = ma.auto_field()
    custo_mp = ma.auto_field()
    custoemkg_mp = ma.auto_field()
    departamento_mp = ma.auto_field()
    pedidomin_mp = ma.auto_field()
    gastomedio_mp = ma.auto_field()
    gms_mp = ma.auto_field()

class EstoqueSchema(ma.SQLAlchemySchema):
    class Meta:
        model = estoque_model.Estoque
        
    id_estq = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    quantidade_estq = ma.auto_field()
    gms_mp = ma.auto_field()
    pedidomin_mp = ma.auto_field()

class HistoricoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = historico_model.Historico
        
    id_hst = ma.auto_field() 
    date_change = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    ultimaquantidade_hst = ma.auto_field()
    novaquantidade_hst = ma.auto_field()
    difference_hst = ma.auto_field()
    modo_hst = ma.auto_field()

class InventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = inventario_model.Inventario
        
    id_invt = ma.auto_field()
    estado_invt = ma.auto_field()
    data_invt = ma.auto_field()
 
class InventarioDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = inventariodados_model.InventarioDados
        
    id_invtdados = ma.auto_field()
    id_invt = ma.auto_field()
    data_invt = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    quantidade_invtdados = ma.auto_field()   
    quantidade_estq = ma.auto_field()   

class ComprasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = compras_model.Compras
        
    id_compras = ma.auto_field()
    estado_compras = ma.auto_field()
    data_compras = ma.auto_field()   

class ComprasDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = comprasdados_model.ComprasDados
        
    id_comprasd = ma.auto_field()
    id_compras = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    pedido_comprasd = ma.auto_field()
    fornecedor_comprasd = ma.auto_field()
    valorpedido_comprasd = ma.auto_field()
    departamento_comprasd = ma.auto_field()
    previsao_comprasd = ma.auto_field()
    vencimento_comprasd = ma.auto_field()
    fechado_comprasd = ma.auto_field()

class ReceitasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = receitas_model.Receitas

    id_rct = ma.auto_field()
    nome_rct = ma.auto_field()
    descricao_rct = ma.auto_field()
    preparo_rct = ma.auto_field()

class ReceitasMateriasPrimasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = receitasmateriaprimas_model.ReceitaMateriasPrimas

    id_rct = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    quantidade = ma.auto_field()
    unidade = ma.auto_field()

####################################################################### APP ###################################################################################################

#with app.app_context():
#    db.create_all()

# FUNCOES DO GIRO MEDIO ########################################################################################################

def some_function(giro_medio):
    config = Config.query.filter_by(giro_medio=giro_medio).first()

    # Create or update configuration settings
def update_config(new_value):
    config = Config.query.first()
    if config:
        config.giro_medio = new_value
    else:
        config = Config(giro_medio=new_value)
        db.session.add(config)
    db.session.commit()
    
# Route to update the GM ###############
    
@app.route('/giromedio', methods=['POST'])
def update():
    new_value = int(request.form['new_value'])
    update_config(new_value)

    materiaprima = materiasprimas_model.MateriasPrimas.query.filter_by(user_id=current_user.id).all()

    for mp in materiaprima:
        if mp.gastomedio_mp is not None:
            gm_float = float(mp.gastomedio_mp)
            new_value_float = float(new_value)

            new_gm = gm_float * new_value_float

            mp.gms_mp = new_gm  # Update the gms_mp column of the existing MateriasPrimas object


    db.session.commit()


    return redirect(url_for('materiasPrimas'))

# Custom filter to round numbers
@app.template_filter('giromedio')
def round_filter(value):
    config = Config.query.first()
    if config:
        return value * config.giro_medio
    else:
        return value * 6  # Default value if not found

#################################################################################################################################

# ROUTES ########################################################################################################################

@login_manager.user_loader
def load_user(user_id):
    return usuarios_model.Usuarios.query.get(user_id)

@app.route('/')
def index():

    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = usuarios_model.Usuarios(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_url = request.form.get("next")

        user = usuarios_model.Usuarios.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id
            login_user(user)

            # Redirect to the originally requested URL if available, or else redirect to the index route
            next_page = request.args.get('next')  # Get the 'next' parameter from the request URL
            return redirect(next_page or url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/cleanup-fornecedores', methods=['GET'])
def cleanupFornecedor():
    with app.app_context():
        db.session.query(fornecedores_model.Fornecedores).delete()  # Delete all entries from the Entry table
        db.session.commit()
    return redirect(url_for('fornecedores'))

@app.route('/cleanup-mp', methods=['GET'])
def cleanupMP():
    with app.app_context():
        db.session.query(materiasPrimas.MateriasPrimas).delete()  # Delete all entries from the Entry table
        db.session.commit()
    return redirect(url_for('materiasprimas'))

## FORNECEDORES ##########################################

@app.route('/fornecedores', methods=['GET', 'POST'])
@login_required
def fornecedores():
    print(dir(datetime))
    if request.method == 'POST':
        nome_fornecedor = request.form.get('nome_fornecedor')
        tempo_entrega = request.form.get('tempo_entrega')
        prazo_pagamento = request.form.get('prazo_pagamento')
        dia_pedido = request.form.get('dia_pedido')
        nome_vendedor = request.form.get('nome_vendedor')
        contato_tel = request.form.get('contato_tel')
        email_vendedor = request.form.get('email_vendedor')

        fornecedores = fornecedores_model.Fornecedores(
            nome_fornecedor=nome_fornecedor,
            tempo_entrega=tempo_entrega,
            prazo_pagamento=prazo_pagamento,
            dia_pedido=dia_pedido,
            nome_vendedor=nome_vendedor,
            contato_tel=contato_tel,
            email_vendedor=email_vendedor,
            user_id=current_user.id
            )
        db.session.add(fornecedores)
        db.session.commit()
        return redirect(url_for('fornecedores'))  # Redirect to GET request after form submission


    fornecedores = fornecedores_model.Fornecedores.query.filter_by(user_id=current_user.id).all()
    fornecedor_schema = FornecedorSchema(many=True)
    serialized_data = fornecedor_schema.dump(fornecedores)
    return render_template('fornecedores.html', fornecedores=serialized_data)

@app.route('/delete-fornecedor/<int:id>', methods=['POST'])
def deleteFornecedor(id):
    fornecedores = fornecedores_model.Fornecedores.query.get_or_404(id)
    db.session.delete(fornecedores)
    db.session.commit()
    return redirect(url_for('fornecedores', id=id) )

@app.route('/edit-fornecedor/<int:id>', methods=['POST'])
def editFornecedor(id):
    if request.method == 'POST':
        fornecedores = fornecedores_model.Fornecedores.query.get_or_404(id)
        fornecedores.nome_fornecedor = request.form.get('nome_fornecedor')
        fornecedores.tempo_entrega = request.form.get('tempo_entrega')
        fornecedores.prazo_pagamento = request.form.get('prazo_pagamento')
        fornecedores.dia_pedido = request.form.get('dia_pedido')
        fornecedores.nome_vendedor = request.form.get('nome_vendedor')
        fornecedores.contato_tel = request.form.get('contato_tel')
        fornecedores.email_vendedor = request.form.get('email_vendedor')

        db.session.commit()
        return redirect(url_for('fornecedores', id=id))

# MATERIAS PRIMAS ###################################

@app.route('/materiasprimas', methods=['GET', 'POST'])
@login_required
def materiasPrimas(giromedio=None):
    # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table
    config = config_model.Config.query.first()
    #giromedio = config.giro_medio if config else None
    if config is not None:
        giromedio = config.giro_medio
    else:
        giromedio = None  # Or any other default value
    print(giromedio)

    cost_per_unit = 2
    if request.method == 'POST':
        #id_mp = request.form.get('id_mp')
        nome_mp = request.form.get('nome_mp')
        unidade_mp = request.form.get('unidade_mp')
        pesounitario_mp = request.form.get('pesounitario_mp')
        pesototal_mp = request.form.get('pesototal_mp')
        custo_mp = request.form.get('custo_mp')
        departamento_mp = request.form.get('departamento_mp')
        pedidomin_mp = request.form.get('pedidomin_mp')
        gastomedio_mp = request.form.get('gastomedio_mp')



        # Convert to floats
        custo_mp_float = float(custo_mp)
        pesototal_mp_float = float(pesototal_mp)
        gastomedio_mp_float = float(gastomedio_mp)
        if giromedio is not None:
            giromedio_float = float(giromedio)
        else:
            giromedio_float = 6

        gmps = gastomedio_mp_float * giromedio_float

        # Perform the division operation
        if pesototal_mp_float != 0:  # Avoid division by zero
            cost_per_unit = custo_mp_float / pesototal_mp_float

        materiasprimas = materiasprimas_model.MateriasPrimas(
            nome_mp=nome_mp,
            unidade_mp=unidade_mp,
            pesounitario_mp=pesounitario_mp,
            pesototal_mp=pesototal_mp,
            custo_mp=custo_mp,
            custoemkg_mp=cost_per_unit,
            departamento_mp=departamento_mp,
            pedidomin_mp=pedidomin_mp,
            gastomedio_mp=gastomedio_mp,
            gms_mp=gmps,
            user_id=current_user.id
            )

        db.session.add(materiasprimas)
        db.session.commit()

        id_mp = materiasprimas.id_mp
        gms = materiasprimas.gms_mp
        pedidomin = materiasprimas.pedidomin_mp


        estoque = estoque_model.Estoque(
            id_mp=id_mp,
            nome_mp=nome_mp,
            unidade_mp=unidade_mp,
            quantidade_estq=0,
            gms_mp=gms,
            pedidomin_mp=pedidomin,
            user_id=current_user.id
        )


        db.session.add(estoque)
        db.session.commit()

        return redirect(url_for('materiasPrimas'))

    materiasprimas = materiasprimas_model.MateriasPrimas.query.filter_by(user_id=current_user.id).all()
    materiaprima_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiaprima_schema.dump(materiasprimas)

    #GIRO MEDIO####

    config = config_model.Config.query.first()
    if config is not None:
        giro_medio = config.giro_medio
    else:
        giro_medio = 6

    return render_template('materiasprimas.html', materiasprimas = serialized_data_mp, giromedio=giro_medio)

@app.route('/delete-materiaprima/<int:id>', methods=['POST'])
def deleteMateriaPrima(id):
    # Get the MateriasPrimas object to delete
    materiasprimas = materiasprimas_model.MateriasPrimas.query.get_or_404(id)

    # Delete related records in the estoque table
    estoque_items = estoque_model.Estoque.query.filter_by(id_mp=id).all()
    for estoque_item in estoque_items:
        db.session.delete(estoque_item)

    # Commit the session to delete the related records
    db.session.commit()

    # Now, delete the MateriasPrimas object
    db.session.delete(materiasprimas)
    db.session.commit()

    return redirect(url_for('materiasPrimas', id=id))


@app.route('/edit-materiaprima/<int:id>', methods=['POST'])
def editMateriaPrima(id):
    if request.method == 'POST':
        # Get the MateriasPrimas object to edit
        materiasprimas = materiasprimas_model.MateriasPrimas.query.get_or_404(id)

        # Update attributes of the MateriasPrimas object
        materiasprimas.nome_mp = request.form.get('nome_mp')
        materiasprimas.unidade_mp = request.form.get('unidade_mp')
        materiasprimas.pesounitario_mp = request.form.get('pesounitario_mp')
        materiasprimas.pesototal_mp = request.form.get('pesototal_mp')
        materiasprimas.custo_mp = request.form.get('custo_mp')
        materiasprimas.departamento_mp = request.form.get('departamento_mp')
        materiasprimas.pedidomin_mp = request.form.get('pedidomin_mp')
        materiasprimas.gastomedio_mp = request.form.get('gastomedio_mp')

        # Convert cost and total weight to floats
        custo_mp_float = float(materiasprimas.custo_mp)
        pesototal_mp_float = float(materiasprimas.pesototal_mp)

        if pesototal_mp_float != 0:
            materiasprimas.custoemkg_mp = custo_mp_float / pesototal_mp_float

        # Commit the changes to the MateriasPrimas object
        db.session.commit()

        # Update corresponding values in the related Estoque table
        estoque_items = estoque_model.Estoque.query.filter_by(id_mp=id).all()
        for estoque_item in estoque_items:
            estoque_item.nome_mp = materiasprimas.nome_mp
            estoque_item.unidade_mp = materiasprimas.unidade_mp
            estoque_item.gms_mp = materiasprimas.gms_mp
            estoque_item.pedidomin_mp = materiasprimas.pedidomin_mp

        # Commit the changes to the related Estoque records
        db.session.commit()

        return redirect(url_for('materiasPrimas', id=id))

# INVENTARIO ############################################################################

@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    today_date = datetime.now()
    formatted_date = format_date(today_date, format='full', locale='pt')

    estoque = estoque_model.Estoque.query.filter_by(user_id=current_user.id).all()
    estoque_schema = EstoqueSchema(many=True)
    serialized_data_estq = estoque_schema.dump(estoque)

    materiasprimas = materiasprimas_model.MateriasPrimas.query.filter_by(user_id=current_user.id).all()
    materiasprimas_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiasprimas_schema.dump(materiasprimas)

    if request.method == 'POST':
        new_quantities = request.form.getlist('quantidade_estq')

        for index, invt in enumerate(estoque):
            id_mp=invt.id_mp
            nome_mp = invt.nome_mp
            old_quantity = invt.quantidade_estq
            new_quantity = new_quantities[index]

            #diference between old quantity and new quantity
            old_quantity_float = float(old_quantity)
            new_quantity_float = float(new_quantity)
            difference = new_quantity_float - old_quantity_float

            # Get current timestamp with microseconds
            #current_time = datetime.now().strftime('%Y-%m-%d // %H:%M:%S.%f')[:-3]
            current_time = datetime.now()

            modo = 'Registro Manual'

            # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table

            if difference != 0:
                #print(id_mp, current_time,old_quantity, new_quantity, difference)
                historico = historico_model.Historico(
                date_change=current_time,
                id_mp=id_mp,
                nome_mp=nome_mp,
                ultimaquantidade_hst=old_quantity,
                novaquantidade_hst=new_quantity,
                difference_hst=difference,
                modo_hst=modo,
                user_id=current_user.id
                )

                db.session.add(historico)

            invt.quantidade_estq = new_quantities[index]

        db.session.commit()


        return redirect(url_for('inventario'))

    historico = historico_model.Historico.query.filter_by(user_id=current_user.id).all()
    historico_schema = HistoricoSchema(many=True)
    serialized_data_hst = historico_schema.dump(historico)

    # Assuming 'Inventario' is your SQLAlchemy model
    available_months = db.session.query(func.strftime('%Y-%m', inventario_model.Inventario.data_invt)).distinct().all()

    # Extract the formatted months from the result
    available_months = [result[0] for result in available_months]

    current_month = datetime.now().strftime('%Y-%m')


    inventario = inventario_model.Inventario.query.filter_by(user_id=current_user.id).all()
    inventario_schema = InventarioSchema(many=True)


    # Separate compras into two lists based on estado_compras
    inventario_aberto = [invt for invt in inventario if invt.estado_invt == "Aberto"]
    inventario_fechado = [invt for invt in inventario if invt.estado_invt == "Fechado"]

    serialized_data_invtAberto = inventario_schema.dump(inventario_aberto)
    serialized_data_invtFechado = inventario_schema.dump(inventario_fechado)


    inventariodados = inventariodados_model.InventarioDados.query.filter_by(user_id=current_user.id).all()
    inventariodados_schema = InventarioDadosSchema(many=True)
    serialized_data_invtDados = inventariodados_schema.dump(inventariodados)



    return render_template('inventario.html',
                           historico=serialized_data_hst ,
                           estoque=serialized_data_estq,
                           today_date=formatted_date,
                            materiasprimas=serialized_data_mp,
                            datetime=datetime,
                            available_months=available_months,
                            inventarioAberto=serialized_data_invtAberto,
                            inventarioFechado=serialized_data_invtFechado,
                            inventarioDados=serialized_data_invtDados,
                            current_month=current_month
                            )

#########################################################################################################################################
# Translation dictionaries for months and days in Portuguese
MONTHS_PT = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

DAYS_PT = {
    0: "seg",
    1: "ter",
    2: "qua",
    3: "qui",
    4: "sex",
    5: "sáb",
    6: "dom"
}

def datetimeformat(value):
    if isinstance(value, str):
        try:
            # Adjust format string to match the datetime string format
            value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            # Handle the case where the value is not a valid datetime string
            value = datetime.now()
    formatted_date = value.strftime("%d/%m/%Y")
    day_of_week = DAYS_PT[value.weekday()]  # Get the day of the week in Portuguese
    return f"{formatted_date} ({day_of_week})"
app.jinja_env.filters['datetimeformat'] = datetimeformat

def custom_datetime_format(value):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    formatted_date = value.strftime("%Y-%m-%d (%H:%M)")
    return formatted_date
app.jinja_env.filters['custom_datetime_format'] = custom_datetime_format


###########################################################################################################################################

@app.route('/salvar_inventario', methods=['POST'])
def salvar_inventario():
    date_str = request.form['datePicker']
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    inventario = inventario_model.Inventario(
        data_invt=date_object,
        estado_invt='Aberto',
        user_id=current_user.id
        )
    db.session.add(inventario)
    db.session.commit()

    selected_items = request.form.getlist('selected_items')
    for item_id in selected_items:


        item = materiasprimas_model.MateriasPrimas.query.filter_by(id_mp=item_id).first()
        # Check if the item exists
        if item:
        # If the item exists, access its attributes
            nome_mp = item.nome_mp
            unidades_mp = item.unidade_mp
        else:
        # Handle the case where the item does not exist
        # You can log a message, skip this item, or handle it in any other appropriate way
            print(f"Item with nome_mp '{item_id}' does not exist in the database.")

        quantidade_estq = estoque_model.Estoque.query.filter_by(id_mp=item_id).first().quantidade_estq

        inventariodados = inventariodados_model.InventarioDados(
            id_invt=inventario.id_invt,
            data_invt=date_object,
            id_mp=item_id,
            nome_mp=nome_mp,
            unidade_mp=unidades_mp,
            quantidade_invtdados=0.0,
            quantidade_estq=quantidade_estq,
            user_id=current_user.id
            )
        db.session.add(inventariodados)
    db.session.commit()


    return redirect(url_for('inventario'))

@app.route('/fechar_inventario', methods=['POST'])
def fechar_inventario():

    new_quantities = request.form.getlist('quantidade_invtdados')
    id_mps = request.form.getlist('id_mp')
    id_invts = request.form.getlist('id_invt')


    for new_quantity, id_mp, id_invt in zip(new_quantities, id_mps, id_invts):
        estoque = estoque_model.Estoque.query.filter_by(id_mp=id_mp).first()

        inventario = inventario_model.Inventario.query.filter_by(id_invt=id_invt).first()
        inventario.estado_invt = 'Fechado'

        # Check if estoque is found
        if estoque:
            nome_mp = estoque.nome_mp
            old_quantity = estoque.quantidade_estq

            old_quantity_float = float(old_quantity)
            new_quantity_float = float(new_quantity)

            difference = new_quantity_float - old_quantity_float

        # Add history if there's a difference
            if difference != 0:
                current_time = datetime.now().strftime('%Y-%m-%d // %H:%M:%S.%f')[:-3]
                modo = 'Inventario'

                historico = historico_model.Historico(
                date_change=current_time,
                id_mp=id_mp,
                nome_mp=nome_mp,
                ultimaquantidade_hst=old_quantity,
                novaquantidade_hst=new_quantity,
                difference_hst=difference,
                modo_hst=modo,
                user_id=current_user.id
                )
                db.session.add(historico)

        # Update the quantity in estoque
        estoque.quantidade_estq = new_quantity

        #change the status of the inventory to 'Fechado'


        # Commit changes to the database
        db.session.commit()
    return redirect(url_for('inventario'))







## PEDIDO DE COMPRAS ###################################################################################################################

@app.route('/compras', methods=['GET', 'POST'])
@login_required
def compras():

    fornecedores = fornecedores_model.Fornecedores.query.filter_by(user_id=current_user.id).all()
    fornecedores_schema = FornecedorSchema(many=True)


    estoque = estoque_model.Estoque.query.filter_by(user_id=current_user.id).all()
    estoque_schema = EstoqueSchema(many=True)


    compras = compras_model.Compras.query.filter_by(user_id=current_user.id).all()
    compras_schema = ComprasSchema(many=True)


    comprasdados = comprasdados_model.ComprasDados.query.filter_by(user_id=current_user.id).all()
    comprasdados_schema = ComprasDadosSchema(many=True)


    # Dictionary to store counts of fechado_comprasd for each compras_id
    fechado_comprasd_counts = {}

    # Counting fechado_comprasd values for each compras_id
    for dado in comprasdados:
        if dado.id_compras not in fechado_comprasd_counts:
            fechado_comprasd_counts[dado.id_compras] = []
        fechado_comprasd_counts[dado.id_compras].append(dado.fechado_comprasd)

    # Updating estado_compras for compras with all fechado_comprasd values set to 1
    for compra in compras:
        fechado_comprasd_values = fechado_comprasd_counts.get(compra.id_compras, [])
        if all(value == 1 for value in fechado_comprasd_values):
            compra.estado_compras = "Entregue"

    # Separate compras into two lists based on estado_compras
    compras_entregue = [compra for compra in compras if compra.estado_compras == "Entregue"]
    compras_pendente = [compra for compra in compras if compra.estado_compras == "Pendente"]

    # Commit the changes to the database
    db.session.commit()

    # Serialize the data for rendering in the template
    serialized_data_f = fornecedores_schema.dump(fornecedores)
    serialized_data_estq = estoque_schema.dump(estoque)
    serialized_data_compras_entregue = compras_schema.dump(compras_entregue)
    serialized_data_compras_pendente = compras_schema.dump(compras_pendente)
    serialized_data_comprasdados = comprasdados_schema.dump(comprasdados)

    return render_template('compras.html',
                           comprasEntregue=serialized_data_compras_entregue,
                           comprasPendente=serialized_data_compras_pendente,
                           comprasdados=serialized_data_comprasdados,
                           estoque=serialized_data_estq,
                           fornecedores=serialized_data_f)


@app.route('/salvar_compra', methods=['POST'])
def salvar_compra():

    global cost_per_unit, unidade_mp, departamento_comprasd
    print('salvando')
    #current_time = datetime.now().strftime('%Y-%m-%d // %H:%M:%S.%f')[:-3]
    current_time = datetime.now()

    compras = compras_model.Compras(
        data_compras=current_time,
        estado_compras='Pendente',
        user_id=current_user.id
        )
    db.session.add(compras)
    db.session.commit()

    selected_items = request.form.getlist('selected_items[]')
    for item_id in selected_items:
        item = materiasprimas_model.MateriasPrimas.query.filter_by(nome_mp=item_id).first()
# Check if the item exists
        if item:
        # If the item exists, access its attributes
            unidade_mp = item.unidade_mp
            cost_per_unit = item.custoemkg_mp
            departamento_comprasd = item.departamento_mp
        else:
        # Handle the case where the item does not exist
        # You can log a message, skip this item, or handle it in any other appropriate way
            print(f"Item with nome_mp '{item_id}' does not exist in the database.")
        # Fetch form data
        pedido_comprasd = Decimal(request.form.get(f'pedido_comprasd_{item_id}'))
        fornecedor_comprasd = request.form.get(f'fornecedores_{item_id}')

        forn = fornecedores_model.Fornecedores.query.filter_by(nome_fornecedor=fornecedor_comprasd).first()
        previsao = forn.tempo_entrega
        vencimento = forn.prazo_pagamento

        # Get today's date
        today = datetime.now()

        #previsao_comprasd = today + timedelta(days=previsao)
        #vencimento_comprasd = today + timedelta(days=vencimento)
        previsao_comprasd = datetime.strptime('2024-04-10T15:09:24', '%Y-%m-%dT%H:%M:%S')
        vencimento_comprasd = datetime.strptime('2024-04-10T15:09:24', '%Y-%m-%dT%H:%M:%S')

        #formatted_previsao = previsao_comprasd.strftime('%Y-%m-%dT%H:%M:%S')
        #formatted_vencimento = vencimento_comprasd.strftime('%Y-%m-%dT%H:%M:%S')

        #Calculate purchase order value
        valorpedido_comprasd = pedido_comprasd * cost_per_unit

        comprasdados = comprasdados_model.ComprasDados(
            id_compras = compras.id_compras,
            nome_mp = item_id,
            unidade_mp = unidade_mp,
            pedido_comprasd = pedido_comprasd,
            fornecedor_comprasd = fornecedor_comprasd,
            valorpedido_comprasd =  valorpedido_comprasd,
            departamento_comprasd=departamento_comprasd,
            previsao_comprasd = previsao_comprasd,
            vencimento_comprasd = vencimento_comprasd,
            fechado_comprasd = False,
            user_id=current_user.id
            )
        db.session.add(comprasdados)

    db.session.commit()

    return redirect(url_for('compras'))


@app.route('/fechar_compra', methods=['POST'])
def fechar_compra():

    selected_items = request.form.getlist('selected_dados[]')

    for item_id in selected_items:

        print(item_id)


        comprasd = comprasdados_model.ComprasDados.query.get_or_404(item_id)
        comprasd.fechado_comprasd = True
        #update stock
        estoquemp = estoque_model.Estoque.query.filter_by(nome_mp=comprasd.nome_mp).first()
        estoquequantidade = estoquemp.quantidade_estq
        estoquenome = estoquemp.nome_mp
        pedidoFloat = Decimal(comprasd.pedido_comprasd)
        estoquemp.quantidade_estq = estoquequantidade + pedidoFloat
        #add history

        # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table
        materiap = materiasprimas_model.MateriasPrimas.query.filter_by(nome_mp=estoquenome).first()
        id_materiaprima = materiap.id_mp if materiap else None

        # Get current timestamp with microseconds
        current_time = datetime.now()

        modo = 'Compra'

        historico = historico_model.Historico(
            date_change=current_time,
            id_mp=id_materiaprima,
            nome_mp=comprasd.nome_mp,
            ultimaquantidade_hst=estoquequantidade,
            novaquantidade_hst=estoquequantidade + pedidoFloat,
            difference_hst=pedidoFloat,
            modo_hst=modo,
            user_id=current_user.id
            )

        db.session.add(historico)
        db.session.commit()


    return redirect(url_for('compras'))
############################################################################### RUN APP ################################################

@app.route('/historico')
@login_required
def historico():
    historico = historico_model.Historico.query.filter_by(user_id=current_user.id).all()
    historico_schema = HistoricoSchema(many=True)
    serialized_data_hst = historico_schema.dump(historico)

    return render_template('historico.html', historico=serialized_data_hst)



# RECEITAS #####################################################


@app.route('/receitas', methods=['GET', 'POST'])
@login_required
def receitas():

    materiasprimas = materiasprimas_model.MateriasPrimas.query.all()
    materiasprimas_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiasprimas_schema.dump(materiasprimas)



    #if request
    if request.method == 'POST':
        nome_rct = request.form.get('nome_rct')

        descricao_rct = request.form.get('descricao_rct')
        preparo_rct = request.form.get('preparo_rct')



        receitas = receitas_model.Receitas(
            nome_rct=nome_rct,

            descricao_rct=descricao_rct,
            preparo_rct=preparo_rct,
            user_id=current_user.id
        )

        db.session.add(receitas)
        db.session.commit()

        # Handle ingredients insertion
        ingredient_count = int(request.form.get('ingredient_count'))

        for i in range(ingredient_count):
            id_mp = request.form.get(f'id_mp_{i}')
            quantidade = request.form.get(f'quantidade_{i}')
            unidade = request.form.get(f'unidade_{i}')

            #print(quantidade)

             # Fetch the nome_mp corresponding to the id_mp from the MP table
            materiaprima = (materiasprimas_model.MateriasPrimas.query.filter_by(id_mp=id_mp).first())
            nome_mp = materiaprima.nome_mp if materiaprima else None

            receita_mp = receitasmateriaprimas_model.ReceitaMateriasPrimas(
                id_rct=receitas.id_rct,
                id_mp=id_mp,
                nome_mp=nome_mp,
                quantidade=quantidade,
                unidade=unidade,
                user_id=current_user.id
            )

            db.session.add(receita_mp)
            db.session.commit()

        return redirect(url_for('receitas'))

    receitas = receitas_model.Receitas.query.all()
    receitas_schema = ReceitasSchema(many=True)
    serialized_data_rct = receitas_schema.dump(receitas)

    receitasmp = receitasmateriaprimas_model.ReceitaMateriasPrimas.query.all()
    receitasmp_schema = ReceitasMateriasPrimasSchema(many=True)
    serialized_data_rctmp = receitasmp_schema.dump(receitasmp)




    return render_template('receitas.html',
    materiasprimas=serialized_data_mp,
    receitas=serialized_data_rct,
    receitasmp=serialized_data_rctmp)


#EDIT
@app.route('/edit-receita/<int:id>', methods=['POST'])
def editReceita(id):
    if request.method == 'POST':
        receitas = receitas_model.Receitas.query.get_or_404(id)
        receitas.nome_rct = request.form.get('nome_rct')
        receitas.descricao_rct = request.form.get('descricao_rct')
        receitas.preparo_rct = request.form.get('preparo_rct')
        #receitas.id_clt = request.form.get('id_clt')



        db.session.commit()
        return redirect(url_for('receitas', id=id))

#DELETE
@app.route('/delete-receita/<int:id>', methods=['POST'])
def deleteReceita(id):  # Fetch the receitas record
    receitas = receitas_model.Receitas.query.get_or_404(id)
    try:
        # Delete child records from ReceitaMateriasPrimas table
        receitasmateriaprimas_model.ReceitaMateriasPrimas.query.filter_by(id_rct=id).delete()
        
        # Delete the parent record from Receitas table
        db.session.delete(receitas)
        db.session.commit()
    except IntegrityError:
        # If there's an integrity error, rollback changes and abort with error message
        db.session.rollback()
        abort(500, "Cannot delete or update a parent row: a foreign key constraint fails")
    
    return redirect(url_for('receitas', id=id) )
   


## PRODUCAO ############################################################################################################

@app.route('/produzir_receita', methods=['POST'])
def produzir_receita():
    # Get the recipe id and quantity from the form data
    id_rct = request.form.get('id_rct')
    quantidade = request.form.get('quantidade')

    # Get the recipe from the database
    receita = receitas_model.Receitas.query.get(id_rct)

    # Check if the recipe exists
    if not receita:
        return "Receita não encontrada", 404

    # Get the ingredients for the recipe
    ingredientes = receitasmateriaprimas_model.ReceitaMateriasPrimas.query.filter_by(id_rct=id_rct).all()

    # Check if each ingredient is available in the necessary quantity
    for ingrediente in ingredientes:
        estoque_item = estoque_model.Estoque.query.filter_by(id_mp=ingrediente.id_mp).first()
        if estoque_item.quantidade_estq < ingrediente.quantidade * quantidade:
            return f"Não há quantidade suficiente de {ingrediente.nome_mp} em estoque", 400

    # If all ingredients are available, subtract from the stock and update the inventory
    for ingrediente in ingredientes:
        estoque_item = estoque_model.Estoque.query.filter_by(id_mp=ingrediente.id_mp).first()
        estoque_item.quantidade_estq -= ingrediente.quantidade * quantidade

        # Update the inventory
        inventariodados = inventariodados_model.InventarioDados.query.filter_by(id_mp=ingrediente.id_mp).first()
        inventariodados.quantidade_invtdados = estoque_item.quantidade_estq

        # Register the production in the history
        historico = historico_model.Historico(
            date_change=datetime.now(),
            id_mp=ingrediente.id_mp,
            nome_mp=ingrediente.nome_mp,
            ultimaquantidade_hst=estoque_item.quantidade_estq + ingrediente.quantidade * quantidade,
            novaquantidade_hst=estoque_item.quantidade_estq,
            difference_hst=-ingrediente.quantidade * quantidade,
            modo_hst='Produção',
            user_id=current_user.id
        )
        db.session.add(historico)

    db.session.commit()

    return "Receita produzida com sucesso", 200


if __name__ == '__main__':

    app.run()