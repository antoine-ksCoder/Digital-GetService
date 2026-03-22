# 🗄️ Configuration Base de Données Distante

Votre application utilise **SQLAlchemy 2.0** - un ORM puissant qui supporte plusieurs bases de données.

## 📋 Bases de données supportées

| BD | URL Format | Statut |
|----|-----------|--------|
| **SQLite** | `sqlite:///path/to/db.sqlite` | ✅ Par défaut (local) |
| **PostgreSQL** | `postgresql://user:pass@host:port/dbname` | ✅ Recommandé (production) |
| **MySQL** | `mysql+pymysql://user:pass@host:port/dbname` | ✅ Supported |
| **MariaDB** | `mysql+pymysql://user:pass@host:port/dbname` | ✅ Supported |
| **SQL Server** | `mssql+pyodbc://user:pass@host/dbname` | ⚠️ Nécessite pyodbc |

---

## 🚀 Configuration PostgreSQL (Recommandé)

PostgreSQL est le meilleur choix pour la production.

### 1. Créer une base de données

**Option A: Hébergement cloud (Recommandé)**

- **Vercel PostgreSQL**: https://vercel.com/docs/storage/vercel-postgres
- **Railway.app**: https://railway.app/ (gratuit pour débuter)
- **Supabase**: https://supabase.com/ (PostgreSQL gratuit)
- **AWS RDS**: https://aws.amazon.com/rds/
- **Heroku Postgres**: https://www.heroku.com/postgres

**Option B: Serveur dédié**
```bash
# Sur votre serveur PostgreSQL
createdb digital_get_services
createuser dgs_user
psql -d digital_get_services -c "ALTER USER dgs_user WITH PASSWORD 'votre_mot_de_passe';"
```

### 2. Obtenir la chaîne de connexion

Elle ressemble à:
```
postgresql://user:password@host:port/dbname
```

**Exemple avec Supabase:**
```
postgresql://dgs_user:password123@db.xxxxx.supabase.co:5432/dgs_db
```

### 3. Installer le pilote PostgreSQL

```bash
pip install psycopg2-binary
# ou
pip install psycopg[binary]
```

(Déjà dans `requirements.txt`)

### 4. Configurer le `.env`

```env
DATABASE_URL=postgresql://dgs_user:password123@db.example.com:5432/digital_get_services

# Optionnel - pas besoin de DB_PATH si DATABASE_URL est défini
# DB_PATH=
```

### 5. Redémarrer l'application

```bash
python app.py
```

**SQLAlchemy créera automatiquement les tables!**

---

## 🐬 Configuration MySQL/MariaDB

### 1. Créer la base de données

```bash
mysql -u root -p
CREATE DATABASE digital_get_services CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dgs_user'@'%' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON digital_get_services.* TO 'dgs_user'@'%';
FLUSH PRIVILEGES;
```

### 2. Installer le pilote

```bash
pip install pymysql
```

### 3. Configurer le `.env`

```env
DATABASE_URL=mysql+pymysql://dgs_user:password123@db.example.com:3306/digital_get_services
```

### 4. Redémarrer

```bash
python app.py
```

---

## 🧪 Tester la connexion

### Via Flask Shell

```bash
python -c "from app import create_app, db; app = create_app(); print('✅ Connexion réussie' if db.engine.connect() else '❌ Erreur')"
```

### Via Query

```bash
python
```

```python
from app import create_app, db
from models import User

app = create_app()
with app.app_context():
    # Tester la connexion
    users = User.query.all()
    print(f"✅ {len(users)} utilisateurs trouvés")
    print(db.engine.url)  # Voir l'URL connectée
```

### Vérifier le type de BD

```python
with app.app_context():
    print(f"BD: {db.engine.dialect.name}")  # 'postgresql', 'mysql', etc.
    print(f"URL: {db.engine.url}")
```

---

## 🔧 Migration de données (SQLite → PostgreSQL)

Si vous avez des données en SQLite à migrer:

### 1. Installer l'outil de migration

```bash
pip install alembic
```

### 2. Exporter depuis SQLite

```bash
# Créer un dump SQLite
sqlite3 base_donnees.sqlite ".dump" > dump.sql
```

### 3. Importer dans PostgreSQL

```bash
# Adapter le dump au format PostgreSQL
psql -h host -U user -d database -f dump.sql
```

Ou utiliser un outil comme **pgAdmin** pour importer.

---

## 🔒 Sécurité - Variables d'environnement

**IMPORTANT:** Ne JAMAIS mettre de vrais identifiants dans le code!

```env
# ✅ BON - Fichier .env (protégé par .gitignore)
DATABASE_URL=postgresql://user:password@secure-host.com:5432/db

# ❌ MAUVAIS - Dans le code
DATABASE_URL="postgresql://user:password@host:5432/db"  # Visible sur GitHub!
```

### Production sécurisée

**Utiliser les variables d'environnement du serveur:**

```bash
# Heroku
heroku config:set DATABASE_URL="postgresql://..."

# Docker
docker run -e DATABASE_URL="postgresql://..." my-app

# Linux/systemd
export DATABASE_URL="postgresql://..."

# AWS Lambda / Azure Functions
Définir dans les variables d'environnement
```

---

## ⚙️ Configuration avancée

### Connection pooling

SQLAlchemy configure automatiquement le pool de connexions:

```python
# Dans app.py (déjà configuré)
app.config["SQLALCHEMY_ECHO"] = False  # True pour voir les requêtes SQL
app.config["SQLALCHEMY_RECORD_QUERIES"] = False
```

### Nombre de connexions maximum

```env
# Dans .env (optionnel)
DATABASE_POOL_SIZE=10
DATABASE_POOL_RECYCLE=3600
```

Puis dans app.py:
```python
pool_size = int(os.getenv("DATABASE_POOL_SIZE", "10"))
pool_recycle = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": pool_size,
    "pool_recycle": pool_recycle,
    "pool_pre_ping": True,
}
```

---

## 📊 Modèles SQLAlchemy

Votre application utilise des modèles SQLAlchemy comme:

```python
from models import User, Conversation, Message

# Créer
user = User(email="test@example.com", full_name="Test")
db.session.add(user)
db.session.commit()

# Lire
users = User.query.all()
user = User.query.filter_by(email="test@example.com").first()

# Mettre à jour
user.full_name = "Nouveau nom"
db.session.commit()

# Supprimer
db.session.delete(user)
db.session.commit()
```

**Fonctionnent identiquement avec n'importe quelle BD!**

---

## 🐛 Troubleshooting

### "Connection refused"
- Vérifier que le serveur BD est en ligne
- Vérifier l'URL: host, port, credentials
- Vérifier firewall/règles de sécurité

### "Authentication failed"
- Vérifier le username/password
- Vérifier que l'utilisateur a les droits

### "Database doesn't exist"
- Créer la BD: `CREATE DATABASE ...`
- Vérifier le nom dans l'URL

### Performance lente
- Vérifier la connexion réseau
- Ajouter des index sur les colonnes fréquemment cherchées
- Utiliser le connection pooling

### Trop de connexions ouvertes
```python
# Configurer le pool_recycle
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 3600,  # Recycler après 1h
    "pool_pre_ping": True,  # Tester la connexion avant usage
}
```

---

## 📈 Schéma de vos tables

Vos modèles créeront automatiquement ces tables:

- `user` - Utilisateurs
- `conversation` - Conversations de chat
- `message` - Messages
- `domaine_accueil` - Domaines du site
- `equipe_propos` - Équipe (À propos)
- `services_catalog` - Catalogue services
- `realisation_realisation` - Réalisations
- Et bien d'autres...

**Tout se crée automatiquement** `db.create_all()`

---

## ✅ Checklist pour passer en production

- [ ] Migrer vers PostgreSQL (ou MySQL)
- [ ] Configurer DATABASE_URL dans l'environnement
- [ ] Tester la connexion
- [ ] Vérifier les backups de BD
- [ ] Configurer le pool de connexions
- [ ] Monitorer les performances
- [ ] Mettre en place des alertes
- [ ] Plan de disaster recovery

---

## 🔗 Ressources

- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Supabase** (PostgreSQL gratuit): https://supabase.com/
- **Railway** (hosting gratuit): https://railway.app/

---

**Mise à jour:** 2026-03-21
