# Challenge-Securite

## Description de l'application

Cette application permet d'analyser des logs issus d'une simulation d'attaques. Vous retrouverez plusieurs pages vous permettant d'analyser les données sous différents angles et à différents niveaux de granularité. Cette application se veut interactive et permet à n'importe quel utilisateur de naviguer lui même et de faire ses propres analyses. 

L'application est organisée comme suit : 

* Une page **Acceuil**
    * Cette page détaille les fonctionnalités de l'application ainsi que ces objectifs.

* Une page **Exploration des trafics** 
    * Cette page vous permet de naviguer dans les différents trafics réseau. 

* Une page **Statistiques Descriptives**
    * Ici, vous pourrez retouver des tableaux de bords vous permettant des comprendre en profondeur les logs. Vous pourrez investiguer les différents régles, actions, protocole, IPs, sous différents angles grâce notamment à des filtres.

* Une page **Machine Learning**
    * Sur cette page, deux modèles de Machine Learning sont entrainés pour vous offrir plusieurs scénarios d'analyses. 
        1. Isolation Forest : 
        Permet de détecter les anomalies dans l'ensemble des logs. 

        2. DBSCAN : 
        Permet de détecter les différents comportements dans les logs réseaux 

        3. Analyse croisés des résultats : 
        Vous pourrez croiser vos résultats de ces 2 modèles pour apporfondir vos analyses. 

Bonne naviguation !!!

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
Si vous avez un fichier Parquet contenant des données (`logs_processed.parquet`), **et si vous n'avez pas son équivalent csv**, vous devrez le convertir en CSV afin de l'utiliser pour initialiser votre base de données PostgreSQL ou pour d'autres analyses. Le script de conversion est déjà créé.

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

### 6. Nettoyage Docker
A la fin de votre utilisation, pensez à nettoyer en utilisant la commande suivante :
```bash
docker-compose down -v
```
