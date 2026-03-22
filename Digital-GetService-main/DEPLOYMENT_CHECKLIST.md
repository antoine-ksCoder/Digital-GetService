# ✅ Checklist Déploiement - Digital Get Services

À faire avant de déployer sur votre hébergeur.

---

## 📋 1. Configuration Locale

- [ ] **Application**
  - [ ] Cloner/télécharger le projet
  - [ ] Créer venv: `python -m venv .venv`
  - [ ] Activer venv: `.venv\Scripts\activate` (Windows)
  - [ ] Installer dépendances: `pip install -r requirements.txt`

- [ ] **Fichier `.env`**
  - [ ] Copier `.env.example` → `.env`
  - [ ] Remplir `ADMIN_BOOTSTRAP_EMAIL` et `ADMIN_BOOTSTRAP_PASSWORD`
  - [ ] Remplir `FLASK_SECRET_KEY` (générer: `python -c "import secrets; print(secrets.token_hex(32))"`)
  - [ ] Remplir informations email (si vous envoyez des messages de contact)

- [ ] **Email (optionnel mais recommandé)**
  - [ ] Configurer `MAIL_SMTP_*` variables
  - [ ] Tester: `python -c "from app import create_app; app = create_app(); print(app.config['MAIL_ENABLED'])"`

---

## 🗄️ 2. Base de Données

- [ ] **Connexion à la BD hébergée**
  - [ ] Obtenir infos auprès de l'hébergeur (host, port, user, password, dbname)
  - [ ] Lancer: `python setup_database.py`
  - [ ] Le script construit `DATABASE_URL` automatiquement
  - [ ] Le script crée les 12 tables

- [ ] **Vérification**
  - [ ] Lancer: `python test_database.py`
  - [ ] Vérifier: ✅ Connexion réussie
  - [ ] Vérifier: ✅ 12 tables créées
  - [ ] Vérifier: ✅ Ligne "Admin" créée par bootstrap

---

## 🧪 3. Tests Locaux

- [ ] **Application démarre**
  ```bash
  python app.py
  ```
  - [ ] Aller à: http://localhost:5000/site/accueil
  - [ ] Page charge correctement
  - [ ] Pas d'erreur 500

- [ ] **Pages principales accessibles**
  - [ ] `/site/accueil` - Accueil
  - [ ] `/site/services` - Services
  - [ ] `/site/propos` - À propos
  - [ ] `/site/realisation` - Réalisations
  - [ ] `/site/notreEquipe` - Équipe
  - [ ] `/site/formulaire` - Contact

- [ ] **Admin login**
  - [ ] Aller à: http://localhost:5000/backoffice/login
  - [ ] Se connecter avec `ADMIN_BOOTSTRAP_EMAIL` et `ADMIN_BOOTSTRAP_PASSWORD`
  - [ ] Dashboard admin charge
  - [ ] Menus disponibles: Users, Services, People, Projects, etc.

- [ ] **Chat (si configuré)**
  - [ ] Créer 2 utilisateurs test
  - [ ] Accéder à `/site/chat`
  - [ ] Les deux peuvent se voir et communiquer

- [ ] **Contact form** (si email configuré)
  - [ ] Aller à `/site/formulaire`
  - [ ] Remplir le formulaire
  - [ ] Cliquer "Envoyer"
  - [ ] Message "Succès" ou "Erreur" s'affiche
  - [ ] Email reçu? (vérifier `/backoffice/mail-test` en cas de doute)

---

## 🔐 4. Sécurité avant déploiement

- [ ] **Fichier `.env` ne sera PAS commité**
  - [ ] Vérifier `.gitignore` contient `.env`
  - [ ] Vérifier `.env` n'est pas dans les fichiers suivis: `git ls-files | grep env`

- [ ] **Secrets configurés**
  - [ ] `FLASK_SECRET_KEY` - Généré aléatoirement (pas "default")
  - [ ] `ADMIN_BOOTSTRAP_PASSWORD` - Fort (min 8 caractères, mix caractères)
  - [ ] Pas de credential en dur dans le code
  - [ ] `DATABASE_URL` - Dans `.env`, pas dans `app.py`

- [ ] **Mode debug désactivé**
  - [ ] Vérifier dans `app.py`: `debug=False` ou enlevé
  - [ ] `SQLALCHEMY_ECHO` = False

- [ ] **HTTPS préparé**
  - [ ] Si hébergeur supporte HTTPS: activer
  - [ ] Configurer: `SESSION_COOKIE_SECURE=1` pour production
  - [ ] Vérifier redirection HTTP → HTTPS

---

## 📦 5. Préparation déploiement

- [ ] **Fichiers prêts**
  - [ ] `requirements.txt` - À jour (pip freeze > requirements.txt)
  - [ ] `Procfile` - Pour Heroku si déploiement Heroku
  - [ ] `runtime.txt` - Version Python si Heroku
  - [ ] `.env.example` - Mis à jour avec tous les paramètres

- [ ] **Code committé sur git**
  - [ ] Tous les fichiers source ajoutés
  - [ ] Commit message: "Prêt pour déploiement"
  - [ ] Aucune erreur de déploiement (tests en local passent)

- [ ] **Dépendances minimales**
  - [ ] Pas de packages non-utilisés dans `requirements.txt`
  - [ ] Vérifier taille finale
  - [ ] Test installation: `pip install -r requirements.txt` en venv vierge

---

## 🚀 6. Configuration Hébergeur

- [ ] **Variables d'environnement configurées**
  ```
  ADMIN_BOOTSTRAP_EMAIL=admin@domain.com
  ADMIN_BOOTSTRAP_PASSWORD=***
  FLASK_SECRET_KEY=***
  DATABASE_URL=postgresql://...  (copier depuis .env)
  MAIL_ENABLED=1 (si email utilisé)
  MAIL_SMTP_*=... (si email utilisé)
  PORT=5000 (si nécessaire, sinon 8000 ou défaut hébergeur)
  ```
  - [ ] Toutes les variables d'env copiées/configurées
  - [ ] Pas de `.env` nécessaire sur l'hébergeur

- [ ] **BD existante accessibl**
  - [ ] Connection string de l'hébergeur = DATABASE_URL
  - [ ] Tables existent déjà (créées localement)
  - [ ] Pas de risque de recréation accidentelle

- [ ] **Logs/Monitoring configurés**
  - [ ] Logs accessibles sur l'hébergeur
  - [ ] Notifications erreurs: email ou Slack
  - [ ] Monitoring CPU/RAM/BD

---

## ✨ 7. Vérifications finales

- [ ] **DNS/Domaine**
  - [ ] Domaine pointe vers l'hébergeur
  - [ ] DNS propagé (peut prendre 24h)
  - [ ] HTTPS certificat valide

- [ ] **Sites accessibles**
  - [ ] `https://yourdom.com/site/accueil` - Charge
  - [ ] `https://yourdom.com/backoffice/login` - Admin accessible
  - [ ] `/sitemap.xml` - Fichier XML visible
  - [ ] `/robots.txt` - Fichier texte visible

- [ ] **Fonctionnalités testées en production**
  - [ ] Admin login fonctionne
  - [ ] Chat fonctionne (si utilisé)
  - [ ] Formulaire de contact fonctionne
  - [ ] CRUD données fonctionne
  - [ ] Pas d'erreurs 500

---

## 📊 8. Post-Déploiement (24h après)

- [ ] **Monitoring en place**
  - [ ] Logs vérifiés - pas d'erreurs graves
  - [ ] Performance acceptable (< 2s chargement)
  - [ ] BD responsive (pas de timeouts)

- [ ] **SEO checks**
  - [ ] Submit sitemap à Google Search Console
  - [ ] Submit sitemap à Bing Webmaster
  - [ ] Google peut crawler (robots.txt OK)

- [ ] **Backups configurés**
  - [ ] BD backup quotidien
  - [ ] Code sauvegardé sur GitHub
  - [ ] Plan de disaster recovery en place

---

## 🐛 Troubleshooting si erreur

### "Connection refused" ou "Database error"
```bash
1. Vérifier DATABASE_URL sur l'hébergeur
2. Ping l'hôte: ping db.hosting.com
3. Tester local encore: python test_database.py
4. Contacter hébergeur BD
```

### "Module not found" ou "ImportError"
```bash
1. Vérifier: pip install -r requirements.txt
2. Vérifier Python version compatible
3. Vérifier toutes les dépendances installées
```

### "Static files 404" ou CSS/JS manquant
```bash
1. Vérifier dossier static/ existe
2. Sur hébergeur: `python app.py --collect-static` (si Flask)
3. Vérifier `STATIC_FOLDER` dans config
```

### Admin login ne marche pas
```bash
1. Vérifier ADMIN_BOOTSTRAP_EMAIL/PASSWORD dans .env
2. Vérifier première démarrage crée l'user
3. Vérifier user dans BD: SELECT * FROM user;
4. Reset si besoin: Vider table user et redémarrer
```

---

## 🎉 C'est bon!

Si tous les checks sont ✅ c'est prêt à déployer!

```
✅ Application fonctionne localement
✅ BD hébergée connectée et prêt
✅ Sécurité configurée
✅ Hébergeur préparé
✅ Variables d'env à jour
✅ Premier utilisateur admin créé

→ GO LIVE! 🚀
```

---

**Besoin d'aide?**
- Erreur spécifique? Voir section Troubleshooting
- Questions env? Voir `ENV_SETUP.md`
- Questions BD? Voir `HOSTING_SETUP.md` ou `DATABASE_CONFIG.md`

**Mise à jour:** 2026-03-21
