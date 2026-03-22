# Flask version du site (dossier Update)

## Installation

```bash
cd Digital-GetService-main
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration de l'environnement

### Développement local
1. Copier `.env.example` en `.env`
2. Compléter les variables d'environnement **notamment:**
   - `ADMIN_BOOTSTRAP_EMAIL` - Email de l'administrateur initial
   - `ADMIN_BOOTSTRAP_PASSWORD` - Mot de passe de l'administrateur (min 8 caractères)
   - `ADMIN_BOOTSTRAP_NAME` - Nom de l'administrateur
   - `FLASK_SECRET_KEY` - Clé secrète Flask

```bash
cp .env.example .env
# Editer .env avec vos valeurs
```

## Lancer l'application

```bash
python app.py
```

Application disponible sur `http://127.0.0.1:5000/site/accueil`.

Back-office: `http://127.0.0.1:5000/backoffice/login`

## Redis (rate-limit + sessions)

Lancer Redis localement:
```bash
docker compose up -d
```

Par defaut, `REDIS_URL` est utilise pour le rate-limit et les sessions.

## Production (.env + serveur WSGI)

### 1. Configuration du fichier .env
Créer un fichier `.env` à la racine avec vos paramètres de production:
```bash
cp .env.example .env
# Editer .env avec vos valeurs de production
```

**Variables critiques à configurer:**
- `ADMIN_BOOTSTRAP_EMAIL` et `ADMIN_BOOTSTRAP_PASSWORD` - Identifiants admin initiaux
- `FLASK_SECRET_KEY` - Clé secrète robuste (générer avec: `python -c "import secrets; print(secrets.token_hex(32))"`)
- `MAIL_SMTP_*` - Configuration du serveur email
- `HCAPTCHA_SITE_KEY` et `HCAPTCHA_SECRET_KEY` - Pour la capture CAPTCHA
- `SESSION_COOKIE_SECURE=1` - Pour HTTPS
- `DATABASE_URL` - Si personnalisé

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer avec un serveur WSGI

**Linux/Docker avec gunicorn:**
```bash
gunicorn -w 2 --threads 4 --timeout 120 -b 0.0.0.0:5000 app:app
```

Pour WebSockets en production:
```bash
gunicorn -k gevent -w 1 -b 0.0.0.0:5000 app:app
```

**Windows avec waitress:**
```bash
waitress-serve --listen=0.0.0.0:5000 app:app
```

### 4. Sécurité
⚠️ **IMPORTANT:**
- Ne JAMAIS commiter le fichier `.env` (protégé par `.gitignore`)
- Utiliser un gestionnaire de secrets pour les vraies clés en production
- Changer `ADMIN_BOOTSTRAP_PASSWORD` après la première connexion
- Générer une nouvelle `FLASK_SECRET_KEY` pour chaque déploiement

## 🔍 SEO et Moteurs de Recherche

L'application est optimisée pour les moteurs de recherche:

### Fichiers SEO
- `/sitemap.xml` - Découvrabilité des pages par Google
- `/robots.txt` - Instructions pour les crawlers
- Meta tags complets - Title, description, keywords par page
- Open Graph - Partages optimisés sur réseaux sociaux
- Structured Data (JSON-LD) - Google comprend mieux votre contenu

### Pour que Google vous trouve:
1. **Google Search Console** (https://search.google.com/search-console/)
   - Vérifier votre domaine
   - Soumettre `/sitemap.xml`
   - Voir les erreurs d'indexation

2. **Bing Webmaster Tools** (https://www.bing.com/webmasters/)
   - Ajouter votre site
   - Soumettre le sitemap

3. **Contenu**:
   - Google préfère le contenu de qualité
   - Enrichir vos pages avec du texte unique
   - Ajouter des images avec balises `alt` descriptives

Voir `SEO_GUIDE.md` pour plus de détails sur l'optimisation.

## 📚 Documentation

- **`HOSTING_SETUP.md`** ⭐ **Pour votre situation: BD hébergée sur serveur (LIRE EN PREMIER)**
- **`DEPLOYMENT_CHECKLIST.md`** ⭐ **Avant de déployer: vérifier tout est OK**
- **`SETUP_QUICK_START.md`** - Guide rapide configuration BD distante
- `SEO_GUIDE.md` - Guide complet SEO
- `EMAIL_CONFIG.md` - Configuration email SMTP
- `ENV_SETUP.md` - Configuration des variables d'environnement
- `DATABASE_CONFIG.md` - Configuration BDs distantes (PostgreSQL, MySQL)
- `DATABASE_SCHEMA.md` - Structure des tables et modèles
- `ORM_EXAMPLES.md` - Exemples d'utilisation SQLAlchemy (CRUD, requêtes)
- `CHAT_SYSTEM.md` - Système de chat bidirectionnel

## 🎯 Votre Workflow

1. **Lire:** [`HOSTING_SETUP.md`] - Explique vote situation exacte
2. **Configurer:** Lancer `python setup_database.py`
3. **Vérifier:** `python test_database.py`
4. **Tester:** `python app.py` et `http://localhost:5000`
5. **Checklist:** [`DEPLOYMENT_CHECKLIST.md`] - Avant déploiement
6. **Déployer:** Sur votre hébergement

## 🗄️ Base de Données (ORM SQLAlchemy)

### Par défaut: SQLite local
```bash
python app.py  # Créera base_donnees.sqlite
```

### Pour une BD distante hébergée (PostgreSQL, MySQL)

**⚡ Utiliser le script automatique:**
```bash
python setup_database.py
```

Le script:
- ✅ Construit `DATABASE_URL` automatiquement
- ✅ Teste la connexion
- ✅ **Crée les 12 tables automatiquement**
- ✅ Sauvegarde dans `.env`

**Manuel:** Voir `SETUP_QUICK_START.md` pour configuration step-by-step.

Voir `DATABASE_CONFIG.md` pour le guide complet.

