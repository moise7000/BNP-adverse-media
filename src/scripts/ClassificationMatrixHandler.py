from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class MaterialityLevel(Enum):
    """
    Énumération des niveaux de matérialité pour l'évaluation des informations adverses.

    Ces niveaux permettent de classer la gravité des informations adverses découvertes
    lors du processus KYC (Know Your Customer).

    Attributs:
        HIGHLY_MATERIAL: Niveau le plus élevé - Condamnation criminelle
        SIGNIFICANTLY_MATERIAL: Enquête criminelle en cours
        MATERIAL: Actions réglementaires ou d'application en cours
        MODERATELY_MATERIAL: Règlements/pénalités criminels
        PRECAUTIONARY: Accusations criminelles
        CLOSED_MATTER: Affaire close - pénalités civiles significatives
        NON_RELEVANT: Non pertinent - allégations ou enquêtes civiles
        SPECULATION: Spéculation - accusations rejetées ou exonération
    """
    HIGHLY_MATERIAL = "Highly Material"
    SIGNIFICANTLY_MATERIAL = "Significantly Material"
    MATERIAL = "Material"
    MODERATELY_MATERIAL = "Moderately Material"
    PRECAUTIONARY = "Precautionary"
    CLOSED_MATTER = "Closed matter"
    NON_RELEVANT = "Non-Relevant"
    SPECULATION = "Speculation"


class WrongdoingCategory(Enum):
    """
    Énumération des catégories de mauvaise conduite évaluées dans le processus KYC.

    Ces catégories couvrent l'ensemble des types d'infractions financières et réglementaires
    qui peuvent affecter l'évaluation d'un client bancaire.

    Attributs:
        AML_CFT: Blanchiment d'argent et financement du terrorisme
        TAX_EVASION: Évasion fiscale (réelle ou facilitation)
        SANCTIONS_EMBARGOES: Violations de sanctions et embargos
        BRIBERY_CORRUPTION: Corruption, pots-de-vin, détournement de fonds
        WRONGDOING_BOARD_SENIOR: Fautes au niveau du conseil d'administration ou direction
        FRAUD: Fraude (titres, conspiracy)
        FIN_CRIME_DEFICIENCIES: Déficiences dans les programmes de conformité
        MARKET_ABUSE: Abus de marché incluant délit d'initié
        MARKET_MANIPULATION: Manipulation de marché, fixation des prix
        MISSELLING: Vente abusive
        REPUTATIONAL_CSR: Risques réputationnels, préoccupations RSE
        ADMINISTRATIVE_VIOLATIONS: Violations administratives (archivage, etc.)
        OTHER_REGULATORY: Autres violations réglementaires
        DOMESTIC_MATTERS: Affaires domestiques (civiles, sociales, etc.)
    """
    AML_CFT = "AML/CFT Matters"
    TAX_EVASION = "Tax evasion (actual or facilitation of)"
    SANCTIONS_EMBARGOES = "Sanctions & embargoes"
    BRIBERY_CORRUPTION = "Bribery & Corruption (e.g, graft, kickbacks, embezzlement)"
    WRONGDOING_BOARD_SENIOR = "Wrong Doing at board/senior level"
    FRAUD = "Fraud (Securities, conspiracy to commit fraud)"
    FIN_CRIME_DEFICIENCIES = "Deficiencies in Fin Crime Compliance Program, internal controls"
    MARKET_ABUSE = "Market abuse inc. Insider Trading"
    MARKET_MANIPULATION = "Market manipulation, price fixing, or rate rigging"
    MISSELLING = "Misselling"
    REPUTATIONAL_CSR = "Implications to reputational risk, CSR concerns, or major financial impact of a firm"
    ADMINISTRATIVE_VIOLATIONS = "Administrative violations such as Record Keeping Violations"
    OTHER_REGULATORY = "Other regulatory breaches including internal control failures"
    DOMESTIC_MATTERS = "Domestic Matters"


@dataclass
class EscalationProcedure:
    """
    Procédure d'escalade à suivre selon le type et la gravité de l'infraction.

    Cette classe définit les étapes de remontée d'information et les personnes
    à notifier lors de la découverte d'informations adverses.

    Attributs:
        second_line (str): Responsable de deuxième ligne à contacter (ex: "KYI Group Mgr")
        send_to_mlro (bool): Indique si le MLRO (Money Laundering Reporting Officer) doit être notifié
        cc_compliance (bool): Indique si l'équipe Compliance doit être mise en copie
        four_eyes (bool): Indique si une validation à 4 yeux est requise (par défaut: False)
    """
    second_line: str
    send_to_mlro: bool
    cc_compliance: bool
    four_eyes: bool = False


@dataclass
class ClassificationRule:
    """
    Règle de classification pour un type d'action et d'information adverse.

    Cette classe regroupe tous les éléments nécessaires pour classifier une information
    adverse découverte lors du processus KYC.

    Attributs:
        action_type (str): Type d'action (ex: "Criminal Conviction", "Open investigation")
        materiality_level (MaterialityLevel): Niveau de matérialité de l'information
        escalation (EscalationProcedure): Procédure d'escalade à suivre
        description (str): Description détaillée de la règle
    """
    action_type: str
    materiality_level: MaterialityLevel
    escalation: EscalationProcedure
    description: str


@dataclass
class WrongdoingType:
    """
    Type de mauvaise conduite avec ses règles de classification associées.

    Cette classe regroupe une catégorie de mauvaise conduite avec toutes les règles
    de classification qui s'y appliquent.

    Attributs:
        category (WrongdoingCategory): Catégorie de la mauvaise conduite
        classification_rules (List[ClassificationRule]): Liste des règles de classification applicables
        notes (Optional[str]): Notes additionnelles sur cette catégorie (par défaut: None)
    """
    category: WrongdoingCategory
    classification_rules: List[ClassificationRule]
    notes: Optional[str] = None


class KYCClassificationMatrix:
    """
    Matrice de classification KYC/AML pour l'évaluation des informations adverses.

    Cette classe principale gère l'ensemble de la matrice de classification utilisée
    pour évaluer les informations adverses dans le cadre du processus KYC bancaire.
    Elle permet d'accéder aux règles de classification, aux facteurs atténuants/aggravants,
    et aux issues possibles pour une relation client.

    Attributs:
        matrix (Dict[WrongdoingCategory, List[ClassificationRule]]): Dictionnaire contenant
            toutes les règles de classification par catégorie
        mitigating_factors (Dict[str, List[str]]): Facteurs atténuants par dimension
        aggravating_factors (Dict[str, List[str]]): Facteurs aggravants par dimension
        potential_outcomes (List[Dict[str, str]]): Liste des issues possibles
    """

    def __init__(self):
        """
        Initialise la matrice de classification KYC.

        Objectif:
            Construire l'ensemble de la matrice avec toutes ses composantes :
            règles de classification, facteurs atténuants/aggravants, et issues possibles.

        Paramètres:
            Aucun

        Retourne:
            Instance de KYCClassificationMatrix initialisée
        """
        self.matrix = self._build_matrix()
        self.mitigating_factors = self._build_mitigating_factors()
        self.aggravating_factors = self._build_aggravating_factors()
        self.potential_outcomes = self._build_potential_outcomes()

    def _build_matrix(self) -> Dict[WrongdoingCategory, List[ClassificationRule]]:
        """
        Construit la matrice complète de classification.

        Objectif:
            Créer l'ensemble des règles de classification pour toutes les catégories
            de mauvaise conduite, avec les procédures d'escalade appropriées.
            Les catégories prioritaires (AML/CFT, fraude, etc.) ont une escalade
            vers le MLRO, tandis que d'autres utilisent la procédure "4 eyes".

        Paramètres:
            Aucun (méthode privée)

        Retourne:
            Dict[WrongdoingCategory, List[ClassificationRule]]: Dictionnaire mappant
            chaque catégorie de mauvaise conduite à sa liste de règles de classification.

        Structure retournée:
            {
                WrongdoingCategory.AML_CFT: [
                    ClassificationRule(...),
                    ClassificationRule(...),
                    ...
                ],
                WrongdoingCategory.FRAUD: [...],
                ...
            }
        """

        # Procédures d'escalade standards
        escalation_high_priority = EscalationProcedure(
            second_line="KYI Group Mgr",
            send_to_mlro=True,
            cc_compliance=True,
            four_eyes=False
        )

        escalation_four_eyes = EscalationProcedure(
            second_line="KYI Group Mgr",
            send_to_mlro=False,
            cc_compliance=False,
            four_eyes=True
        )

        # Catégories prioritaires (AML/CFT, Tax Evasion, Sanctions, Bribery, Board/Senior, Fraud, Fin Crime Deficiencies)
        high_priority_categories = [
            WrongdoingCategory.AML_CFT,
            WrongdoingCategory.TAX_EVASION,
            WrongdoingCategory.SANCTIONS_EMBARGOES,
            WrongdoingCategory.BRIBERY_CORRUPTION,
            WrongdoingCategory.WRONGDOING_BOARD_SENIOR,
            WrongdoingCategory.FRAUD,
            WrongdoingCategory.FIN_CRIME_DEFICIENCIES
        ]

        # Catégories avec procédure 4 eyes
        four_eyes_categories = [
            WrongdoingCategory.MARKET_ABUSE,
            WrongdoingCategory.MARKET_MANIPULATION,
            WrongdoingCategory.MISSELLING,
            WrongdoingCategory.REPUTATIONAL_CSR,
            WrongdoingCategory.ADMINISTRATIVE_VIOLATIONS,
            WrongdoingCategory.OTHER_REGULATORY,
            WrongdoingCategory.DOMESTIC_MATTERS
        ]

        matrix = {}

        # Règles communes pour toutes les catégories
        common_rules = [
            ClassificationRule(
                action_type="Criminal Conviction",
                materiality_level=MaterialityLevel.HIGHLY_MATERIAL,
                escalation=escalation_high_priority,
                description="Criminal conviction"
            ),
            ClassificationRule(
                action_type="Open criminal investigation",
                materiality_level=MaterialityLevel.SIGNIFICANTLY_MATERIAL,
                escalation=escalation_high_priority,
                description="Open criminal investigation"
            ),
            ClassificationRule(
                action_type="Open enforcement actions or regulatory actions",
                materiality_level=MaterialityLevel.MATERIAL,
                escalation=escalation_high_priority,
                description="Open enforcement actions or other regulatory actions in rules of law jurisdictions"
            ),
            ClassificationRule(
                action_type="Criminal settlements / penalties",
                materiality_level=MaterialityLevel.MODERATELY_MATERIAL,
                escalation=escalation_high_priority,
                description="Criminal settlements / penalties"
            ),
            ClassificationRule(
                action_type="Criminal charges",
                materiality_level=MaterialityLevel.PRECAUTIONARY,
                escalation=escalation_high_priority,
                description="Criminal charges"
            ),
            ClassificationRule(
                action_type="Significant civil penalties or fines",
                materiality_level=MaterialityLevel.CLOSED_MATTER,
                escalation=escalation_high_priority,
                description="Significant civil penalties or fines, and/or disgorgements as per jurisdiction reference scale"
            ),
            ClassificationRule(
                action_type="Repeated allegations from reputable media",
                materiality_level=MaterialityLevel.NON_RELEVANT,
                escalation=escalation_high_priority,
                description="Single or repeated allegations from reputable media sources"
            ),
            ClassificationRule(
                action_type="Open civil investigation",
                materiality_level=MaterialityLevel.NON_RELEVANT,
                escalation=escalation_high_priority,
                description="Open civil investigation / repeated accusations from reputable investigative journalism sources, opinion editorials"
            ),
            ClassificationRule(
                action_type="Lower civil penalties or fines",
                materiality_level=MaterialityLevel.NON_RELEVANT,
                escalation=escalation_high_priority,
                description="Lower civil penalties or fines, and/or disgorgements as per jurisdiction reference scale / investigations, charges or settlements from other jurisdictions"
            ),
            ClassificationRule(
                action_type="Isolated allegations NOT from reputable sources",
                materiality_level=MaterialityLevel.SPECULATION,
                escalation=escalation_high_priority,
                description="Isolated allegations NOT from reputable sources"
            ),
            ClassificationRule(
                action_type="Dismissal of charges or Exoneration",
                materiality_level=MaterialityLevel.SPECULATION,
                escalation=escalation_high_priority,
                description="Dismissal of charges or Exoneration by credible judicial system"
            )
        ]

        # Appliquer les règles avec les bonnes procédures d'escalade
        for category in WrongdoingCategory:
            if category in high_priority_categories:
                # Garder escalation_high_priority
                matrix[category] = common_rules.copy()
            elif category in four_eyes_categories:
                # Remplacer par escalation_four_eyes
                matrix[category] = [
                    ClassificationRule(
                        action_type=rule.action_type,
                        materiality_level=rule.materiality_level,
                        escalation=escalation_four_eyes,
                        description=rule.description
                    ) for rule in common_rules
                ]
            else:
                matrix[category] = common_rules.copy()

        return matrix

    def _build_mitigating_factors(self) -> Dict[str, List[str]]:
        """
        Construit la liste des facteurs atténuants pour l'évaluation.

        Objectif:
            Fournir une liste structurée de tous les éléments qui peuvent atténuer
            la gravité d'une information adverse. Ces facteurs sont utilisés pour
            nuancer l'évaluation du risque client.

        Paramètres:
            Aucun (méthode privée)

        Retourne:
            Dict[str, List[str]]: Dictionnaire où chaque clé est une dimension d'évaluation
            (ex: "Information Stage", "Client Remediation") et chaque valeur est une liste
            de facteurs atténuants pour cette dimension.

        Structure retournée:
            {
                "Information Stage": [
                    "Rumor < allegation < accusation < investigation",
                    ...
                ],
                "Client Remediation": [
                    "Voluntarily reported wrongdoing",
                    ...
                ],
                ...
            }
        """
        return {
            "Information Stage": [
                "Rumor < allegation < accusation < investigation",
                "Allegations / accusations not followed by formal investigations"
            ],
            "Provenance": [
                "Less reputable sources versus reputable sources",
                "Large number of reputable economic / financial media sources"
            ],
            "Underlying Breach": [
                "Isolated case (not repeating/systemic)",
                "Limited to low ranking employees only",
                "Limited size and scale of illicit activity (local geographical spread, low alleged value)",
                "Absence of clear intent to violate laws/regulations",
                "No bearing on current business operations",
                "Investigation targeted specific branch/affiliate entirely separate from client"
            ],
            "Client Remediation": [
                "Improvements to internal controls and/or compliance culture",
                "Implemented additional controls or enhancements to policies",
                "Enhanced training",
                "Voluntarily reported wrongdoing and cooperated with investigation",
                "Dismissed, terminated or sued individuals involved",
                "Changed management team"
            ],
            "Outcomes": [
                "De minimus fines in relation to administrative breaches",
                "Fines appear indicative of regulatory environment client operates within",
                "Investigation/settlement appear to be isolated event with remedial actions",
                "No additional breaches committed"
            ],
            "Client Profile": [
                "Transparency of top management relationships with BNPP",
                "Longevity of top management relationships",
                "Operates as regulated financial institution subject to oversight",
                "Large, multinational corporation subject to federal regulations",
                "Products ringfenced (language in contracts protecting BNPP)",
                "Established relationship with BNPP in low sensitive jurisdiction"
            ],
            "Timescales": [
                "Underlying conduct and/or investigation reasonably historic"
            ]
        }

    def _build_aggravating_factors(self) -> Dict[str, List[str]]:
        """
        Construit la liste des facteurs aggravants pour l'évaluation.

        Objectif:
            Fournir une liste structurée de tous les éléments qui peuvent aggraver
            la gravité d'une information adverse. Ces facteurs augmentent le niveau
            de risque perçu pour la relation client.

        Paramètres:
            Aucun (méthode privée)

        Retourne:
            Dict[str, List[str]]: Dictionnaire où chaque clé est une dimension d'évaluation
            (ex: "Pattern", "Senior Involvement") et chaque valeur est une liste de facteurs
            aggravants pour cette dimension.

        Structure retournée:
            {
                "Pattern": [
                    "Repeated and recurring breaches",
                    ...
                ],
                "Senior Involvement": [
                    "Persons involved hold positions with significant influence",
                    ...
                ],
                ...
            }
        """
        return {
            "Pattern": [
                "Repeated and recurring breaches suggesting weak governance",
                "Poor internal control framework",
                "Large number of regulatory authorities investigating"
            ],
            "Senior Involvement": [
                "Persons involved hold positions with significant influence",
                "Influence over key decisions and company's strategies"
            ],
            "Outcomes": [
                "Repeated convictions",
                "Adverse information showing patterns or trends"
            ],
            "Client Profile": [
                "Client operating in regulated FI but in country with weak monitoring",
                "Country on FATF blacklist or grey list"
            ]
        }

    def _build_potential_outcomes(self) -> List[Dict[str, str]]:
        """
        Construit la liste des issues possibles pour la relation client.

        Objectif:
            Définir l'ensemble des actions qui peuvent être prises suite à l'évaluation
            d'informations adverses, allant de la simple surveillance renforcée jusqu'à
            la sortie du client.

        Paramètres:
            Aucun (méthode privée)

        Retourne:
            List[Dict[str, str]]: Liste de dictionnaires, chacun représentant une issue
            possible avec son identifiant, son nom et sa description.

        Structure retournée:
            [
                {
                    "id": "1",
                    "outcome": "Deemed adequate mitigation in place",
                    "description": "Mitigation measures are considered sufficient"
                },
                {
                    "id": "2",
                    "outcome": "Enhanced ongoing monitoring...",
                    "description": "Required when investigations are starting..."
                },
                ...
            ]
        """
        return [
            {
                "id": "1",
                "outcome": "Deemed adequate mitigation in place",
                "description": "Mitigation measures are considered sufficient"
            },
            {
                "id": "2",
                "outcome": "Enhanced ongoing monitoring of adverse news required",
                "description": "Required when investigations are starting until formal outcome is public"
            },
            {
                "id": "3",
                "outcome": "Look back on past transactions and Enhanced ongoing monitoring",
                "description": "Review historical transactions with enhanced monitoring"
            },
            {
                "id": "4",
                "outcome": "Inclusion of further EDD measures",
                "description": "Review of client AML/CFT/AB&C policies procedures etc"
            },
            {
                "id": "5",
                "outcome": "Targeted payment/activity review",
                "description": "Dependent on specifics of the adverse news"
            },
            {
                "id": "6",
                "outcome": "Restriction of certain products",
                "description": "Dependent on the specifics of the adverse news"
            },
            {
                "id": "7",
                "outcome": "Client exit",
                "description": "Termination of client relationship"
            }
        ]

    def get_classification(self, category: WrongdoingCategory, action_type: str) -> Optional[ClassificationRule]:
        """
        Obtient la règle de classification pour une catégorie et un type d'action donnés.

        Objectif:
            Rechercher et retourner la règle de classification appropriée en fonction
            de la catégorie d'infraction et du type d'action (ex: condamnation, enquête).
            Cette méthode permet d'obtenir rapidement le niveau de matérialité et la
            procédure d'escalade à suivre.

        Paramètres:
            category (WrongdoingCategory): Catégorie de mauvaise conduite à évaluer
                (ex: WrongdoingCategory.AML_CFT, WrongdoingCategory.FRAUD)
            action_type (str): Type d'action recherché (ex: "Criminal Conviction",
                "Open investigation"). La recherche est insensible à la casse et
                utilise une correspondance partielle.

        Retourne:
            Optional[ClassificationRule]: La règle de classification trouvée si elle existe,
            None si aucune règle ne correspond aux critères de recherche.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> rule = matrix.get_classification(
            ...     WrongdoingCategory.AML_CFT,
            ...     "Criminal Conviction"
            ... )
            >>> if rule:
            ...     print(f"Niveau: {rule.materiality_level.value}")
            Niveau: Highly Material
        """
        rules = self.matrix.get(category, [])
        for rule in rules:
            if action_type.lower() in rule.action_type.lower():
                return rule
        return None

    def get_all_categories(self) -> List[WrongdoingCategory]:
        """
        Obtient la liste complète de toutes les catégories de mauvaise conduite.

        Objectif:
            Fournir l'ensemble des catégories disponibles dans la matrice pour
            permettre l'itération ou la sélection parmi toutes les catégories possibles.

        Paramètres:
            Aucun

        Retourne:
            List[WrongdoingCategory]: Liste de toutes les catégories de mauvaise conduite
            disponibles dans l'énumération WrongdoingCategory.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> categories = matrix.get_all_categories()
            >>> for cat in categories:
            ...     print(cat.value)
            AML/CFT Matters
            Tax evasion (actual or facilitation of)
            ...
        """
        return list(WrongdoingCategory)

    def get_all_materiality_levels(self) -> List[MaterialityLevel]:
        """
        Obtient la liste complète de tous les niveaux de matérialité.

        Objectif:
            Fournir l'ensemble des niveaux de matérialité possibles pour l'évaluation
            des informations adverses, ordonnés du plus grave au moins grave.

        Paramètres:
            Aucun

        Retourne:
            List[MaterialityLevel]: Liste de tous les niveaux de matérialité disponibles
            dans l'énumération MaterialityLevel.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> levels = matrix.get_all_materiality_levels()
            >>> for level in levels:
            ...     print(level.value)
            Highly Material
            Significantly Material
            Material
            ...
        """
        return list(MaterialityLevel)

    def get_rules_by_category(self, category: WrongdoingCategory) -> List[ClassificationRule]:
        """
        Obtient toutes les règles de classification pour une catégorie donnée.

        Objectif:
            Récupérer l'ensemble des règles de classification associées à une catégorie
            spécifique de mauvaise conduite. Utile pour afficher toutes les options
            de classification possibles pour une catégorie.

        Paramètres:
            category (WrongdoingCategory): Catégorie de mauvaise conduite dont on veut
                obtenir toutes les règles

        Retourne:
            List[ClassificationRule]: Liste de toutes les règles de classification
            pour cette catégorie. Retourne une liste vide si la catégorie n'existe pas.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> rules = matrix.get_rules_by_category(WrongdoingCategory.FRAUD)
            >>> for rule in rules:
            ...     print(f"{rule.action_type}: {rule.materiality_level.value}")
            Criminal Conviction: Highly Material
            Open criminal investigation: Significantly Material
            ...
        """
        return self.matrix.get(category, [])

    def get_mitigating_factors_by_dimension(self, dimension: str) -> List[str]:
        """
        Obtient les facteurs atténuants pour une dimension spécifique.

        Objectif:
            Récupérer la liste des facteurs atténuants pour une dimension d'évaluation
            particulière (ex: "Client Remediation", "Information Stage").

        Paramètres:
            dimension (str): Nom de la dimension d'évaluation. Les dimensions valides sont:
                - "Information Stage"
                - "Provenance"
                - "Underlying Breach"
                - "Client Remediation"
                - "Outcomes"
                - "Client Profile"
                - "Timescales"

        Retourne:
            List[str]: Liste des facteurs atténuants pour cette dimension.
            Retourne une liste vide si la dimension n'existe pas.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> factors = matrix.get_mitigating_factors_by_dimension("Client Remediation")
            >>> for factor in factors:
            ...     print(factor)
            Improvements to internal controls and/or compliance culture
            Implemented additional controls or enhancements to policies
            ...
        """
        return self.mitigating_factors.get(dimension, [])

    def get_aggravating_factors_by_dimension(self, dimension: str) -> List[str]:
        """
        Obtient les facteurs aggravants pour une dimension spécifique.

        Objectif:
            Récupérer la liste des facteurs aggravants pour une dimension d'évaluation
            particulière (ex: "Pattern", "Senior Involvement").

        Paramètres:
            dimension (str): Nom de la dimension d'évaluation. Les dimensions valides sont:
                - "Pattern"
                - "Senior Involvement"
                - "Outcomes"
                - "Client Profile"

        Retourne:
            List[str]: Liste des facteurs aggravants pour cette dimension.
            Retourne une liste vide si la dimension n'existe pas.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> factors = matrix.get_aggravating_factors_by_dimension("Pattern")
            >>> for factor in factors:
            ...     print(factor)
            Repeated and recurring breaches suggesting weak governance
            Poor internal control framework
            ...
        """
        return self.aggravating_factors.get(dimension, [])

    def get_outcome_by_id(self, outcome_id: str) -> Optional[Dict[str, str]]:
        """
        Obtient une issue possible par son identifiant.

        Objectif:
            Récupérer les détails d'une issue spécifique pour la relation client
            en utilisant son identifiant numérique.

        Paramètres:
            outcome_id (str): Identifiant de l'issue recherchée (de "1" à "7")

        Retourne:
            Optional[Dict[str, str]]: Dictionnaire contenant les informations de l'issue
            avec les clés "id", "outcome" et "description". Retourne None si l'identifiant
            n'existe pas.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> outcome = matrix.get_outcome_by_id("7")
            >>> if outcome:
            ...     print(f"{outcome['outcome']}: {outcome['description']}")
            Client exit: Termination of client relationship
        """
        for outcome in self.potential_outcomes:
            if outcome["id"] == outcome_id:
                return outcome
        return None

    def to_dict(self) -> Dict:
        """
        Convertit la matrice complète en dictionnaire pour export JSON.

        Objectif:
            Sérialiser l'ensemble de la matrice de classification (règles, facteurs
            atténuants/aggravants, issues possibles) dans un format dictionnaire
            facilement exportable en JSON ou utilisable pour l'entraînement d'un modèle.

        Paramètres:
            Aucun

        Retourne:
            Dict: Dictionnaire structuré contenant quatre sections principales:
                - "matrix": Toutes les règles de classification par catégorie
                - "mitigating_factors": Tous les facteurs atténuants par dimension
                - "aggravating_factors": Tous les facteurs aggravants par dimension
                - "potential_outcomes": Toutes les issues possibles

        Structure retournée:
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
                        },
                        ...
                    ],
                    ...
                },
                "mitigating_factors": {...},
                "aggravating_factors": {...},
                "potential_outcomes": [...]
            }

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> import json
            >>> matrix_dict = matrix.to_dict()
            >>> json_str = json.dumps(matrix_dict, indent=2)
            >>> # Sauvegarder dans un fichier
            >>> with open>>> with open('kyc_matrix.json', 'w') as f:
            ...     json.dump(matrix_dict, f, indent=2)
        """
        return {
            "matrix": {
                category.value: [
                    {
                        "action_type": rule.action_type,
                        "materiality_level": rule.materiality_level.value,
                        "description": rule.description,
                        "escalation": {
                            "second_line": rule.escalation.second_line,
                            "send_to_mlro": rule.escalation.send_to_mlro,
                            "cc_compliance": rule.escalation.cc_compliance,
                            "four_eyes": rule.escalation.four_eyes
                        }
                    }
                    for rule in rules
                ]
                for category, rules in self.matrix.items()
            },
            "mitigating_factors": self.mitigating_factors,
            "aggravating_factors": self.aggravating_factors,
            "potential_outcomes": self.potential_outcomes
        }

    def get_escalation_requirements(self, category: WrongdoingCategory) -> EscalationProcedure:
        """
        Obtient les exigences d'escalade pour une catégorie donnée.

        Objectif:
            Déterminer rapidement quelle procédure d'escalade s'applique à une catégorie
            de mauvaise conduite (MLRO + Compliance ou 4 eyes). Utile pour savoir
            immédiatement qui doit être notifié.

        Paramètres:
            category (WrongdoingCategory): Catégorie de mauvaise conduite dont on veut
                connaître la procédure d'escalade

        Retourne:
            EscalationProcedure: Procédure d'escalade applicable à cette catégorie.
            Toutes les règles d'une même catégorie partagent la même procédure d'escalade.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> escalation = matrix.get_escalation_requirements(WrongdoingCategory.AML_CFT)
            >>> print(f"Send to MLRO: {escalation.send_to_mlro}")
            >>> print(f"CC Compliance: {escalation.cc_compliance}")
            >>> print(f"Four eyes: {escalation.four_eyes}")
            Send to MLRO: True
            CC Compliance: True
            Four eyes: False
        """
        rules = self.matrix.get(category, [])
        if rules:
            return rules[0].escalation
        # Par défaut, retourne une escalade haute priorité
        return EscalationProcedure(
            second_line="KYI Group Mgr",
            send_to_mlro=True,
            cc_compliance=True,
            four_eyes=False
        )

    def is_high_priority_category(self, category: WrongdoingCategory) -> bool:
        """
        Vérifie si une catégorie est considérée comme haute priorité.

        Objectif:
            Déterminer rapidement si une catégorie nécessite une escalade immédiate
            vers le MLRO. Les catégories haute priorité incluent AML/CFT, fraude,
            corruption, sanctions, etc.

        Paramètres:
            category (WrongdoingCategory): Catégorie à vérifier

        Retourne:
            bool: True si la catégorie est haute priorité (escalade MLRO requise),
            False si elle utilise la procédure 4 eyes.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> matrix.is_high_priority_category(WrongdoingCategory.AML_CFT)
            True
            >>> matrix.is_high_priority_category(WrongdoingCategory.ADMINISTRATIVE_VIOLATIONS)
            False
        """
        escalation = self.get_escalation_requirements(category)
        return escalation.send_to_mlro

    def get_all_mitigating_dimensions(self) -> List[str]:
        """
        Obtient la liste de toutes les dimensions de facteurs atténuants.

        Objectif:
            Fournir la liste complète des dimensions disponibles pour les facteurs
            atténuants. Utile pour parcourir ou afficher toutes les dimensions possibles.

        Paramètres:
            Aucun

        Retourne:
            List[str]: Liste des noms de dimensions pour les facteurs atténuants.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> dimensions = matrix.get_all_mitigating_dimensions()
            >>> print(dimensions)
            ['Information Stage', 'Provenance', 'Underlying Breach', 'Client Remediation',
             'Outcomes', 'Client Profile', 'Timescales']
        """
        return list(self.mitigating_factors.keys())

    def get_all_aggravating_dimensions(self) -> List[str]:
        """
        Obtient la liste de toutes les dimensions de facteurs aggravants.

        Objectif:
            Fournir la liste complète des dimensions disponibles pour les facteurs
            aggravants. Utile pour parcourir ou afficher toutes les dimensions possibles.

        Paramètres:
            Aucun

        Retourne:
            List[str]: Liste des noms de dimensions pour les facteurs aggravants.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> dimensions = matrix.get_all_aggravating_dimensions()
            >>> print(dimensions)
            ['Pattern', 'Senior Involvement', 'Outcomes', 'Client Profile']
        """
        return list(self.aggravating_factors.keys())

    def search_rules_by_materiality(self, materiality_level: MaterialityLevel) -> Dict[WrongdoingCategory, List[ClassificationRule]]:
        """
        Recherche toutes les règles correspondant à un niveau de matérialité donné.

        Objectif:
            Trouver toutes les combinaisons catégorie/action qui correspondent à un
            niveau de matérialité spécifique. Utile pour identifier tous les scénarios
            qui nécessitent le même niveau d'attention.

        Paramètres:
            materiality_level (MaterialityLevel): Niveau de matérialité recherché
                (ex: MaterialityLevel.HIGHLY_MATERIAL)

        Retourne:
            Dict[WrongdoingCategory, List[ClassificationRule]]: Dictionnaire mappant
            chaque catégorie aux règles qui correspondent au niveau de matérialité recherché.

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> highly_material = matrix.search_rules_by_materiality(MaterialityLevel.HIGHLY_MATERIAL)
            >>> for category, rules in highly_material.items():
            ...     print(f"{category.value}: {len(rules)} règle(s)")
            AML/CFT Matters: 1 règle(s)
            Fraud: 1 règle(s)
            ...
        """
        results = {}
        for category, rules in self.matrix.items():
            matching_rules = [rule for rule in rules if rule.materiality_level == materiality_level]
            if matching_rules:
                results[category] = matching_rules
        return results

    def get_summary_statistics(self) -> Dict[str, any]:
        """
        Obtient des statistiques récapitulatives sur la matrice.

        Objectif:
            Fournir une vue d'ensemble quantitative de la matrice : nombre de catégories,
            de règles, de facteurs, etc. Utile pour la documentation et la validation.

        Paramètres:
            Aucun

        Retourne:
            Dict[str, any]: Dictionnaire contenant diverses statistiques:
                - total_categories: Nombre total de catégories
                - total_rules: Nombre total de règles de classification
                - high_priority_categories: Nombre de catégories haute priorité
                - four_eyes_categories: Nombre de catégories avec procédure 4 eyes
                - total_mitigating_factors: Nombre total de facteurs atténuants
                - total_aggravating_factors: Nombre total de facteurs aggravants
                - total_potential_outcomes: Nombre d'issues possibles
                - materiality_levels: Nombre de niveaux de matérialité

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> stats = matrix.get_summary_statistics()
            >>> print(f"Total de catégories: {stats['total_categories']}")
            >>> print(f"Total de règles: {stats['total_rules']}")
            Total de catégories: 14
            Total de règles: 154
        """
        total_rules = sum(len(rules) for rules in self.matrix.values())
        high_priority = sum(1 for cat in self.matrix.keys() if self.is_high_priority_category(cat))
        four_eyes = len(self.matrix) - high_priority

        total_mitigating = sum(len(factors) for factors in self.mitigating_factors.values())
        total_aggravating = sum(len(factors) for factors in self.aggravating_factors.values())

        return {
            "total_categories": len(self.matrix),
            "total_rules": total_rules,
            "high_priority_categories": high_priority,
            "four_eyes_categories": four_eyes,
            "total_mitigating_factors": total_mitigating,
            "total_aggravating_factors": total_aggravating,
            "total_potential_outcomes": len(self.potential_outcomes),
            "materiality_levels": len(MaterialityLevel),
            "mitigating_dimensions": len(self.mitigating_factors),
            "aggravating_dimensions": len(self.aggravating_factors)
        }

    def export_to_json(self, filepath: str) -> bool:
        """
        Exporte la matrice complète dans un fichier JSON.

        Objectif:
            Sauvegarder la matrice de classification dans un fichier JSON pour
            utilisation ultérieure, partage, ou entraînement de modèle.

        Paramètres:
            filepath (str): Chemin du fichier JSON à créer (ex: "kyc_matrix.json")

        Retourne:
            bool: True si l'export a réussi, False en cas d'erreur

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> success = matrix.export_to_json("data/kyc_matrix.json")
            >>> if success:
            ...     print("Export réussi!")
            Export réussi!
        """
        import json
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de l'export: {e}")
            return False

    def print_category_summary(self, category: WrongdoingCategory) -> None:
        """
        Affiche un résumé détaillé d'une catégorie de mauvaise conduite.

        Objectif:
            Fournir une vue d'ensemble lisible et formatée de toutes les informations
            relatives à une catégorie : règles, procédure d'escalade, notes.
            Utile pour la documentation et la formation.

        Paramètres:
            category (WrongdoingCategory): Catégorie à afficher

        Retourne:
            None (affiche directement dans la console)

        Exemple:
            >>> matrix = KYCClassificationMatrix()
            >>> matrix.print_category_summary(WrongdoingCategory.AML_CFT)

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
            ...
        """
        print(f"\n{'='*60}")
        print(f"Catégorie: {category.value}")
        print(f"{'='*60}\n")

        # Escalation
        escalation = self.get_escalation_requirements(category)
        print("Procédure d'escalade:")
        print(f"  - Seconde ligne: {escalation.second_line}")
        print(f"  - Envoyer au MLRO: {'Oui' if escalation.send_to_mlro else 'Non'}")
        print(f"  - CC Compliance: {'Oui' if escalation.cc_compliance else 'Non'}")
        print(f"  - Four eyes: {'Oui' if escalation.four_eyes else 'Non'}")

        # Règles
        rules = self.get_rules_by_category(category)
        print(f"\nRègles de classification ({len(rules)}):\n")
        for i, rule in enumerate(rules, 1):
            print(f"{i}. {rule.action_type}")
            print(f"   Niveau: {rule.materiality_level.value}")
            print(f"   Description: {rule.description}\n")


# Exemple d'utilisation complet
if __name__ == "__main__":
    """
    Script de démonstration des fonctionnalités de la matrice KYC.
    
    Ce script montre comment:
    1. Initialiser la matrice
    2. Récupérer des règles de classification
    3. Afficher des statistiques
    4. Exporter les données
    5. Rechercher des informations spécifiques
    """

    print("=" * 70)
    print("DÉMONSTRATION DE LA MATRICE DE CLASSIFICATION KYC")
    print("=" * 70)

    # 1. Créer la matrice
    print("\n1. Initialisation de la matrice...")
    matrix = KYCClassificationMatrix()
    print("✓ Matrice initialisée avec succès")

    # 2. Afficher les statistiques
    print("\n2. Statistiques de la matrice:")
    print("-" * 70)
    stats = matrix.get_summary_statistics()
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")

    # 3. Exemple de recherche de classification
    print("\n3. Exemple de classification:")
    print("-" * 70)
    rule = matrix.get_classification(
        WrongdoingCategory.AML_CFT,
        "Criminal Conviction"
    )
    if rule:
        print(f"   Catégorie: AML/CFT")
        print(f"   Type d'action: {rule.action_type}")
        print(f"   Niveau de matérialité: {rule.materiality_level.value}")
        print(f"   Envoyer au MLRO: {rule.escalation.send_to_mlro}")
        print(f"   CC Compliance: {rule.escalation.cc_compliance}")

    # 4. Afficher les catégories haute priorité
    print("\n4. Catégories haute priorité (escalade MLRO):")
    print("-" * 70)
    for category in matrix.get_all_categories():
        if matrix.is_high_priority_category(category):
            print(f"   ✓ {category.value}")

    # 5. Exemple de facteurs atténuants
    print("\n5. Facteurs atténuants - Client Remediation:")
    print("-" * 70)
    factors = matrix.get_mitigating_factors_by_dimension("Client Remediation")
    for factor in factors:
        print(f"   • {factor}")

    # 6. Recherche par niveau de matérialité
    print("\n6. Recherche des règles 'Highly Material':")
    print("-" * 70)
    highly_material = matrix.search_rules_by_materiality(MaterialityLevel.HIGHLY_MATERIAL)
    print(f"   Trouvé dans {len(highly_material)} catégorie(s)")
    for category, rules in list(highly_material.items())[:3]:  # Afficher 3 exemples
        print(f"   • {category.value}: {len(rules)} règle(s)")

    # 7. Export JSON
    print("\n7. Export de la matrice:")
    print("-" * 70)
    success = matrix.export_to_json("kyc_classification_matrix.json")
    if success:
        print("   ✓ Matrice exportée vers 'kyc_classification_matrix.json'")
    else:
        print("   ✗ Erreur lors de l'export")

    # 8. Afficher un résumé de catégorie
    print("\n8. Résumé détaillé d'une catégorie:")
    print("-" * 70)
    matrix.print_category_summary(WrongdoingCategory.FRAUD)

    print("\n" + "=" * 70)
    print("FIN DE LA DÉMONSTRATION")
    print("=" * 70)