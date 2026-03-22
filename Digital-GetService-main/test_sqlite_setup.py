#!/usr/bin/env python3
"""Test rapide de l'application avec SQLite"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au chemin
sys.path.insert(0, str(Path(__file__).parent))

# Configurer SQLite dans l'environnement
os.environ["DATABASE_URL"] = "sqlite:///test_db.sqlite"
os.environ["FLASK_SECRET_KEY"] = "test-key"

print("=" * 70)
print("🧪 TEST SQLITE - DÉMARRAGE APPLICATION")
print("=" * 70)

try:
    print("\n1️⃣  Importation de l'application...")
    from app import create_app, db
    print("   ✅ App importée")

    print("\n2️⃣  Création de l'app Flask...")
    app = create_app()
    print("   ✅ App créée")

    print("\n3️⃣  Context app et vérification de la BD...")
    with app.app_context():
        # Vérifier les tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"   ✅ Dialecte: {db.engine.dialect.name}")
        print(f"   ✅ Nombre de tables: {len(tables)}")
        
        if tables:
            print("\n   Tables présentes:")
            for table in sorted(tables):
                print(f"     - {table}")
        else:
            print("\n   ℹ️  Aucune table (création nécessaire)")
            print("\n4️⃣  Création des tables...")
            db.create_all()
            
            # Vérifier à nouveau
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"   ✅ {len(tables)} table(s) créée(s)")
            
            for table in sorted(tables):
                print(f"     - {table}")

    print("\n" + "=" * 70)
    print("✅ SUCCÈS - Base de données SQLite fonctionnelle!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

sys.exit(0)
