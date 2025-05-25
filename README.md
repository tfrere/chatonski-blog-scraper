# Chatonsky Text Scraper

Ce script Python permet de récupérer les articles du blog de Gregory Chatonsky (https://chatonsky.net/category/journal/) et de les sauvegarder dans un fichier texte.

## Fonctionnalités

- Récupération des articles dans l'ordre chronologique (du plus récent au plus ancien)
- Sauvegarde progressive (chaque article est sauvegardé dès qu'il est traité)
- Option pour limiter le nombre d'articles à récupérer
- Extraction du titre, de la date, de l'URL et du contenu de chaque article

## Installation

1. Assurez-vous d'avoir Python 3.9+ installé
2. Installez les dépendances avec Poetry :

```bash
poetry install
```

## Utilisation

### Récupérer tous les articles

```bash
poetry run python main.py
```

### Récupérer un nombre limité d'articles

Pour récupérer uniquement les N articles les plus récents :

```bash
poetry run python main.py --limit N
```

Par exemple, pour les 10 derniers articles :

```bash
poetry run python main.py --limit 10
```

## Format du fichier de sortie

Les articles sont sauvegardés dans le dossier `output/` avec un horodatage dans le nom du fichier.

Chaque article dans le fichier contient :

- Le titre de l'article
- La date de publication
- L'URL de l'article
- Le contenu textuel complet
- Un séparateur (`---------`) entre chaque article

## Dépendances

- beautifulsoup4 : Pour extraire le contenu des pages web
- requests : Pour effectuer les requêtes HTTP

## Notes

- Le script respecte le serveur avec un délai de 0.5 secondes entre chaque requête
- La sauvegarde progressive permet de ne pas perdre les données en cas d'interruption
- Les articles sont récupérés dans leur ordre de publication original
