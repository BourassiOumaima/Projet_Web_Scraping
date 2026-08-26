<<<<<<< HEAD
#  Indeed Job Scraper - Application de recherche d'offres

Application Flask moderne pour scraper et afficher les offres d'emploi et de stages depuis Indeed (France et Maroc).

##  Fonctionnalités

-  Recherche par mot-clé et pays
-  Statistiques en temps réel
-  Dates formatées et complètes
-  Affichage du salaire (si disponible)
-  Type de contrat
-  Mise à jour automatique toutes les 2 heures
-  Interface responsive et moderne
-  Design avec animations et effets visuels

##  Prérequis

- Python 3.8 ou supérieur
- Google Chrome installé sur votre système
- ChromeDriver (géré automatiquement par webdriver-manager)

##  Installation

### 1. Créer la structure du projet
```bash
mkdir indeed-scraper
cd indeed-scraper
mkdir templates
```

### 2. Créer un environnement virtuel (recommandé)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Structure du projet finale
```
indeed-scraper/
¦
+-- app.py                          # Application Flask principale
+-- scrape_indeed_selenium.py       # Script de scraping
+-- requirements.txt                # Dépendances Python
+-- README.md                       # Ce fichier
+-- templates/
    +-- index.html                  # Interface utilisateur
```

## ?? Utilisation

### Lancer l'application
```bash
python app.py
```

L'application sera accessible sur : `http://127.0.0.1:5000`

### Première utilisation

1. **Chargement initial** : L'application lance automatiquement une recherche au démarrage
2. **Recherche personnalisée** : 
   - Entrez un mot-clé (ex: "Data Scientist", "Stage Marketing")
   - Sélectionnez le pays (France ???? ou Maroc ????)
   - Cliquez sur "?? Rechercher"
3. **Résultats** : Les offres s'affichent sous forme de cartes avec toutes les informations

### Mise à jour automatique

L'application se met à jour automatiquement **toutes les 2 heures** pour récupérer les nouvelles offres.

## ??? Configuration

### Modifier les paramètres par défaut

Dans `app.py`, vous pouvez ajuster :
```python
mot_cle_defaut = "Data Scientist"  # Recherche par défaut
pays_defaut = "fr"                  # Pays par défaut (fr ou ma)
```

### Modifier la fréquence de mise à jour
```python
# Dans app.py, ligne du scheduler
scheduler.add_job(func=mise_a_jour_offres, trigger="interval", hours=2)
# Changez 'hours=2' par la valeur souhaitée
```

### Augmenter le nombre de pages scrapées
```python
# Dans app.py, dans la route index()
offres_cache = scrape_indeed_selenium(mot_cle, pays=pays, pages=1)
# Changez 'pages=1' par le nombre souhaité (attention au temps d'exécution)
```

##  Informations extraites

Pour chaque offre :
-  **Titre du poste**
-  **Entreprise**
-  **Lieu**
-  **Date de publication** (formatée)
-  **Salaire** (si disponible)
-  **Type de contrat** (si disponible)
-  **Lien vers l'offre**
-  **Catégorie/Mot-clé**
-  **Pays**

##  Personnalisation de l'interface

### Changer les couleurs du gradient

Dans `templates/index.html`, modifiez les couleurs CSS :
```css
body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Remplacez par vos couleurs préférées */
}
```

### Modifier le nombre de colonnes
```html
<!-- Dans templates/index.html -->
<div class="col-lg-4 col-md-6 mb-4 fade-in">
<!-- 
  lg-4 = 3 colonnes sur desktop
  md-6 = 2 colonnes sur tablette
  Modifiez selon vos besoins
-->
```

##  Résolution des problèmes

### Problème : ChromeDriver introuvable

**Solution** : ChromeDriver est géré automatiquement par `webdriver-manager`. Assurez-vous que Chrome est installé.

### Problème : Aucune offre trouvée

**Causes possibles** :
- Indeed a modifié sa structure HTML
- Le mot-clé ne retourne aucun résultat
- Problème de connexion Internet

**Solution** : Vérifiez votre connexion et essayez un autre mot-clé

### Problème : L'application est lente

**Solution** : 
- Réduisez le nombre de pages : `pages=1`
- Indeed limite parfois les requêtes trop fréquentes

### Problème : Erreur de port déjà utilisé

**Solution** :
```bash
# Changez le port dans app.py
app.run(debug=True, use_reloader=False, port=5001)
```

##  Notes importantes

-  Le scraping doit respecter les conditions d'utilisation d'Indeed
-  Le temps de chargement dépend du nombre de pages et de la connexion
-  Le mode `--headless` de Selenium rend le navigateur invisible
-  Les données ne sont pas sauvegardées (rechargées à chaque recherche)

##  Améliorations futures possibles

- [ ] Export des résultats en CSV/Excel
- [ ] Sauvegarde des offres dans une base de données
- [ ] Filtres avancés (date, type de contrat, salaire)
- [ ] Notifications par email pour nouvelles offres
- [ ] Support de pays supplémentaires
- [ ] Graphiques de statistiques
- [ ] Historique des recherches

##  Licence

Ce projet est à usage éducatif. Respectez les conditions d'utilisation d'Indeed.

##  Support

Pour toute question ou problème :
1. Vérifiez ce README
2. Consultez les messages d'erreur dans le terminal
3. Vérifiez que toutes les dépendances sont installées

##  Auteur

Projet de Web Scraping - Indeed Job Scraper

##  Contact

Pour toute question, suggestion ou amélioration, n'hésitez pas à ouvrir une issue.

---

**Bonne recherche d'emploi !**
```

---

