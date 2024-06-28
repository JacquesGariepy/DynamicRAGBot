
# RAG Bot Manager

## Description

RAG Bot Manager est une application business complète pour la gestion de bots d'exploration et d'un système de Retrieval-Augmented Generation (RAG). Cette plateforme permet de créer, gérer et surveiller des bots autonomes qui collectent des informations à partir de diverses sources, tout en offrant une interface conviviale pour interagir avec un système RAG avancé.

## Concept

Le système combine plusieurs technologies clés :

1. **Bots d'exploration dynamiques** : Des agents autonomes capables de scraper le web, explorer des dépôts Git, des systèmes de fichiers locaux et d'autres sources de données.
2. **Système RAG (Retrieval-Augmented Generation)** : Un mécanisme intelligent qui utilise les informations collectées pour générer des réponses précises et contextuelles aux questions des utilisateurs.
3. **Interface de gestion centralisée** : Une application web qui permet aux utilisateurs de créer, configurer, surveiller et contrôler les bots, ainsi que d'interagir avec le système RAG.
4. **Stockage vectoriel** : Utilisation de Qdrant pour un stockage et une recherche efficaces des données vectorisées.
5. **Sécurité et gestion des utilisateurs** : Système d'authentification robuste et gestion des droits d'accès.

## Arborescence du projet

```plaintext
rag-bot-manager/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── bot.py
│   │   │   ├── user.py
│   │   │   └── task.py
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
│   │   │   ├── ragService.js
│   │   │   └── settingsService.js
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
└── README.md
```

## Installation et configuration

### Prérequis

- Docker et Docker Compose
- Node.js (v14+) et npm pour le développement frontend
- Python 3.8+ pour le développement backend
- Compte OpenAI avec clé API valide

### Étapes d'installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/votre-organisation/rag-bot-manager.git
    cd rag-bot-manager
    ```

2. Configuration du backend :
    ```bash
    cd backend
    cp .env.example .env
    pip install -r requirements.txt
    ```

3. Configuration du frontend :
    ```bash
    cd ../frontend
    cp .env.example .env
    npm install
    ```

4. Lancement de l'application avec Docker :
    ```bash
    cd ../docker
    docker-compose up -d
    ```

5. Accédez à l'application :
    Ouvrez votre navigateur et allez à `http://localhost:80`.

### Outils et technologies utilisés

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

## Développement

Pour lancer l'application en mode développement :

1. Backend :
    ```bash
    cd backend
    flask run
    ```

2. Frontend :
    ```bash
    cd frontend
    npm start
    ```

## Tests

Pour exécuter les tests du backend :
```bash
cd backend
python -m unittest discover tests
```

## Déploiement

Pour déployer l'application en production :

1. Configurez les variables d'environnement pour la production dans les fichiers `.env`.
2. Construisez et déployez les conteneurs Docker :
    ```bash
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
