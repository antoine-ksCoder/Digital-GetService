# 🚀 Configuration BD Distante - Guide rapide

Votre base de données est sur un serveur d'hébergement. Je vais vous montrer comment la configurer.

## 📋 Informations dont vous avez besoin

Contactez votre hébergeur pour obtenir:

```
Type de BD:           PostgreSQL / MySQL / MariaDB
Adresse hôte:         db.example.com  (ou une adresse IP)
Port:                 5432 (PostgreSQL) ou 3306 (MySQL)
Nom d'utilisateur:    dgs_user
Mot de passe:         votre_mot_de_passe
Nom de la BD:         digital_get_services (vide pour l'instant)
```

---

## ⚡ Méthode 1: Script automatique (RECOMMANDÉ)

### Étape 1: Lancer le script
```bash
python setup_database.py
```

### Étape 2: Répondre aux questions
```
Type de BD (postgresql/mysql): postgresql
Adresse hôte (ex: db.example.com): db.myhosting.com
Port (défaut 5432): 5432
Nom d'utilisateur: dgs_user
Mot de passe: ••••••••
Nom de la base de données: digital_get_services

❓ Créer automatiquement les tables? (oui/non): oui
❓ Sauvegarder DATABASE_URL dans .env? (oui/non): oui
```

### Étape 3: Fini!
Le script:
- ✅ Construit la chaîne de connexion `DATABASE_URL`
- ✅ Teste la connexion
- ✅ **Crée automatiquement toutes les tables**
- ✅ Sauvegarde dans `.env`

---

## 🔧 Méthode 2: Configuration manuelle

### Étape 1: Construire DATABASE_URL

#### PostgreSQL
```env
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

**Exemple:**
```env
DATABASE_URL=postgresql://dgs_user:mypassword123@db.myhosting.com:5432/digital_get_services
```

#### MySQL / MariaDB
```env
DATABASE_URL=mysql+pymysql://username:password@host:3306/database_name
```

**Exemple:**
```env
DATABASE_URL=mysql+pymysql://dgs_user:mypassword123@db.myhosting.com:3306/digital_get_services
```

### Étape 2: Ajouter à `.env`

Ouvrir `.env` à la racine du projet et remplacer:
```env
DATABASE_URL=postgresql://dgs_user:mypassword@db.myhosting.com:5432/digital_get_services
```

### Étape 3: Créer les tables

Lancer ce script Python:
```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tables créées!")
```

Ou dans le terminal:
```bash
python -c "from app import create_app, db; app = create_app(); db.create_all(); print('✅ Tables créées!')"
```

---

## ✅ Vérifier la configuration

### Tester la connexion
```bash
python test_database.py
```

Devrait afficher:
```
✅ Connexion réussie!
🗄️  Dialecte détecté: postgresql
📊 Tables détectées:
  ✓ user (10 colonnes)
  ✓ conversation (5 colonnes)
  ✓ message (5 colonnes)
  ... (et 9 autres tables)
```

### Vérifier le fichier .env
```bash
cat .env | grep DATABASE_URL
```

Devrait afficher:
```
DATABASE_URL=postgresql://dgs_user:***@db.myhosting.com:5432/digital_get_services
```

---

## 🛡️ Sécurité

### ❌ IMPORTANT: Ne pas exposer le mot de passe!

**Mauvais:**
```python
DATABASE_URL = "postgresql://user:password@host/db"  # Visible sur GitHub!
```

**Bon:**
```env
# Fichier .env (protégé par .gitignore)
DATABASE_URL=postgresql://user:password@host/db
```

### En production
```bash
# Hébergeur directement (ne pas mettre en code)
export DATABASE_URL="postgresql://user:password@host/db"
```

---

## 🗂️ Tables créées automatiquement (12 au total)

| Table | Description | Lignes initiales |
|-------|-------------|------------------|
| `user` | Utilisateurs | 0 (admin créé au démarrage) |
| `conversation` | Chats | 0 |
| `message` | Messages | 0 |
| `services_catalog` | Services | 0 |
| `service_people` | Experts/Team | 0 |
| `realisation_realisation` | Projets | 0 |
| `domaine_accueil` | Domaines d'activité | 0 |
| `equipe_propos` | Équipe page À propos | 0 |
| `membre_notreequipe` | Équipe page Équipe | 0 |
| `services_service` | Services (legacy) | 0 |
| `services_footer` | Services en footer | 0 |
| `contact_footer` | Contact en footer | 0 |

**Toutes créées automatiquement, rien à faire manuellement!**

---

## 🚀 Déployer après configuration

### 1. Tester localement d'abord
```bash
python app.py
# Aller à http://localhost:5000/site/accueil
# Tester le admin login
```

### 2. Configurer sur l'hébergeur
Ajouter la variable d'environnement:
```bash
DATABASE_URL=postgresql://...
```

### 3. Redémarrer l'app
Les tables existent déjà, l'app démarre directement!

---

## 🐛 Troubleshooting

### "Connection refused"
- ✅ Vérifier l'adresse hôte
- ✅ Vérifier le port (5432 PostgreSQL, 3306 MySQL)
- ✅ Vérifier que la BD est accessible depuis Internet
- ✅ Vérifier les firewall/règles de sécurité de l'hébergeur

### "Authentication failed"
- ✅ Vérifier le username
- ✅ Vérifier le password (caractères spéciaux!)
- ✅ Vérifier les permissions utilisateur

### "Database doesn't exist"
- ✅ Créer la base de données sur l'hébergeur
- ✅ Vérifier le nom dans DATABASE_URL

### "Syntax error in SQL"
- ✅ Vérifier que c'est PostgreSQL ou MySQL (pas SQLite)
- ✅ Vérifier la URL format

### "Too many connections"
- ✅ Configurer le pool de connexions dans `app.py`
- ✅ Redémarrer l'app

---

## 📞 Obtenir les infos de votre hébergeur

### Questions à poser à votre hébergeur

```
1. Type de base de données?
   Réponse: PostgreSQL / MySQL / MariaDB

2. Adresse du serveur BD?
   Réponse: db.hosting123.com

3. Port d'accès?
   Réponse: 5432 ou 3306

4. Identifiant d'accès?
   Réponse: digital_user

5. Mot de passe?
   Réponse: ••••••

6. Quelle base de données utiliser?
   Réponse: J'utiliserai: digital_get_services

7. Puis-je créer des tables dans cette BD?
   Réponse: Oui (si limité, contactez support)
```

---

## ⚡ Résumé quick-start

```bash
# 1. Lancer le setup
python setup_database.py

# 2. Répondre aux questions (2 minutes)
# 3. Vérifier
python test_database.py

# 4. Lancer l'app
python app.py

# 5. Déployer
# Ajouter DATABASE_URL à l'hébergeur
# Redémarrer l'app
```

---

## 📚 Ressources

- `DATABASE_CONFIG.md` - Guide détaillé toutes les BDs
- `ORM_EXAMPLES.md` - Utiliser les données avec l'ORM
- `test_database.py` - Script diagnostic
- `setup_database.py` - **Script setup (utiliser celui-ci!)**

---

**Besoin d'aide?**
1. Lancer: `python setup_database.py`
2. Suivre les instructions
3. C'est automatique! 🎉

**Mise à jour:** 2026-03-21
