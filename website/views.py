from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User,Locaciones,Cargo
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        nombre = request.form.get('Nombre')
        apellido = request.form.get('Apellido')
        localizacionID = request.form.get('localID')
        cargoID = request.form.get('Cargo')
        estado = request.form.get('Estado')
        localidad = Locaciones.query.filter_by(id=localizacionID).first()
        cargos = Cargo.query.filter_by(id=cargoID).first()
        if localidad:
            if cargos:
                if estado == 'on':
                    estadito = True
                else:
                    estadito = None
                print(current_user.id)
                local= User.query.get(current_user.id)
                local.nombre = nombre
                local.apellido = apellido
                local.localizacionID = localizacionID
                local.cargoID = cargoID
                local.estado = estadito
                db.session.commit()
                flash('Actualizado con exito', category='success')
            else:
                flash('El cargo no existe', category='error') 
        else:
            flash('La localidad no existe', category='error')

    return render_template("home.html", user=current_user)

###########################
# Metodos de Localizacion #
###########################

@views.route('/deletelocate/<id>')
def deleteLocate(id):
    registro = Locaciones.query.get(id)
    db.session.delete(registro)
    db.session.commit()
        
    return redirect(url_for("views.localizaciones"))

@views.route('/updateLocate/<id>', methods=['GET', 'POST'])
def updateLocate(id):
    if request.method == "POST":
        localizacion = request.form.get('local')
        Local = Locaciones.query.filter_by(localizacion=localizacion).first()
        if len(localizacion) < 1:
            flash('Debe tener un nombre la locacion!', category='error')
        elif Local:
            porsi = Locaciones.query.filter_by(id=id).first()
            if porsi:
                estado = request.form.get('Estado')
                if estado == 'on':
                    estadito = True
                else:
                    estadito = None
                local= Locaciones.query.get(id)
                local.localizacion = localizacion
                local.estado = estadito
                db.session.commit() 
            else:
                flash('La localizacion ya existe', category='error')
        else:
            estado = request.form.get('Estado')
            if estado == 'on':
                estadito = True
            else:
                estadito = None
            local= Locaciones.query.get(id)
            local.localizacion = localizacion
            local.estado = estadito
            db.session.commit()

        return redirect(url_for("views.localizaciones"))

    locaciones = Locaciones.query.get(id)

    return render_template("updateLocate.html", user=current_user, locaciones=locaciones)

@views.route('/localizaciones', methods=['GET', 'POST'])
def localizaciones():
    Localizaciones = Locaciones.query.all()

    if request.method == 'POST':

        localizacion = request.form.get('local')
        Local = Locaciones.query.filter_by(localizacion=localizacion).first()

        if len(localizacion) < 1:
            flash('Debe tener un nombre la locacion!', category='error')
        elif Local:
            flash('La localizacion ya existe', category='error')
        else:
            new_note = Locaciones(localizacion=localizacion)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for("views.localizaciones"))
            flash('Locacion añadida!', category='success')

    return render_template("localizaciones.html", user=current_user, Localizaciones=Localizaciones)

#####################
# Metodos de Cargos #
#####################
    
@views.route('/deleteCargos/<id>')
def deleteCargos(id):
    registro = Cargo.query.get(id)
    db.session.delete(registro)
    db.session.commit()
        
    return redirect(url_for("views.cargos"))

@views.route('/updateCargos/<id>', methods=['GET', 'POST'])
def updateCargos(id):
    if request.method == "POST":
        cargo = request.form.get('local')
        Local = Cargo.query.filter_by(cargo=cargo).first()
        if len(cargo) < 1:
            flash('Debe tener un nombre el cargos!', category='error')
        elif Local:
            porsi = Cargo.query.filter_by(id=id).first()
            if porsi:
                estado = request.form.get('Estado')
                if estado == 'on':
                    estadito = True
                else:
                    estadito = None
                local= Cargo.query.get(id)
                local.cargo = Cargos
                local.estado = estadito
                db.session.commit() 
            else:
                flash('El cargo ya existe', category='error')
        else:
            estado = request.form.get('Estado')
            if estado == 'on':
                estadito = True
            else:
                estadito = None
            local= Cargo.query.get(id)
            local.cargo = Cargos
            local.estado = estadito
            db.session.commit()

        return redirect(url_for("views.cargos"))

    cargos= Cargo.query.get(id)

    return render_template("updateCargos.html", user=current_user, cargos=cargos)

@views.route('/cargos', methods=['GET', 'POST'])
def cargos():
    cargo = Cargo.query.all()

    if request.method == 'POST':

        cargos = request.form.get('cargo')
        Local = Cargo.query.filter_by(cargo=cargos).first()

        if len(cargos) < 1:
            flash('Debe tener un nombre el cargo!', category='error')
        elif Local:
            flash('El cargo ya existe', category='error')
        else:
            new_note = Cargo(cargo=cargos)
            db.session.add(new_note)
            db.session.commit()
            flash('Cargo añadida!', category='success')
            return redirect(url_for("views.cargos"))

    return render_template("cargos.html", user=current_user, cargo=cargo)