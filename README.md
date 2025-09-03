# 🌍 Prédiction de la consommation d’énergie et des émissions de CO₂ des bâtiments – Ville de Seattle

### 📌 Contexte

Dans le cadre de son objectif de **neutralité carbone à l’horizon 2050**, la **ville de Seattle** cherche à mieux comprendre et anticiper la consommation d’énergie et les émissions de CO₂ de ses **bâtiments non résidentiels**.

Mission confiée :

* Analyser les données de consommation énergétique collectées en 2016.
* Construire des modèles supervisés capables de prédire :

  * la **consommation d’énergie**,
  * les **émissions de CO₂**.
* Déployer un service opérationnel permettant de mettre ces prédictions à disposition via une API.

---

### 🗂️ Données utilisées

* **3 376 relevés** effectués par les agents de la ville.
* Variables principales :

  * Type et usage des bâtiments,
  * Surface, nombre d’étages, parking, âge,
  * Localisation,
  * Indicateurs de consommation d’énergie (kBtu, électricité, gaz, vapeur),
  * Émissions de CO₂.

Prétraitements réalisés :

* Suppression des bâtiments d’habitation, doublons, colonnes inutiles.
* Nettoyage des données de mauvaise qualité.
* Gestion des valeurs manquantes.
* Suppression des outliers (ex. bâtiments > 80 étages).

---

### 🔎 Méthodologie

1. **Analyse exploratoire** et nettoyage des données.
2. **Feature engineering** :

   * Création de nouvelles variables (part électricité/gaz/vapeur, part du parking, âge du bâtiment).
   * Recentrage des distributions par transformation logarithmique.
3. **Sélection et optimisation des modèles** avec **Optuna**.

   * Modèles testés : Ridge, Lasso, ElasticNet, SVR, Random Forest, Gradient Boosting, XGBoost.
   * Maximisation du coefficient de détermination **R²**.
4. **Évaluation des performances**.
5. **Interprétabilité** : analyse des variables importantes avec **SHAP values**.
6. **Déploiement** via **BentoML** et conteneurisation AWS (ECR + ECS Fargate).

---

### 📈 Résultats principaux

* **Modèle consommation d’énergie** :

  * Meilleur modèle : **XGBoost**.
  * Performance : **R² ≈ 0.81** (le modèle explique 81 % de la variance).

* **Modèle émissions de CO₂** :

  * Meilleurs modèles : Ridge, Lasso, ElasticNet, SVR.
  * Performance : **R² ≈ 0.82**.

* **Variables les plus influentes** :

  * Surface totale (GFA),
  * Surface principale du bâtiment,
  * Usage principal du bâtiment,
  * Part d’électricité et de gaz,
  * Âge du bâtiment.

---

### 🚀 Déploiement

* Service déployé avec **BentoML**.
* Création d’une **API REST** permettant de requêter les deux modèles.
* Conteneurisation via **Docker** et déploiement sur **AWS ECS Fargate** (image stockée dans AWS ECR).
* Utilisation de **Pydantic** pour les règles de validation des entrées.
