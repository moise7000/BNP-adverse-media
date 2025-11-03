# Documentation KYC Classification Matrix

## Vue d'ensemble

La **KYC Classification Matrix** est un système de classification des informations adverses pour le processus KYC (Know Your Customer) bancaire. Elle permet d'évaluer systématiquement les risques associés aux clients en fonction de différents types d'infractions et de leur gravité.

## Installation et Initialisation
```python
from kyc_matrix import KYCClassificationMatrix

# Initialiser la matrice
matrix = KYCClassificationMatrix()
```

## Fonctionnalités Principales

### 1. Classification des Informations Adverses

#### Obtenir une règle de classification

Permet de déterminer le niveau de matérialité et la procédure d'escalade pour une infraction spécifique.
```python
from kyc_matrix import WrongdoingCategory

# Rechercher une règle
rule = matrix.get_classification(
    category=WrongdoingCategory.AML_CFT,
    action_type="Criminal Conviction"
)

if rule:
    print(f"Niveau: {rule.materiality_level.value}")
    print(f"Envoyer au MLRO: {rule.escalation.send_to_mlro}")
    print(f"Description: {rule.description}")
```

**Résultat:**
```
Niveau: Highly Material
Envoyer au MLRO: True
Description: Criminal conviction
```

---

### 2. Exploration des Catégories

#### Lister toutes les catégories disponibles
```python
# Obtenir toutes les catégories
categories = matrix.get_all_categories()

for category in categories:
    print(category.value)
```

**Catégories principales:**
- AML/CFT Matters (Blanchiment d'argent)
- Tax evasion (Évasion fiscale)
- Sanctions & embargoes
- Bribery & Corruption (Corruption)
- Fraud (Fraude)
- Market abuse (Abus de marché)
- Et 8 autres...

#### Obtenir toutes les règles d'une catégorie
```python
# Récupérer toutes les règles pour la fraude
rules = matrix.get_rules_by_category(WrongdoingCategory.FRAUD)

for rule in rules:
    print(f"{rule.action_type}: {rule.materiality_level.value}")
```

---

### 3. Niveaux de Matérialité

#### Les 8 niveaux (du plus grave au moins grave)

| Niveau | Description | Exemple |
|--------|-------------|---------|
| **Highly Material** | Le plus grave | Condamnation criminelle |
| **Significantly Material** | Très grave | Enquête criminelle en cours |
| **Material** | Grave | Actions réglementaires en cours |
| **Moderately Material** | Modérément grave | Règlements criminels |
| **Precautionary** | Précautionnaire | Accusations criminelles |
| **Closed Matter** | Affaire close | Pénalités civiles significatives |
| **Non-Relevant** | Non pertinent | Allégations médiatiques |
| **Speculation** | Spéculation | Accusations rejetées |
```python
# Obtenir tous les niveaux
levels = matrix.get_all_materiality_levels()

# Rechercher toutes les règles "Highly Material"
highly_material_rules = matrix.search_rules_by_materiality(
    MaterialityLevel.HIGHLY_MATERIAL
)
```

---

### 4. Procédures d'Escalade

#### Identifier le type d'escalade

Deux types de procédures selon la gravité:

**Escalade Haute Priorité** (MLRO):
- AML/CFT
- Évasion fiscale
- Sanctions
- Corruption
- Fraude au niveau senior
- Déficiences conformité

**Escalade 4 Eyes**:
- Abus de marché
- Manipulation de marché
- Vente abusive
- Violations administratives
- Autres infractions réglementaires
```python
# Vérifier si une catégorie est haute priorité
is_high = matrix.is_high_priority_category(WrongdoingCategory.AML_CFT)
# Retourne: True

# Obtenir les exigences d'escalade
escalation = matrix.get_escalation_requirements(WrongdoingCategory.FRAUD)
print(f"MLRO: {escalation.send_to_mlro}")
print(f"Compliance: {escalation.cc_compliance}")
print(f"Four eyes: {escalation.four_eyes}")
```

---

### 5. Facteurs Atténuants et Aggravants

#### Facteurs Atténuants

Ces éléments peuvent réduire la gravité perçue de l'infraction.
```python
# Obtenir toutes les dimensions
dimensions = matrix.get_all_mitigating_dimensions()
# ['Information Stage', 'Provenance', 'Underlying Breach', 
#  'Client Remediation', 'Outcomes', 'Client Profile', 'Timescales']

# Obtenir les facteurs pour une dimension
factors = matrix.get_mitigating_factors_by_dimension("Client Remediation")
```

**Exemples de facteurs atténuants:**
- ✓ Cas isolé (non systémique)
- ✓ Limité aux employés juniors
- ✓ Client a volontairement signalé l'infraction
- ✓ Amélioration des contrôles internes
- ✓ Changement d'équipe de direction
- ✓ Conduite historique (ancienne)

#### Facteurs Aggravants

Ces éléments augmentent la gravité perçue.
```python
# Obtenir les facteurs aggravants
dimensions = matrix.get_all_aggravating_dimensions()
factors = matrix.get_aggravating_factors_by_dimension("Pattern")
```

**Exemples de facteurs aggravants:**
- ✗ Infractions répétées
- ✗ Gouvernance faible
- ✗ Implication de la direction
- ✗ Multiples autorités enquêtent
- ✗ Pays sur liste noire FATF

---

### 6. Issues Possibles (Outcomes)

#### Les 7 actions possibles
```python
# Obtenir toutes les issues
outcomes = matrix.potential_outcomes

# Obtenir une issue spécifique
outcome = matrix.get_outcome_by_id("7")
print(outcome['outcome'])  # "Client exit"
```

| ID | Issue | Description |
|----|-------|-------------|
| 1 | Mitigation adéquate | Mesures suffisantes en place |
| 2 | Surveillance renforcée | Monitoring des news continues |
| 3 | Revue historique | Analyse transactions passées |
| 4 | Mesures EDD supplémentaires | Révision politiques AML/CFT |
| 5 | Revue ciblée | Analyse paiements spécifiques |
| 6 | Restriction de produits | Limitation services |
| 7 | **Sortie client** | Fin de la relation |

---

### 7. Statistiques et Exports

#### Obtenir des statistiques
```python
stats = matrix.get_summary_statistics()

print(f"Catégories totales: {stats['total_categories']}")
print(f"Règles totales: {stats['total_rules']}")
print(f"Catégories haute priorité: {stats['high_priority_categories']}")
```

**Résultat:**
```
Catégories totales: 14
Règles totales: 154
Catégories haute priorité: 7
Facteurs atténuants: 21
Facteurs aggravants: 6
Issues possibles: 7
```

#### Exporter en JSON
```python
# Export vers fichier JSON
success = matrix.export_to_json("kyc_matrix.json")

# Ou obtenir un dictionnaire
matrix_dict = matrix.to_dict()
```

**Structure JSON:**
```json
{
  "matrix": {
    "AML/CFT Matters": [
      {
        "action_type": "Criminal Conviction",
        "materiality_level": "Highly Material",
        "description": "...",
        "escalation": {
          "second_line": "KYI Group Mgr",
          "send_to_mlro": true,
          "cc_compliance": true,
          "four_eyes": false
        }
      }
    ]
  },
  "mitigating_factors": {...},
  "aggravating_factors": {...},
  "potential_outcomes": [...]
}
```

---

### 8. Affichage et Documentation

#### Afficher un résumé de catégorie
```python
# Afficher toutes les informations d'une catégorie
matrix.print_category_summary(WrongdoingCategory.AML_CFT)
```

**Résultat:**
```
============================================================
Catégorie: AML/CFT Matters
============================================================

Procédure d'escalade:
  - Seconde ligne: KYI Group Mgr
  - Envoyer au MLRO: Oui
  - CC Compliance: Oui
  - Four eyes: Non

Règles de classification (11):

1. Criminal Conviction
   Niveau: Highly Material
   Description: Criminal conviction

2. Open criminal investigation
   Niveau: Significantly Material
   Description: Open criminal investigation
...
```

---

## Cas d'Usage Pratiques

### Cas 1: Évaluation d'une Information Adverse
```python
# Scénario: Client avec enquête criminelle pour fraude
category = WrongdoingCategory.FRAUD
action = "Open criminal investigation"

# 1. Obtenir la classification
rule = matrix.get_classification(category, action)

# 2. Déterminer le niveau de gravité
print(f"Niveau: {rule.materiality_level.value}")
# Significantly Material

# 3. Identifier qui notifier
if rule.escalation.send_to_mlro:
    print("Action: Notifier MLRO immédiatement")
    print("CC: Équipe Compliance")
```

### Cas 2: Analyse des Facteurs Contextuels
```python
# Facteurs atténuants identifiés
mitigating = [
    "Cas isolé (non répété)",
    "Client a coopéré avec l'enquête",
    "Changement de direction effectué"
]

# Facteurs aggravants identifiés
aggravating = [
    "Implication de la haute direction",
    "Multiples régulateurs enquêtent"
]

# Décision: Les facteurs aggravants l'emportent
# Recommandation: Enhanced monitoring + EDD measures
```

### Cas 3: Décision sur la Relation Client
```python
# Après évaluation complète
category = WrongdoingCategory.AML_CFT
materiality = MaterialityLevel.HIGHLY_MATERIAL

# Facteurs aggravants dominants
# + Pas de remédiation efficace
# + Client sur liste grise FATF

# Décision recommandée
outcome = matrix.get_outcome_by_id("7")
print(f"Recommandation: {outcome['outcome']}")
# "Client exit"
```

---

## Architecture des Classes
```
KYCClassificationMatrix
├── matrix: Dict[WrongdoingCategory, List[ClassificationRule]]
├── mitigating_factors: Dict[str, List[str]]
├── aggravating_factors: Dict[str, List[str]]
└── potential_outcomes: List[Dict]

ClassificationRule
├── action_type: str
├── materiality_level: MaterialityLevel
├── escalation: EscalationProcedure
└── description: str

EscalationProcedure
├── second_line: str
├── send_to_mlro: bool
├── cc_compliance: bool
└── four_eyes: bool
```

---

## Méthodes Principales - Référence Rapide

| Méthode | Usage | Retour |
|---------|-------|--------|
| `get_classification()` | Obtenir règle pour catégorie + action | `ClassificationRule` |
| `get_all_categories()` | Lister toutes les catégories | `List[WrongdoingCategory]` |
| `get_rules_by_category()` | Toutes règles d'une catégorie | `List[ClassificationRule]` |
| `is_high_priority_category()` | Vérifier si escalade MLRO | `bool` |
| `get_escalation_requirements()` | Procédure d'escalade | `EscalationProcedure` |
| `search_rules_by_materiality()` | Rechercher par niveau | `Dict[...]` |
| `get_mitigating_factors_by_dimension()` | Facteurs atténuants | `List[str]` |
| `get_summary_statistics()` | Statistiques globales | `Dict` |
| `export_to_json()` | Exporter vers fichier | `bool` |
| `print_category_summary()` | Afficher résumé | `None` |




