from app import db

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    implantation = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    billing_address = db.Column(db.String(250), nullable=False)
    shipping_address = db.Column(db.String(250), nullable=False)
    reason = db.Column(db.String(250), nullable=False)
    pdf_data = db.Column(db.LargeBinary, nullable=True)  # Ajout de la colonne pdf_data