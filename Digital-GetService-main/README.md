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
