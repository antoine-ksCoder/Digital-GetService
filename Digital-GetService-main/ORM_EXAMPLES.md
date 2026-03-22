# 🎯 Exemples ORM SQLAlchemy

Voici comment utiliser SQLAlchemy dans votre application.

## Importer les modèles

```python
from models import User, Conversation, Message, ServicesCatalog, Realisation
from app import db
```

---

## 1️⃣ CRÉER (CREATE)

### Créer un utilisateur

```python
from models import User
from werkzeug.security import generate_password_hash

user = User(
    full_name="John Doe",
    email="john@example.com",
    password_hash=generate_password_hash("secure_password"),
    role="client",
    is_active=1,
    person_type="entrepreneur",
    preferred_lang="fr",
    created_at="2026-03-21T10:30:00"
)

db.session.add(user)
db.session.commit()
print(f"✅ Utilisateur créé avec ID: {user.id}")
```

### Créer un message de contact

```python
from models import Conversation, Message
from datetime import datetime, timezone

# Créer une conversation
conv = Conversation(
    user_one_id=1,
    user_two_id=2,
    created_at=datetime.now(timezone.utc).isoformat()
)
db.session.add(conv)
db.session.flush()  # Récupérer l'ID sans committer

# Créer un message
msg = Message(
    conversation_id=conv.id,
    sender_id=1,
    body="Bonjour, j'aurais besoin d'aide.",
    created_at=datetime.now(timezone.utc).isoformat()
)

db.session.add(msg)
db.session.commit()
print(f"✅ Message créé: {msg.id}")
```

### Créer plusieurs enregistrements

```python
users = [
    User(email="user1@example.com", full_name="User 1", role="client"),
    User(email="user2@example.com", full_name="User 2", role="client"),
    User(email="user3@example.com", full_name="User 3", role="agent"),
]

db.session.add_all(users)
db.session.commit()
print(f"✅ {len(users)} utilisateurs créés")
```

---

## 2️⃣ LIRE (READ / SELECT)

### Récupérer tous les enregistrements

```python
# Toutes les utilisateurs
all_users = User.query.all()
print(f"Total: {len(all_users)}")

for user in all_users:
    print(f"- {user.email}: {user.full_name} ({user.role})")
```

### Récupérer un enregistrement par ID

```python
user = User.query.get(1)
if user:
    print(f"Utilisateur trouvé: {user.email}")
else:
    print("Utilisateur non trouvé")
```

### Rechercher avec des critères (WHERE)

```python
# Trouver un utilisateur par email
user = User.query.filter_by(email="john@example.com").first()

# Trouver tous les admins
admins = User.query.filter_by(role="admin").all()

# Trouver tous les actifs
active_users = User.query.filter_by(is_active=1).all()
```

### Requêtes plus complexes (WHERE avancé)

```python
from sqlalchemy import or_, and_

# Trouver utilisateurs actifs ET (admin OU agent)
users = User.query.filter(
    and_(
        User.is_active == 1,
        or_(User.role == "admin", User.role == "agent")
    )
).all()

# Comparaisons
users = User.query.filter(User.id > 10).all()  # id > 10
users = User.query.filter(User.email.like("%@gmail.com")).all()  # emails Gmail
```

### Compter les enregistrements

```python
total_users = User.query.count()
admin_count = User.query.filter_by(role="admin").count()
print(f"Total: {total_users}, Admins: {admin_count}")
```

### Paginer les résultats

```python
page = 1
per_page = 10

users = User.query.paginate(page=page, per_page=per_page)
print(f"Page {users.page}")
print(f"Total pages: {users.pages}")
print(f"Total items: {users.total}")

for user in users.items:
    print(f"- {user.email}")
```

### Trier les résultats

```python
# Trier par email (A → Z)
users = User.query.order_by(User.email).all()

# Trier par id décroissant (plus récent d'abord)
users = User.query.order_by(User.id.desc()).all()

# Trier par plusieurs colonnes
users = User.query.order_by(User.role, User.email.desc()).all()
```

---

## 3️⃣ METTRE À JOUR (UPDATE)

### Modifier un enregistrement

```python
user = User.query.get(1)
if user:
    user.full_name = "Nouveau Nom"
    user.preferred_lang = "en"
    db.session.commit()
    print("✅ Utilisateur mis à jour")
```

### Modifier plusieurs enregistrements

```python
# Désactiver tous les utilisateurs d'un certain rôle
User.query.filter_by(role="guest").update({"is_active": 0})
db.session.commit()
print("✅ Utilisateurs désactivés")
```

### Incrémenter une valeur

```python
from sqlalchemy import func

user = User.query.get(1)
# Si vous aviez une colonne numérique:
# user.login_count = user.login_count + 1
db.session.commit()
```

---

## 4️⃣ SUPPRIMER (DELETE)

### Supprimer un enregistrement

```python
user = User.query.get(1)
if user:
    db.session.delete(user)
    db.session.commit()
    print("✅ Utilisateur supprimé")
```

### Supprimer plusieurs enregistrements

```python
# Supprimer tous les utilisateurs inactifs
User.query.filter_by(is_active=0).delete()
db.session.commit()
print("✅ Utilisateurs inactifs supprimés")
```

### Supprimer tout (attention!)

```python
# ⚠️ ATTENTION: Cela supprime TOUS les utilisateurs!
# Utilisé uniquement pour les tests
User.query.delete()
db.session.commit()
```

---

## 🔗 Relations entre tables

### Récupérer les messages d'une conversation

```python
conv = Conversation.query.get(1)
messages = conv.messages  # Relation directe
for msg in messages:
    print(f"{msg.sender.email}: {msg.body}")
```

### Récupérer les conversations d'un utilisateur

```python
user = User.query.get(1)
conversations = Conversation.query.filter(
    or_(Conversation.user_one_id == user.id, Conversation.user_two_id == user.id)
).all()

for conv in conversations:
    other_user = conv.user_two if conv.user_one_id == user.id else conv.user_one
    print(f"Conversation avec: {other_user.email}")
    print(f"Messages: {len(conv.messages)}")
```

---

## 🎯 Requêtes avancées

### GROUP BY (Regrouper)

```python
from sqlalchemy import func

# Compter les utilisateurs par rôle
result = db.session.query(
    User.role,
    func.count(User.id).label("count")
).group_by(User.role).all()

for role, count in result:
    print(f"{role}: {count}")
```

### JOIN (Joindre des tables)

```python
# Utilisateurs ET leurs conversations
result = db.session.query(User, Conversation).join(
    Conversation,
    (Conversation.user_one_id == User.id) | (Conversation.user_two_id == User.id)
).all()
```

### AGGREGATE (Fonctions d'agrégation)

```python
from sqlalchemy import func

# Nombre total de messages
total = Message.query.count()

# Premiers et derniers messages
first = Message.query.order_by(Message.id.asc()).first()
last = Message.query.order_by(Message.id.desc()).first()

# Conversations par utilisateur
stats = db.session.query(
    User.email,
    func.count(Conversation.id).label("conv_count")
).outerjoin(Conversation).group_by(User.id).all()
```

---

## 🚨 Gestion des erreurs

### Try/Catch

```python
try:
    user = User(email="duplicate@example.com", full_name="Test")
    db.session.add(user)
    db.session.commit()
except Exception as e:
    db.session.rollback()  # Annuler les changements
    print(f"❌ Erreur: {e}")
```

### Rollback (Annuler)

```python
try:
    user.email = "invalid"
    db.session.commit()
except:
    print("Erreur! Résumé...")
    db.session.rollback()
    # Tous les changements depuis le dernier commit sont annulés
```

---

## 💡 Bonnes pratiques

### 1. Utiliser des contextes d'application

```python
from app import create_app, db

app = create_app()
with app.app_context():
    users = User.query.all()  # Fonctionne!
```

### 2. Lazy loading vs Eager loading

```python
# Lazy load (lent si beaucoup de requêtes)
user = User.query.get(1)
messages = user.messages  # Nouvelle requête SQL!

# Eager load (plus rapide)
from sqlalchemy.orm import joinedload
user = User.query.options(joinedload(User.messages)).get(1)
messages = user.messages  # Pas de nouvelle requête
```

### 3. Limiter les résultats

```python
# Récupérer seulement 10 enregistrements (plus rapide)
users = User.query.limit(10).all()

# Sauter les 50 premiers
users = User.query.offset(50).limit(10).all()
```

### 4. Récupérer seulement certaines colonnes

```python
# Plus rapide si vous n'avez besoin que de l'email
emails = db.session.query(User.email).all()

# Meilleur pour les rapports
result = db.session.query(User.email, User.role).all()
for email, role in result:
    print(f"{email}: {role}")
```

### 5. Transactions

```python
try:
    # Plusieurs opérations
    db.session.add(user1)
    db.session.add(user2)
    db.session.delete(user3)

    db.session.commit()  # Tout ou rien!
except:
    db.session.rollback()
```

---

## 🔍 Débogage

### Voir les requêtes SQL

```python
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Maintenant chaque requête SQL est affichée
user = User.query.get(1)
```

### Echo SQL dans Flask

```python
# Dans app.py
app.config["SQLALCHEMY_ECHO"] = True  # Affiche toutes les requêtes

# Puis redémarrer l'app
```

### Compter les requêtes

```python
from flask import get_flashed_messages
from sqlalchemy.engine import Engine

@app.before_request
def before_request():
    g.query_count_start = len(db.session.connection().info.get('executed_queries', []))

@app.after_request
def after_request(response):
    queries = len(db.session.connection().info.get('executed_queries', []))
    print(f"Requêtes: {queries}")
    return response
```

---

## 📚 Ressources

- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/en/20/orm/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/
- **Tutorial officiel**: https://docs.sqlalchemy.org/en/20/tutorial/

---

**Mise à jour:** 2026-03-21
