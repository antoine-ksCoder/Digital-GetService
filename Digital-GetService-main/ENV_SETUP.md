# Guide de Configuration - Fichier .env

## 📋 Vue d'ensemble

Le fichier `.env` centralise toutes les variables d'environnement sensibles et de configuration de l'application. Il est **jamais commité** au dépôt git pour des raisons de sécurité.

## 🔐 Configuration initiale

### 1. Copier le template
```bash
cp .env.example .env
```

### 2. Remplir les credentials administrateur

Les champs obligatoires au premier démarrage:

```env
# Email de l'administrateur initial
ADMIN_BOOTSTRAP_EMAIL=your-admin-email@example.com

# Mot de passe (minimum 8 caractères, doit être robuste)
# ⚠️ Sera utilisé une seule fois à la première initialisation
ADMIN_BOOTSTRAP_PASSWORD=YourSecure@Password123

# Nom affiché
ADMIN_BOOTSTRAP_NAME=Administrateur
```

**Fonctionnement:** Ces variables ne sont utilisées que si la base de données est vide (premier démarrage). Une fois l'admin créé, les variables d'environnement n'ont plus d'effet.

### 3. Clé secrète Flask

```env
# Clé secrète pour les sessions et tokens
# 🔒 DOIT être unique et aléatoire en production
FLASK_SECRET_KEY=your-secret-key-here
```

**Générer une clé sécurisée:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📧 Configuration Email (SMTP)

```env
# Activer/désactiver l'envoi d'emails
MAIL_ENABLED=1

# Serveur SMTP
MAIL_SMTP_HOST=smtp.gmail.com
MAIL_SMTP_PORT=587

# Identifiants
MAIL_SMTP_USERNAME=your-email@gmail.com
MAIL_SMTP_PASSWORD=your-app-password  # Pas votre password Gmail directement!

# Configuration TLS/SSL
MAIL_SMTP_USE_TLS=1      # Pour port 587
MAIL_SMTP_USE_SSL=0      # Pour port 465, mettre 1

# Adresses
MAIL_FROM_EMAIL=no-reply@digital-get.com
CONTACT_EMAIL=contact@digital-get.com
```

### Exemples courants:

**Gmail:**
```env
MAIL_SMTP_HOST=smtp.gmail.com
MAIL_SMTP_PORT=587
MAIL_SMTP_USERNAME=your-email@gmail.com
MAIL_SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Mot de passe d'application Google
MAIL_SMTP_USE_TLS=1
MAIL_SMTP_USE_SSL=0
```

**Outlook/Hotmail:**
```env
MAIL_SMTP_HOST=outlook.office365.com
MAIL_SMTP_PORT=587
MAIL_SMTP_USERNAME=your-email@outlook.com
MAIL_SMTP_PASSWORD=your-password
MAIL_SMTP_USE_TLS=1
MAIL_SMTP_USE_SSL=0
```

**SendGrid:**
```env
MAIL_SMTP_HOST=smtp.sendgrid.net
MAIL_SMTP_PORT=587
MAIL_SMTP_USERNAME=apikey
MAIL_SMTP_PASSWORD=SG.xxxxxxxxxxxxx  # Clé API SendGrid
MAIL_SMTP_USE_TLS=1
MAIL_SMTP_USE_SSL=0
```

## 💾 Base de données

```env
# URL personnalisée (lasisse vide pour SQLite)
DATABASE_URL=

# Chemin du fichier SQLite (ignoré si DATABASE_URL est défini)
DB_PATH=base_donnees.sqlite
```

**PostgreSQL (si utilisé):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🔑 hCaptcha (Prévention de spam)

```env
# Tokens depuis https://dashboard.hcaptcha.com
HCAPTCHA_SITE_KEY=your-site-key
HCAPTCHA_SECRET_KEY=your-secret-key

# Si vides, le captcha est automatiquement désactivé
```

## 🔄 Redis + Sessions

```env
# URL Redis (pour rate-limiting et sessions)
# Vide = désactivé
REDIS_URL=redis://localhost:6379/0

# Type de session: filesystem ou redis
SESSION_TYPE=filesystem

# Préfixe pour les clés de session Redis
SESSION_KEY_PREFIX=dgs:session:

# Rate limiting storage
RATELIMIT_STORAGE_URI=memory://
```

## 🚀 Variables de déploiement

```env
# Port d'écoute
PORT=5000

# Sécurité des cookies de session
SESSION_COOKIE_SECURE=0  # Mettre 1 en HTTPS
SESSION_COOKIE_SAMESITE=Lax

# Limite de taille de fichier upload
MAX_UPLOAD_MB=5

# WebSocket (chat)
CHAT_WS_URL=
```

## ⚠️ Bonnes pratiques

### ✅ À faire
- Générer des clés secrets aléatoires en production
- Utiliser des passwords robustes (min 12 chars avec majuscules, chiffres, symboles)
- Stocker le .env hors du dépôt git
- Utiliser `.env.example` pour la documentation
- Différencier les configs dev/staging/production
- Garder des valeurs de fallback raisonnables dans le code

### ❌ À éviter
- Commiter le fichier `.env`
- Partager les vrais credentials par email
- Utiliser les mêmes identifiants partout
- Mettre des secrets dans les logs
- Utiliser `ADMIN_BOOTSTRAP_PASSWORD` comme password permanent

## 🔄 Rotation des secrets

### Changer le mot de passe admin
1. Se connecter au backoffice admin
2. Aller dans la gestion des utilisateurs
3. Réinitialiser le mot de passe de l'admin
4. **Le fichier .env n'est plus utilisé après la première initialisation**

### Changer d'autres identifiants
1. Modifier le fichier `.env`
2. Redémarrer l'application
3. Vérifier les nouveaux identifiants dans les logs

## 🧪 Vérification

Pour vérifier que les variables d'environnement sont correctement chargées:

```python
# Dans Python REPL
import os
print(os.getenv('ADMIN_BOOTSTRAP_EMAIL'))
print(os.getenv('FLASK_SECRET_KEY'))
```

## 📱 Déploiement

### Heroku/Cloud platforms
Variables à configurer dans le dashboard:
```bash
heroku config:set ADMIN_BOOTSTRAP_EMAIL=admin@example.com
heroku config:set ADMIN_BOOTSTRAP_PASSWORD=SecurePass123
heroku config:set FLASK_SECRET_KEY=xxxxx
```

### Docker
Passer les variables via `docker run`:
```bash
docker run -e ADMIN_BOOTSTRAP_EMAIL=admin@example.com \
           -e ADMIN_BOOTSTRAP_PASSWORD=SecurePass123 \
           -e FLASK_SECRET_KEY=xxxxx \
           app:latest
```

Ou via fichier `.env`:
```bash
docker run --env-file .env app:latest
```

### Systemd/Linux
Créer `/etc/systemd/system/dgs-app.service`:
```ini
[Unit]
Description=Digital Get Service

[Service]
Type=notify
User=appuser
WorkingDirectory=/opt/app
EnvironmentFile=/opt/app/.env
ExecStart=/usr/bin/python3 -m gunicorn app:app

[Install]
WantedBy=multi-user.target
```

---

**Questions?** Consulter le README.md ou le fichier app.py pour comprendre comment chaque variable est utilisée.
