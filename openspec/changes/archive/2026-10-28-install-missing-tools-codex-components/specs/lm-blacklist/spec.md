## MODIFIED Requirements

### Requirement: Autonomie des paquets et conservation des données
LM, TFL et PLLM SHALL embarquer le même module de liste noire dans leurs
paquets autonomes et plugins. Un paquet isolé SHALL appliquer la liste sans
installation d'un plugin voisin. TCU SHALL conserver le stockage utilisateur
hors cache et SHALL actualiser LM présent ou installer LM absent selon les
règles TCU, sans créer ni remplacer les exclusions personnalisées. La livraison locale SHALL rester distincte de la
publication et de l'installation dans un profil réel.

#### Scenario: Plugins séparés
- **WHEN** TFL et PLLM sont placés dans deux caches de versions distincts
- **THEN** ils appliquent la même liste CODEX_HOME et ne dépendent pas du chemin du plugin LM

#### Scenario: Mise à jour LM
- **WHEN** TCU actualise une copie LM déjà présente
- **THEN** ses sources sont actualisées et les exclusions personnalisées restent intactes

#### Scenario: Installation LM absente
- **WHEN** TCU installe les sources LM absentes dans un profil ayant déjà des exclusions personnalisées
- **THEN** le plugin et les copies autonomes demandées sont installés sans modifier le stockage de la liste noire

