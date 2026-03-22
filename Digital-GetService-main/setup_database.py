#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour configurer et initialiser une base de données distante
Construit l'URL de connexion, teste la connexion, et crée les tables
"""

import os
import sys
from pathlib import Path

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv, set_key
from sqlalchemy import create_engine, inspect, text

def build_database_url():
    """
    Construit la chaîne de connexion DATABASE_URL
    Supporte SQLite (local) ou distante (MySQL/PostgreSQL)
    """

    print("=" * 70)
    print("🔧 CONFIGURATION BASE DE DONNÉES")
    print("=" * 70)

    print("\n📋 Choisir le type de base de données:\n")
    print("1️⃣  SQLite (local) - Recommandé pour développement")
    print("2️⃣  MySQL (distante)")
    print("3️⃣  PostgreSQL (distante)")

    db_choice = input("\nChoisir (1/2/3): ").strip()

    if db_choice == "1":
        return build_sqlite_url()
    elif db_choice == "2":
        return build_mysql_url()
    elif db_choice == "3":
        return build_postgresql_url()
    else:
        print("❌ Choix invalide. Choisir 1, 2 ou 3")
        return None


def build_sqlite_url():
    """
    Configure une base de données SQLite locale
    """
    print("\n" + "=" * 70)
    print("🗄️  CONFIGURATION SQLite LOCAL")
    print("=" * 70)

    default_path = str(Path(__file__).parent.parent / "base_donnees.sqlite")
    db_path = input(f"\nChemin de la BD SQLite (défaut: {default_path}): ").strip()
    if not db_path:
        db_path = default_path

    # Créer le répertoire si nécessaire
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    database_url = f"sqlite:///{db_file.resolve()}"
    print(f"\n✅ URL SQLite: {database_url}")
    return database_url


def build_mysql_url():
    """
    Configure une base de données MySQL distante
    """
    print("\n" + "=" * 70)
    print("📍 CONFIGURATION MySQL DISTANTE")
    print("=" * 70)

    print("\n📋 Veuillez fournir les informations de connexion:\n")

    host = input("Adresse hôte (ex: db.example.com): ").strip()
    if not host:
        print("❌ Adresse hôte requise")
        return None

    port_input = input("Port (défaut 3306): ").strip()
    port = port_input if port_input else 3306

    username = input("Nom d'utilisateur: ").strip()
    if not username:
        print("❌ Utilisateur requis")
        return None

    password = input("Mot de passe: ").strip()

    database = input("Nom de la base de données: ").strip()
    if not database:
        print("❌ Nom BD requis")
        return None

    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    return database_url


def build_postgresql_url():
    """
    Configure une base de données PostgreSQL distante
    """
    print("\n" + "=" * 70)
    print("📍 CONFIGURATION PostgreSQL DISTANTE")
    print("=" * 70)

    print("\n📋 Veuillez fournir les informations de connexion:\n")

    host = input("Adresse hôte (ex: db.example.com): ").strip()
    if not host:
        print("❌ Adresse hôte requise")
        return None

    port_input = input("Port (défaut 5432): ").strip()
    port = port_input if port_input else 5432

    username = input("Nom d'utilisateur: ").strip()
    if not username:
        print("❌ Utilisateur requis")
        return None

    password = input("Mot de passe: ").strip()

    database = input("Nom de la base de données: ").strip()
    if not database:
        print("❌ Nom BD requis")
        return None

    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    return database_url


def test_connection(database_url):
    """
    Teste la connexion à la base de données
    """
    print("\n" + "=" * 70)
    print("🔗 TEST DE CONNEXION")
    print("=" * 70)

    # Masquer le mot de passe dans l'affichage
    display_url = database_url
    if "@" in display_url and "sqlite" not in display_url:
        parts = display_url.split("@")
        user_pass = parts[0].rsplit("://", 1)[1]
        if ":" in user_pass:
            user = user_pass.split(":")[0]
            display_url = parts[0].rsplit("://", 1)[0] + f"://{user}:***@" + parts[1]

    print(f"\n📍 Connexion à: {display_url}")

    try:
        # Charger le .env temporaire
        os.environ["DATABASE_URL"] = database_url

        # Créer un moteur de connexion dédié
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={
                "connect_timeout": 10,
                "read_timeout": 30,
                "write_timeout": 30,
            } if "sqlite" not in database_url else {},
        )

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Connexion réussie!")

            # Afficher le dialecte
            dialect = engine.dialect.name
            print(f"🗄️  Dialecte détecté: {dialect}")

            # Vérifier l'existence des tables
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if tables:
                print(f"\n⚠️  {len(tables)} table(s) trouvée(s):")
                for table in sorted(tables):
                    print(f"  - {table}")
            else:
                print("\n✅ Base de données vide (aucune table)")

        engine.dispose()
        return True

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False


def create_tables(database_url):
    """
    Crée toutes les tables à partir des modèles SQLAlchemy
    """
    print("\n" + "=" * 70)
    print("📝 CRÉATION DES TABLES")
    print("=" * 70)

    try:
        os.environ["DATABASE_URL"] = database_url

        from app import create_app, db

        app = create_app()

        with app.app_context():
            print("\n🔨 Création des tables en cours...")

            # Créer toutes les tables
            db.create_all()

            # Nettoyer la session pour éviter réutilisation de connexion périmée
            db.session.remove()
            db.engine.dispose()

            print("✅ Tables créées avec succès!")

            # Afficher les tables créées
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            print(f"\n📊 {len(tables)} table(s) créée(s):")
            for table in sorted(tables):
                columns = inspector.get_columns(table)
                print(f"  ✓ {table} ({len(columns)} colonnes)")

            return True

    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def save_to_env(database_url):
    """
    Sauvegarde la DATABASE_URL dans le fichier .env
    """
    print("\n" + "=" * 70)
    print("💾 SAUVEGARDE CONFIGURATION")
    print("=" * 70)

    try:
        env_path = Path(__file__).parent / ".env"

        # Lire le fichier .env actuel
        load_dotenv(env_path)

        # Ajouter/mettre à jour DATABASE_URL
        set_key(str(env_path), "DATABASE_URL", database_url)

        print(f"\n✅ DATABASE_URL sauvegardée dans .env")
        print(f"   Fichier: {env_path}")

        # Afficher la ligne dans le fichier
        print(f"\n📄 Contenu ajouté:")
        print(f"   DATABASE_URL={database_url[:50]}...")

        return True

    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False


def main():
    """
    Flux principal
    """

    # Vérifier si DATABASE_URL est déjà définie dans .env
    existing_url = os.getenv("DATABASE_URL", "").strip()
    if existing_url:
        print("=" * 70)
        print("🔍 BASE DE DONNÉES DÉTECTÉE")
        print("=" * 70)
        print(f"\n✅ DATABASE_URL déjà configurée dans .env")
        
        choice = input("\nVoulez-vous utiliser cette configuration? (oui/non): ").strip().lower()
        if choice not in ("oui", "o", "yes", "y"):
            database_url = build_database_url()
            if not database_url:
                return False
        else:
            database_url = existing_url
    else:
        # Étape 1: Construire l'URL
        database_url = build_database_url()
        if not database_url:
            return False

    print(f"\n✅ URL construite: {database_url[:60]}...")

    # Étape 2: Tester la connexion
    if not test_connection(database_url):
        print("\n⚠️  Vérifiez vos identifiants et réessayez")
        return False

    # Étape 3: Créer les tables
    confirm = input(
        "\n❓ Créer automatiquement les tables? (oui/non): "
    ).strip().lower()
    if confirm not in ("oui", "o", "yes", "y"):
        print("❌ Annulé")
        return False

    if not create_tables(database_url):
        print("\n⚠️  Tables non créées")
        return False

    # Étape 4: Sauvegarder dans .env
    if existing_url != database_url:
        confirm = input(
            "\n❓ Sauvegarder DATABASE_URL dans .env? (oui/non): "
        ).strip().lower()
        if confirm not in ("oui", "o", "yes", "y"):
            print("\n⚠️  Non sauvegardée. À configurer manuellement:")
            print(f"   DATABASE_URL={database_url}")
            return False

        if not save_to_env(database_url):
            print("\n⚠️  Non sauvegardée. À configurer manuellement:")
            print(f"   DATABASE_URL={database_url}")
            return False

    # Succès!
    print("\n" + "=" * 70)
    print("✅ CONFIGURATION COMPLÈTE!")
    print("=" * 70)
    print("\n🚀 Prochaines étapes:")
    print("   1. Redémarrer l'application: python app.py")
    print("   2. Tester: python test_database.py")
    print("   3. Déployer sur l'hébergement")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Annulé par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
