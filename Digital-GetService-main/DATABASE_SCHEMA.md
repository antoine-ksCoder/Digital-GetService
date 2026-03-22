# 📊 Schéma Base de Données - Digital Get Services

Structure des tables créées automatiquement par SQLAlchemy.

## 👤 Table: `user`

Stocke les utilisateurs (clients, admins, agents)

```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- admin, agent, client
    is_active INTEGER,
    person_type VARCHAR(50),
    preferred_lang VARCHAR(10),
    created_at VARCHAR(255),
    updated_at VARCHAR(255)
);
```

**Exemples:**
```python
User.query.filter_by(role="admin").all()
User.query.filter_by(email="client@example.com").first()
```

---

## 💬 Table: `conversation`

Conversations de chat entre utilisateurs

```sql
CREATE TABLE conversation (
    id INTEGER PRIMARY KEY,
    user_one_id INTEGER FOREIGN KEY,
    user_two_id INTEGER FOREIGN KEY,
    created_at VARCHAR(255),
    updated_at VARCHAR(255)
);
```

**Exemples:**
```python
Conversation.query.filter_by(user_one_id=1).all()
Conversation.query.filter(
    or_(Conversation.user_one_id == 1, Conversation.user_two_id == 1)
).all()
```

---

## 📝 Table: `message`

Messages individuels

```sql
CREATE TABLE message (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER FOREIGN KEY,
    sender_id INTEGER FOREIGN KEY,
    body TEXT,
    created_at VARCHAR(255),
    updated_at VARCHAR(255)
);
```

**Exemples:**
```python
conv = Conversation.query.get(1)
conv.messages  # Tous les messages de la conversation
Message.query.filter_by(sender_id=1).all()  # Tous mes messages envoyés
```

---

## 🌐 Table: `domaine_accueil`

Domaines d'activité affichés sur l'accueil

```sql
CREATE TABLE domaine_accueil (
    id INTEGER PRIMARY KEY,
    nom VARCHAR(255),
    description TEXT,
    icon VARCHAR(255),
    is_suspended INTEGER
);
```

**Utilisation:** Affichage accueil `/site/accueil`

---

## 🎯 Table: `equipe_propos`

Équipe affichée sur la page "À propos"

```sql
CREATE TABLE equipe_propos (
    id INTEGER PRIMARY KEY,
    nom VARCHAR(255),
    description TEXT,
    icon VARCHAR(255),
    is_suspended INTEGER
);
```

**Utilisation:** Page `/site/propos`

---

## 💼 Table: `services_catalog`

Catalogue centralisé des services

```sql
CREATE TABLE services_catalog (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    status VARCHAR(50),  -- active, inactive
    created_at VARCHAR(255)
);
```

**Utilisé par:** Les services, les personnes, les réalisations

---

## 👨‍💼 Table: `service_people`

Personnes/experts associés aux services

```sql
CREATE TABLE service_people (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    specialty VARCHAR(255),
    photo_path TEXT,
    is_active INTEGER
);
```

**Affichage:** Page `/site/notreEquipe`

---

## 🏆 Table: `realisation_realisation`

Projets/réalisations

```sql
CREATE TABLE realisation_realisation (
    id INTEGER PRIMARY KEY,
    titre VARCHAR(255),
    description TEXT,
    client VARCHAR(255),
    technologies VARCHAR(255),
    date_completion DATE,
    lien_site VARCHAR(255),
    image_path VARCHAR(255),
    categorie VARCHAR(255),
    is_suspended INTEGER
);
```

**Affichage:** Page `/site/realisation`

---

## 📋 Table: `services_service`

Services hérités (ancien système)

```sql
CREATE TABLE services_service (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    is_suspended INTEGER
);
```

**Utilisé par:** Migration/compatibilité avec ancien système

---

## 🔗 Tables de relation (Many-to-Many)

### `service_people_services_catalog`

Relie les personnes aux services

```sql
CREATE TABLE service_people_services_catalog (
    service_people_id INTEGER FOREIGN KEY,
    services_catalog_id INTEGER FOREIGN KEY
);
```

**Requête:**
```python
person = ServicePeople.query.get(1)
person.services  # Tous les services de cette personne
```

---

## 🗄️ Footer & Contact (Content Management)

### `services_footer`
Services affichés en footer

### `contact_footer`
Information de contact en footer

### `reseau_footer`
Réseaux sociaux en footer

### `header`
Configuration du header

---

## 📈 Statistiques

### Requête: Compter les tables

```python
inspector = db.inspect(db.engine)
tables = inspector.get_table_names()
print(f"Total tables: {len(tables)}")
# Sortie: Total tables: 12
```

### Requête: Voir l'espace utilisé

**PostgreSQL:**
```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**MySQL:**
```sql
SELECT
    TABLE_NAME,
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'Size (MB)'
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'digital_get_services'
ORDER BY DATA_LENGTH + INDEX_LENGTH DESC;
```

---

## 🔐 Sécurité des données

### Bonnes pratiques implémentées:

1. **Mots de passe hachés**
   ✅ Utilise `werkzeug.security.generate_password_hash()`
   ❌ Les mots de passe ne sont JAMAIS stockés en clair

2. **SQL Injection prévenue**
   ✅ Utilise les paramètres liés (`:param`)
   ❌ Pas de concaténation de chaînes SQL

3. **CSRF protection**
   ✅ Tokens CSRF sur tous les formulaires
   ✅ Validation côté serveur

4. **Intégrité référentielle**
   ✅ Foreign keys sur les relations
   ✅ Cascade delete configurée

---

## 💁 Common Queries

### Créer les tables

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()  # Crée toutes les tables
    print("✅ Tables créées")
```

### Vider une table

```python
with app.app_context():
    Message.query.delete()  # ⚠️ Attention!
    db.session.commit()
```

### Exporter les données

```python
import json

users = User.query.all()
data = [{"email": u.email, "role": u.role} for u in users]
with open("users.json", "w") as f:
    json.dump(data, f)
```

### Importer les données

```python
import json

with open("users.json", "r") as f:
    data = json.load(f)
    for user_data in data:
        user = User(**user_data)
        db.session.add(user)
    db.session.commit()
    print(f"✅ {len(data)} utilisateurs importés")
```

---

## 🧪 Tests avec les templates

### Vérifier les données en template Jinja

```html
<!-- Template -->
<h1>Total utilisateurs: {{ users|length }}</h1>
<ul>
{% for user in users %}
    <li>{{ user.email }} - {{ user.role }}</li>
{% endfor %}
</ul>

<!-- Depuis Python -->
return render_template("index.html", users=User.query.all())
```

---

## 📚 Logs SQL

### Voir les requêtes générées

```python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Puis exécutez des requêtes
users = User.query.all()
# Affiche: SELECT user.id, user.email, ... FROM user
```

---

**Mise à jour:** 2026-03-21
**Compatibilité:** SQLite, PostgreSQL, MySQL
