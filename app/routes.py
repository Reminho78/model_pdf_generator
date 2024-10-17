from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Form

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/form')
def form_view():
    return render_template('form.html')

@main.route('/list')
def list_forms():
    forms = Form.query.all()  # Correction : Utilisation de Form avec une majuscule
    return render_template('list.html', forms=forms)

@main.route('/submit_form', methods=['POST'])
def submit_form():
    implantation = request.form['implantation']
    creation_date = request.form['creation_date']
    billing_address = request.form['billing_address']
    shipping_address = request.form['shipping_address']
    reason = request.form['reason']

    # Vérifie si "Autre motif" est sélectionné et utilise la valeur de other_reason
    if reason == 'Autre motif':
        reason = request.form['other_reason']  # Utilise la valeur d'other_reason

    new_form = Form(implantation=implantation,  # Correction : Utilisation de Form avec une majuscule
                    creation_date=creation_date,
                    billing_address=billing_address,
                    shipping_address=shipping_address, 
                    reason=reason)
    db.session.add(new_form)
    db.session.commit()
    return redirect(url_for('main.list_forms'))

@main.route('/delete_form/<int:form_id>', methods=['POST'])
def delete_form(form_id):
    form = Form.query.get(form_id)  # Correction : Utilisation de Form avec une majuscule
    if form:
        db.session.delete(form)
        db.session.commit()
    return redirect(url_for('main.list_forms'))