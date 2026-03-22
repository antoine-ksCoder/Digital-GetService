# 🔥 Configuration BD Hébergée - Étape par Étape

Vous avez une base de données hébergée avec just une adresse hôte et pas de tables.
C'est parfait! Voici comment la configurer.

---

## 📋 Étape 1: Récupérer les infos de connexion

Contactez votre hébergeur (support@example.com) et demandez:

```
❓ Quel type de base de données?
✅ PostgreSQL / MySQL / MariaDB

❓ Quelle est l'adresse du serveur?
✅ db.yourhosting.com (ou adresse IP: 192.168.1.1)

❓ Quel port?
✅ Par défaut: 5432 (PostgreSQL) ou 3306 (MySQL)

❓ Quels sont mes identifiants?
✅ Username: (ex: dgs_user ou similar)
✅ Password: ••••••

❓ Quelle base de données dois-je utiliser?
✅ Soit une déjà créée, soit demander d'en créer une
```

**Exemple de réponse:**
```
Type: PostgreSQL
Hôte: db.myhosting.com
Port: 5432
User: dgs_user
Pass: MyPassword123
DB: digital_get_services
```

---

## ⚡ Étape 2: Lancer le script de configuration

Une fois que vous avez les infos, lancer ce script:

```bash
python setup_database.py
```

### Le script demande:
```
Type de BD (postgresql/mysql): postgresql
Adresse hôte (ex: db.example.com): db.myhosting.com
Port (défaut 5432): 5432
Nom d'utilisateur: dgs_user
Mot de passe: MyPassword123
Nom de la base de données: digital_get_services

❓ Créer automatiquement les tables? (oui/non): oui
❓ Sauvegarder DATABASE_URL dans .env? (oui/non): oui
```

### Le script fait automatiquement:
✅ **Construit** la chaîne de connexion (DATABASE_URL)
✅ **Teste** la connexion (vous dit si OK ou erreur)
✅ **Crée** les 12 tables vides
✅ **Sauvegarde** DATABASE_URL dans `.env`

---

## ✅ Étape 3: Vérifier que tout fonctionne

### Test 1: Diagnostic rapide
```bash
python test_database.py
```

Doit afficher:
```
✅ Connexion réussie!
📊 12 tables créées:
  • user
  • conversation
  • message
  ... (et 9 autres)
```

### Test 2: Vérifier le fichier .env
```bash
cat .env
```

Doit contenir:
```env
DATABASE_URL=postgresql://dgs_user:***@db.myhosting.com:5432/digital_get_services
```

(Le mot de passe masqué par *** c'est normal)

### Test 3: Lancer l'app localement
```bash
python app.py
```

Puis aller à: `http://localhost:5000/site/accueil`

Tester:
- Admin login (identifiants du `.env`)
- Naviguer les pages
- Tout fonctionne? ✅

---

## 🚀 Étape 4: Déployer sur l'hébergeur

### Configuration sur l'hébergeur (dépend du service)

#### Heroku
```bash
heroku config:set DATABASE_URL="postgresql://dgs_user:MyPassword123@db.myhosting.com:5432/digital_get_services"
```

#### Autre hébergeur (cpanel, etc.)
1. Aller dans l'admin panel
2. Trouver "Environment variables" ou "Config"
3. Ajouter:
   ```
   KEY: DATABASE_URL
   VALUE: postgresql://dgs_user:MyPassword123@db.myhosting.com:5432/digital_get_services
   ```
4. Sauvegarder

### Redémarrer l'app
- L'hébergeur détecte la nouvelle variable
- L'app redémarre automatiquement
- Les tables existent déjà (créées localement)
- L'app fonctionne directement! 🎉

---

## 🎯 Résumé rapide (5 minutes)

```bash
# 1. Lancer le setup (vous guide)
python setup_database.py

# 2. Répondre aux questions (30 sec)
# 3. Vérifier
python test_database.py

# 4. Tester localement
python app.py

# 5. Sur l'hébergeur
# Ajouter DATABASE_URL en variable d'env
# Redémarrer

# 6. Accéder à votre site
# https://yourdom.com/site/accueil ✅
```

---

## ⚠️ Erreurs courantes

### "Connection refused"
```
❌ Erreur: Connection refused

Causes:
1. Bad host: db.myhosting.com - Vérifier l'adresse exacte
2. Bad port: 5432 - Vérifier le port
3. DB offline: Vérifier avec l'hébergeur
4. Firewall: L'hébergeur peut bloquer les connexions distantes

Actions:
✅ Double-check l'adresse hôte exacte
✅ Tester avec l'outil MySQL/pgAdmin du hébergeur
✅ Contacter support@hosting.com
```

### "Authentication failed"
```
❌ Erreur: FATAL: password authentication failed

Causes:
1. Bad username: dgs_user - Vérifier l'exactitude (case-sensitive)
2. Bad password: MyPassword123 - Caractères spéciaux?
3. User doesn't exist: Créer l'utilisateur

Actions:
✅ Vérifier caractère par caractère
✅ Si @ ou ! ou & dans le password, peut-être besoin de l'encoder
✅ Créer nouvel utilisateur via hébergeur si nécessaire
```

### "Database doesn't exist"
```
❌ Erreur: FATAL: database "digital_get_services" does not exist

Causes:
1. Mauvais nom de BD
2. BD pas créée

Actions:
✅ Vérifier le nom exactement
✅ Créer la BD via hébergeur panel ou:
   PostgreSQL: CREATE DATABASE digital_get_services;
   MySQL: CREATE DATABASE digital_get_services;
```

### "No tables found"
```
⚠️  Le script dit "0 tables trouvées"

C'est normal! La BD est vide. Le script va les créer.
Continuer et répondre "oui" quand il demande de créer les tables.
```

---

## 💡 Tips & Tricks

### Si vous devez réinstaller les tables
```bash
python -c "from app import create_app, db; app = create_app(); db.create_all(); print('✅ OK')"
```

### Si vous devez vider complètement la BD
```bash
python -c "from app import create_app, db; app = create_app(); db.drop_all(); db.create_all(); print('✅ Reset OK')"
```

### Exporter/Importer les données
```bash
# PostgreSQL export
pg_dump "postgresql://user:pass@host/db" > backup.sql

# PostgreSQL import
psql "postgresql://user:pass@host/db" < backup.sql

# MySQL export
mysqldump -u user -p host db > backup.sql

# MySQL import
mysql -u user -p host db < backup.sql
```

---

## 📞 Support

Si ça marche pas:

1. **Tester la connexion d'abord**
   ```bash
   python setup_database.py
   # Tester juste la connexion, pas créer les tables
   ```

2. **Vérifier chaque paramètre**
   - Host: Peut être un nom ou une IP?
   - Port: Usuellement 5432 ou 3306
   - User: Créé par l'hébergeur?
   - Password: Exactement comme reçu?
   - DB: Existe-t-elle?

3. **Contacter votre hébergeur**
   - Voici l'erreur exacte: [copier-coller]
   - Je dois me connecter to: postgresql://user:pass@host:5432/db
   - Pouvez-vous vérifier?

---

## ✨ Une fois fonctionnellement

**Branchez les données!**

```python
# Ajouter des utilisateurs
from app import create_app, db
from models import User

app = create_app()
with app.app_context():
    user = User(
        email="contact@mycompany.com",
        full_name="Mon Entreprise",
        password_hash="...",
        role="admin"
    )
    db.session.add(user)
    db.session.commit()
```

Voir `ORM_EXAMPLES.md` pour plus d'exemples!

---

**Besoin d'aide?** Lancer: `python setup_database.py` 🚀

**Mise à jour:** 2026-03-21
