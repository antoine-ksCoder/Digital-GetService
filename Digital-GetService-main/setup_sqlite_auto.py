#!/usr/bin/env python3
"""Setup non-interactif pour SQLite (pour test/déploiement)"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Utiliser DATABASE_URL du .env existant ou fallback SQLite
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv("DATABASE_URL", "").strip()
if not database_url:
    database_url = f"sqlite:///{Path(__file__).parent / 'base_donnees.sqlite'}"

print("=" * 70)
print("🚀 SETUP AUTOMATIQUE - BASE DE DONNÉES SQLITE")
print("=" * 70)
print(f"\n📍 URL: {database_url[:60]}...")

from sqlalchemy import create_engine, inspect, text

print("\n1️⃣  Test de connexion...")
try:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("   ✅ Connexion réussie!")
    engine.dispose()
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

print("\n2️⃣  Création des tables...")
try:
    from app import create_app, db
    app = create_app()
    
    with app.app_context():
        db.create_all()
        db.session.remove()
        db.engine.dispose()
        
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"   ✅ {len(tables)} table(s) créée(s)")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ SETUP COMPLET - Base de données prête!")
print("=" * 70)
print("\n🚀 Commandes suivantes:")
print("   python app.py          # Démarrer l'application")
print("   python test_database.py # Tester les connexions")
