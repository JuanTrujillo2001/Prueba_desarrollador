from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificacion = request.form.get('identificacion')
        contrasena = request.form.get('password')
        
        user = User.query.filter_by(identificacion=identificacion).first()
        if user:
            if check_password_hash(user.contrasena, contrasena):
                flash('accedido con éxito!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Contraseña Incorrecta, Pruebe otra vez', category='danger')
        else:
            flash('Identificacion no existe', category='danger')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        Nombre = request.form.get('Nombre')
        Apellido = request.form.get('Apellido')
        identificacion = request.form.get('identificacion')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(identificacion=identificacion).first()

        if user:
            flash('Identificacion ya existe', category='danger')
        elif len(Nombre) < 2:
            flash('Nombre debe ser mayor que 1 caracteres.', category='error')
        elif len(Apellido) < 4:
            flash('Apellido debe ser mayor que 3 caracteres.', category='error')
        elif len(identificacion) < 1:
            flash('Debes colocar una identificacion', category='error')
        elif password1 != password2:
            flash('Las contraseña no son iguales', category='error')
        elif len(password1) < 7:
            flash('Contraseña debe ser mayor que 7 caracteres.', category='error')
        else:
            new_user = User(nombre=Nombre, apellido=Apellido, identificacion=identificacion, contrasena=generate_password_hash((password1), method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Cuenta Creada!', category='success')
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)

