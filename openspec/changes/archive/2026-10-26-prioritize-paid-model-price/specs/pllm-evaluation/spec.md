## REMOVED Requirements

### Requirement: Classement interne par performances
**Reason** : Le développeur exige que le prix établisse le classement des
payants ayant réussi les tests ; les performances seules ne doivent plus
choisir un payant plus cher.
**Migration** : Remplacer cette règle par le classement propre à la catégorie
ci-dessous, sans migration destructive de données ni modification des seuils.

## ADDED Requirements

### Requirement: Classement interne par prix des payants et performances des gratuits
Hors forçage, PLLM SHALL tester tous les candidats admissibles de la catégorie.
Les tests SHALL déterminer l'admissibilité. Les réussites payantes de 1/2 et 5
SHALL être classées par coût moyen TFL croissant, débit décroissant, TTFT
croissant puis ordre stable TFL. Le premier SHALL représenter le mode. Un
débit supérieur SHALL NOT faire devancer un payant moins cher valide.

#### Scenario: Payant moins cher et moins rapide
- **WHEN** deux payants valides coûtent 0,15 et 0,21 USD/M avec respectivement 113 et 200 tokens/s
- **THEN** le payant à 0,15 USD/M représente le mode malgré son débit inférieur

#### Scenario: Payant moins cher invalide
- **WHEN** le payant le moins cher échoue à un contrôle ou seuil obligatoire
- **THEN** il reste exclu du classement des réussites et le moins cher valide peut être retenu

#### Scenario: Prix égaux
- **WHEN** deux payants valides ont le même coût moyen vérifié
- **THEN** le débit décroissant puis le TTFT croissant et l'ordre stable les départagent

### Requirement: Coût vérifié de classement PLLM
Le coût SHALL être la moyenne des prix d'entrée/sortie TFL : hors pointe pour
Go et prix de base pour OpenRouter. Les égalités tarifaires SHALL résister aux
erreurs d'addition binaire. Les prix non vérifiables SHALL rester exclus.
Le JSON SHALL tracer les prix et leur provenance sans hériter de prix périmés.
Mode6 SHALL garder son candidat direct unique sans tarif inventé.

#### Scenario: Moyennes égales calculées différemment
- **WHEN** les prix 0,1/0,2 et 0,15/0,15 sont publiés pour deux candidats
- **THEN** leurs coûts moyens sont égaux à 0,15 et les performances peuvent les départager

#### Scenario: Prix absent ou invalide
- **WHEN** le catalogue ne fournit pas un prix vérifiable pour un candidat payant
- **THEN** le candidat est exclu avec sa cause, sans prix ni classement inventés

### Requirement: Classement des gratuits par performances
Les réussites gratuites de 3/4 et du repli de 5 SHALL être classées par débit
décroissant, TTFT croissant puis ordre stable TFL, Go avant général en 3/4.
Le premier SHALL représenter le mode ; aucun prix artificiel SHALL être utilisé.

#### Scenario: Gratuit plus performant
- **WHEN** deux gratuits valides ont des débits distincts en 3/4 ou dans le repli gratuit de 5
- **THEN** celui au débit maximal est retenu et aucun prix artificiel ne les départage

### Requirement: Invariants du classement tarifaire
Les priorités 1 à 6, seuils, quotas, raisonnement, forçages et protocole 8
SHALL rester inchangés. Le JSON SHALL tracer candidats et tentatives ; active
SHALL terminer le classement du premier mode valide avant de s'arrêter.
Le rapport SHALL conserver ses huit colonnes.

#### Scenario: Publication et priorités préservées
- **WHEN** plusieurs politiques valides ont été classées avec leurs règles propres
- **THEN** la première par priorité 1 à 6 est sélectionnée, avec huit colonnes inchangées
- **AND** son prix courant et les preuves des candidats restent auditables dans le JSON
