import io
from app import db
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter, PageMerge

def translate_month_to_french(date_str):
    # Dictionnaire pour mapper les mois anglais vers les mois français en majuscules
    months_translation = {
        "January": "JANVIER", "February": "FÉVRIER", "March": "MARS", "April": "AVRIL",
        "May": "MAI", "June": "JUIN", "July": "JUILLET", "August": "AOÛT",
        "September": "SEPTEMBRE", "October": "OCTOBRE", "November": "NOVEMBRE", "December": "DÉCEMBRE"
    }

    # Séparer la date en parties (jour, mois, année)
    parts = date_str.split(' ')

    # Traduire le mois si trouvé dans le dictionnaire
    translated_month = months_translation.get(parts[1], parts[1])  # Garde le mois en anglais si non trouvé

    # Recompose la date en français
    return f"{parts[0]} {translated_month} {parts[2]}"

def generate_pdf_with_template(form):
    # Chemin vers le modèle PDF
    template_path = 'app/static/fac_modele.pdf'

    # Charger le modèle PDF avec pdfrw
    template_pdf = PdfReader(template_path)
    template_page = template_pdf.pages[0]  # Si le PDF a une seule page

    # Créer un PDF temporaire avec FPDF
    pdf = FPDF()
    pdf.add_page()

    # Formatage de la date en anglais, puis traduction en français
    formatted_date = form.creation_date.strftime('%d %B %Y')
    translated_date = translate_month_to_french(formatted_date)

    # Ajouter les informations du formulaire
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(31, 56, 100)

    pdf.set_xy(25, 68)  # Position pour 'implantation'
    pdf.cell(0, 10, f"{form.implantation}", 0, 1)

    pdf.set_xy(125, 55)  # Position pour 'creation_date'
    pdf.cell(0, 10, f"{translated_date}", 0, 1)  # Utiliser la date traduite ici

    pdf.set_xy(130, 30)  # Position pour 'billing_address'
    pdf.cell(0, 10, f"{form.billing_address}", 0, 1)

    pdf.set_xy(38, 77)  # Position pour 'shipping_address'
    pdf.cell(0, 10, f"{form.shipping_address}", 0, 1)


    # ondition pour 'reason'
    if form.reason == "Fermeture des locaux":
        pdf.set_font("Arial", size=25)
        pdf.set_xy(8, 119)  # Position pour afficher la croix pour "Fermeture des locaux"
        pdf.cell(0, 10, "×", 0, 1)  # Afficher une petite croix
        pdf.set_font("Arial", size=11)  # Remettre la taille de police à 11
    elif form.reason == "Autre fournisseur":
        pdf.set_font("Arial", size=25)
        pdf.set_xy(8, 127)  # Position pour afficher la croix pour "Autre fournisseur"
        pdf.cell(0, 10, "×", 0, 1)  # Afficher une petite croix
        pdf.set_font("Arial", size=11)  # Remettre la taille de police à 11
    else:     
        pdf.set_font("Arial", size=25)
        pdf.set_xy(8, 135)  # Position pour afficher la croix pour "Fermeture des locaux"
        pdf.cell(0, 10, "×", 0, 1)  # Afficher une petite croix
        pdf.set_font("Arial", size=11)  # Remettre la taille de police à 11
        pdf.set_xy(42, 136)  # Position pour 'reason'
        pdf.cell(0, 10, f"{form.reason}", 0, 1)

    # Sauvegarder le PDF temporaire dans un buffer
    pdf_output = io.BytesIO()
    pdf_data = pdf.output(dest='S').encode('latin1')  # Générer le PDF en mémoire
    pdf_output.write(pdf_data)
    pdf_output.seek(0)

    # Convertir BytesIO en bytes pour être lu par pdfrw
    pdf_output_bytes = pdf_output.getvalue()

    # Lire le PDF temporaire avec pdfrw
    overlay_pdf = PdfReader(fdata=pdf_output_bytes)

    # Fusionner le modèle avec le contenu ajouté
    merger = PageMerge(template_page)
    merger.add(overlay_pdf.pages[0]).render()

    # Sauvegarder le PDF final dans un buffer
    output_pdf = io.BytesIO()
    PdfWriter(output_pdf, trailer=template_pdf).write()

    # Retourner le PDF binaire pour l'enregistrement dans la base de données
    form.pdf_data = output_pdf.getvalue()  # Ici on enregistre uniquement le PDF binaire
    db.session.commit()  # Mettre à jour la base de données uniquement pour pdf_data
    return form.pdf_data