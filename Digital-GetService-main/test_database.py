#!/usr/bin/env python3
"""
Script de diagnostic pour la base de données
Teste la connexion et affiche les informations
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_database():
    """Test la connexion à la base de données"""

    print("=" * 60)
    print("🗄️  DIAGNOSTIC BASE DE DONNÉES")
    print("=" * 60)

    # Importer après avoir chargé .env
    from app import create_app, db

    app = create_app()

    with app.app_context():
        # Afficher la configuration
        db_url = str(db.engine.url)
        dialect = db.engine.dialect.name

        print(f"\n📊 Configuration actuelle:")
        print(f"  Dialecte: {dialect}")
        print(f"  URL: {db_url}")

        # Masquer le mot de passe dans l'affichage
        masked_url = db_url
        if "@" in masked_url:
            parts = masked_url.split("@")
            user_pass = parts[0].rsplit("://", 1)[1]
            if ":" in user_pass:
                user = user_pass.split(":")[0]
                masked_url = parts[0].rsplit("://", 1)[0] + f"://{user}:***@" + parts[1]
        print(f"  URL masquée: {masked_url}")

        # Tester la connexion
        print(f"\n🔗 Test de connexion...")
        try:
            connection = db.engine.connect()
            connection.close()
            print("  ✅ Connexion réussie!")
        except Exception as e:
            print(f"  ❌ Erreur de connexion: {e}")
            return False

        # Tester les tables
        print(f"\n📋 Tables détectées:")
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            if tables:
                for table in sorted(tables):
                    columns = inspector.get_columns(table)
                    print(f"  • {table} ({len(columns)} colonnes)")
                    # Afficher les colonnes principales
                    for col in columns[:3]:
                        col_type = str(col['type'])
                        nullable = "NULL" if col['nullable'] else "NOT NULL"
                        print(f"      - {col['name']}: {col_type} {nullable}")
                    if len(columns) > 3:
                        print(f"      ... et {len(columns) - 3} autres colonnes")
            else:
                print("  ⚠️  Aucune table trouvée (BD vide)")
        except Exception as e:
            print(f"  ❌ Erreur lors de la lecture des tables: {e}")
            return False

        # Tester les modèles
        print(f"\n📝 Test des modèles:")
        try:
            from models import User, Conversation, Message

            user_count = User.query.count()
            conv_count = Conversation.query.count()
            msg_count = Message.query.count()

            print(f"  • Utilisateurs: {user_count}")
            print(f"  • Conversations: {conv_count}")
            print(f"  • Messages: {msg_count}")

            if user_count > 0:
                first_user = User.query.first()
                print(f"    → Premier utilisateur: {first_user.email} ({first_user.role})")
        except Exception as e:
            print(f"  ⚠️  Impossible de lire les modèles: {e}")

        # Afficher les infos de la BD
        print(f"\n💾 Espace disque:")
        try:
            result = db.session.execute(db.text("SELECT version();"))
            version = result.scalar()
            print(f"  Serveur: {version}")
        except:
            pass

        # Configuration du pool
        print(f"\n🔌 Configuration du pool de connexions:")
        print(f"  Pool size: {db.engine.pool.size}")
        print(f"  Max overflow: {db.engine.pool.max_overflow}")
        print(f"  Pool recycle: {db.engine.pool._recycle if hasattr(db.engine.pool, '_recycle') else 'N/A'}")

        print(f"\n✅ Diagnostic complété avec succès!")
        return True

if __name__ == "__main__":
    try:
        success = test_database()
        sys.exit(0 if success else 1)
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("   Vérifiez que vous êtes dans le bon répertoire")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
