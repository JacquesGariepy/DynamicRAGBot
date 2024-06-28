# RAG Bot Manager

## Description

RAG Bot Manager est une application d'entreprise complète conçue pour la gestion de bots d'exploration et d'un système de Retrieval-Augmented Generation (RAG). Cette plateforme offre une solution robuste pour créer, gérer et surveiller des bots autonomes qui collectent des informations à partir de diverses sources, tout en fournissant une interface conviviale pour interagir avec un système RAG avancé.

## Fonctionnalités principales

- Création et gestion de bots d'exploration dynamiques
- Interface utilisateur intuitive pour le contrôle des bots
- Système RAG intégré pour la génération de réponses contextuelles
- Tableau de bord pour la surveillance des performances des bots
- Gestion des utilisateurs et des droits d'accès
- API RESTful pour l'intégration avec d'autres systèmes

## Architecture du projet

```
rag-bot-manager/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── bot.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── bot.py
│   │   │   ├── rag.py
│   │   │   └── admin.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── bot_service.py
│   │   │   └── rag_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_bot_service.py
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js
│   │   │   └── PrivateRoute.js
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── BotManagement.js
│   │   │   ├── RAGInterface.js
│   │   │   ├── Settings.js
│   │   │   └── Login.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── botService.js
│   │   │   └── ragService.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── README.md
│   └── .env.example
│
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
│
├── README.md
└── CONTRIBUTING.md
```

## Technologies utilisées

- **Backend** :
  - Flask : Framework web Python
  - SQLAlchemy : ORM pour la gestion de la base de données
  - Flask-JWT-Extended : Gestion de l'authentification
  - Qdrant : Base de données vectorielle
  - Sentence-Transformers : Pour l'encodage des documents
  - OpenAI GPT : Pour la génération de réponses dans le système RAG

- **Frontend** :
  - React : Bibliothèque JavaScript pour la construction de l'interface utilisateur
  - Axios : Client HTTP pour les requêtes API
  - React Router : Pour la navigation dans l'application

- **Base de données** :
  - PostgreSQL : Base de données relationnelle

- **Conteneurisation et orchestration** :
  - Docker : Pour la conteneurisation de l'application
  - Docker Compose : Pour l'orchestration des services

## Prérequis

- Docker et Docker Compose
- Node.js (v14+) et npm pour le développement frontend
- Python 3.8+ pour le développement backend
- Compte OpenAI avec clé API valide

## Installation et configuration

1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-organisation/rag-bot-manager.git
   cd rag-bot-manager
   ```

2. Configuration du backend :
   ```
   cd backend
   cp .env.example .env
   # Modifiez le fichier .env avec vos propres valeurs
   pip install -r requirements.txt
   ```

3. Configuration du frontend :
   ```
   cd ../frontend
   cp .env.example .env
   # Modifiez le fichier .env si nécessaire
   npm install
   ```

4. Lancement de l'application avec Docker :
   ```
   cd ../docker
   docker-compose up -d
   ```

5. Accédez à l'application :
   Ouvrez votre navigateur et allez à `http://localhost:80`

## Développement

Pour lancer l'application en mode développement :

1. Backend :
   ```
   cd backend
   flask run
   ```

2. Frontend :
   ```
   cd frontend
   npm start
   ```

## Tests

Pour exécuter les tests du backend :
```
cd backend
python -m unittest discover tests
```

## Déploiement

Pour déployer l'application en production :

1. Configurez les variables d'environnement pour la production dans les fichiers `.env`.
2. Construisez et déployez les conteneurs Docker :
   ```
   cd docker
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Contribution

Les contributions sont les bienvenues ! Veuillez consulter le fichier [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives de contribution.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur le dépôt GitHub du projet.

## Auteurs

- [Votre nom] - Développeur principal

## Remerciements

- OpenAI pour leur API GPT
- L'équipe Qdrant pour leur excellente base de données vectorielle
- Tous les contributeurs open source des bibliothèques utilisées dans ce projet
