from flask import Blueprint, render_template, request, redirect, url_for
from flask import send_file, make_response
from app import db
import io
from app.models import Form
from app.pdf_generator import generate_pdf_with_template
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    print("Rendering home.html")  # Débogage
    return render_template('home.html')

@main.route('/form')
def form():
    return render_template('form.html')

@main.route('/list')
def list_forms():
    forms = Form.query.all()
    return render_template('list.html', forms=forms)

@main.route('/submit_form', methods=['POST'])
def submit_form():
    # Récupération des valeurs du formulaire
    implantation = request.form['implantation']
    creation_date = request.form['creation_date']
    billing_address = request.form['billing_address']
    shipping_address = request.form['shipping_address']

    # Vérifie si "Autre motif" est sélectionné et utilise la valeur de other_reason
    reason = request.form['reason']
    if reason == 'Autre motif':
        other_reason = request.form.get('other_reason')
        if other_reason:
            reason = other_reason  # Utilise la valeur de 'other_reason' si disponible
        else:
            return "Le champ 'Autre motif' est requis", 400

    # Crée un nouvel objet Form avec les données récupérées
    new_form = Form(
        implantation=implantation,
        creation_date=creation_date,
        billing_address=billing_address,
        shipping_address=shipping_address,
        reason=reason
    )

    # Ajouter le formulaire à la session de la base de données et committer
    db.session.add(new_form)
    db.session.commit()

    # Redirection vers la liste des formulaires après soumission
    return redirect(url_for('main.list_forms'))

@main.route('/delete_form/<int:form_id>', methods=['POST'])
def delete_form(form_id):
    form = Form.query.get(form_id)
    if form:
        db.session.delete(form)
        db.session.commit()
    return redirect(url_for('main.list_forms'))

@main.route('/generate_pdf/<int:form_id>', methods=['GET'])
def generate_pdf_route(form_id):
    form = Form.query.get_or_404(form_id)
    
    # Code pour générer le PDF
    pdf_data = generate_pdf_with_template(form)
    form.pdf_data = pdf_data
    form.pdf_generated = True  # Met à jour l'état pour indiquer que le PDF a été généré
    
    db.session.commit()
    
    # Télécharge le PDF
    return send_file(io.BytesIO(form.pdf_data), download_name='output.pdf', as_attachment=True)

@main.route('/download_pdf/<int:form_id>')
def download_pdf(form_id):
    form = Form.query.get_or_404(form_id)

    # Crée un dictionnaire des données du formulaire
    form_data = {
        'implantation': form.implantation,
        'creation_date': form.creation_date,
        'billing_address': form.billing_address,
        'shipping_address': form.shipping_address,
        'reason': form.reason
    }

    # Générer le PDF avec le modèle
    pdf_output = generate_pdf_with_template(form_data)

    # Crée une réponse Flask pour le téléchargement
    response = make_response(pdf_output.read())
    response.headers.set('Content-Disposition', 'attachment', filename='formulaire.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

@main.route('/list_pdfs', methods=['GET'])
def list_pdfs():
    # Récupérer le motif sélectionné dans la requête GET
    selected_reason = request.args.get('reason', '')

    # Filtrer les formulaires en fonction du motif s'il est sélectionné
    if selected_reason:
       forms = Form.query.filter(Form.reason == selected_reason, Form.pdf_data != None).all()
    else:
        forms = Form.query.filter(Form.pdf_data != None).all()

    # Afficher la page HTML avec la liste des formulaires filtrés
    return render_template('list_pdfs.html', forms=forms, selected_reason=selected_reason)