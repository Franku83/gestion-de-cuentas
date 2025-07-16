from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    plataforma = db.Column(db.String(100))
    fecha_inicio = db.Column(db.String(10))
    fecha_fin = db.Column(db.String(10))
    usuario = db.Column(db.String(100))
    password = db.Column(db.String(100))
    status = db.Column(db.String(50))
    proveedor = db.Column(db.String(100))

    def mensaje_personalizado(self):
        return f"{self.cliente}, tu cuenta de {self.plataforma} vence el {self.fecha_fin}. ¡Renueva a tiempo para no perder el servicio!"

@app.route('/')
def index():
    cuentas = Account.query.all()
    return render_template('index.html', cuentas=cuentas)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nueva = Account(
            cliente=request.form['cliente'],
            plataforma=request.form['plataforma'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            usuario=request.form['usuario'],
            password=request.form['password'],
            status=request.form['status'],
            proveedor=request.form['proveedor']
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_account.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cuenta = Account.query.get_or_404(id)
    if request.method == 'POST':
        cuenta.cliente = request.form['cliente']
        cuenta.plataforma = request.form['plataforma']
        cuenta.fecha_inicio = request.form['fecha_inicio']
        cuenta.fecha_fin = request.form['fecha_fin']
        cuenta.usuario = request.form['usuario']
        cuenta.password = request.form['password']
        cuenta.status = request.form['status']
        cuenta.proveedor = request.form['proveedor']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_account.html', cuenta=cuenta)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    cuenta = Account.query.get_or_404(id)
    db.session.delete(cuenta)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/vencen_hoy')
def vencen_hoy():
    hoy = date.today().strftime('%Y-%m-%d')
    cuentas = Account.query.filter(Account.fecha_fin == hoy).all()
    return render_template('due_today.html', cuentas=cuentas, hoy=hoy)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)