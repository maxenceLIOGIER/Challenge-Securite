# Challenge-Securite

## Description de l'application
[ à faire]


### Prérequis

Avant de commencer, assurez-vous que vous avez installé les outils suivants :
- [Docker](https://www.docker.com/products/docker-desktop) (avec Docker Compose)
- [Git](https://git-scm.com/)
- [Python 3.x](https://www.python.org/downloads/)


## Étapes d'installation

### 1. Clonez le dépôt

Commencez par cloner ce dépôt Git sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/votre-repository.git
cd votre-repository
```

### 2. Convertir le fichier parquet en csv
Si vous avez un fichier Parquet contenant des données (`log_export.parquet`), vous devrez le convertir en CSV afin de l'utiliser pour initialiser votre base de données PostgreSQL ou pour d'autres analyses. Le script de conversion est déjà créé.

#### Assurez vous d'avoir installé pandas et os
Vous pouvez l'installer via la commande suivante :
```bash
pip install pandas os
```

#### Exécutez le script `convert_parquet_to_csv.py` :
```bash
python convert_parquet_to_csv.py
```
Ce script effectue les étapes suivantes :
- Charge le fichier Parquet (`logs_processed.parquet`).
- Convertit les colonnes nécessaires (notamment les colonnes de ports) pour qu'elles soient compatibles avec la base de données PostgreSQL.
- Sauvegarde le fichier converti sous le nom `logs_processed.csv` dans le répertoire `donnees_finales/`.
- Supprime le fichier parquet


### 3. Construire et démarrer les conteneurs Docker
Dans le répertoire du projet, exécutez la commande suivante pour construire les images Docker et démarrer les conteneurs en arrière-plan :

```bash
docker-compose up --build -d
```
Cette commande va :
- Construire les images Docker spécifiées dans le fichier `docker-compose.yml`.
- Démarrer les conteneurs pour PostgreSQL et l'application Streamlit.

### 4. Vérification du démarrage des conteneurs
Pour vérifier que tout fonctionne correctement, vous pouvez exécuter la commande suivante pour afficher l'état des conteneurs :

```bash
docker-compose ps
```
Assurez-vous que tous les conteneurs sont en cours d'exécution. En particulier, le conteneur PostgreSQL (nommé `DBPostgres`) et le conteneur Streamlit (nommé `client`) doivent être en état "Up".

### 5. Accéder à l'application Streamlit
Une fois les conteneurs démarrés, vous pouvez accéder à votre application Streamlit via votre navigateur à l'adresse suivante :
http://localhost:8502