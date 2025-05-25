# Chatonsky Text Scraper

Ce script Python permet de récupérer tous les articles du blog de Gregory Chatonsky (https://chatonsky.net/category/journal/) et de les sauvegarder dans un fichier texte.

## Installation

1. Assurez-vous d'avoir Python 3.9+ installé
2. Installez les dépendances avec Poetry :

```bash
poetry install
```

## Utilisation

Pour exécuter le script :

```bash
poetry run python main.py
```

Le script va :

1. Récupérer le flux RSS du blog
2. Extraire le contenu de chaque article
3. Sauvegarder tous les textes dans un fichier dans le dossier `output/`

Le nom du fichier de sortie inclut un horodatage pour éviter les écrasements accidentels.

## Structure du fichier de sortie

Chaque article dans le fichier de sortie contient :

- Le titre de l'article
- La date de publication
- L'URL de l'article
- Le contenu textuel complet
- Une ligne de séparation

## Dépendances

- feedparser : Pour parser le flux RSS
- beautifulsoup4 : Pour extraire le contenu des pages web
- requests : Pour effectuer les requêtes HTTP
