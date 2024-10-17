import os
import secrets

# Génère une clé secrète de 24 octets
secret_key = secrets.token_hex(24)
print(secret_key)
class Config:
    # Configuration de la base de données PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://remidubenard:ricketmorty@localhost:5432/facoto_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False