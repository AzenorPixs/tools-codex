# Conception

## Unités et preuves

1. Efforts : conserver les contrats existants et lire l'entrée effort/values
   de reasoning_options. Rejeter budgets, interrupteurs seuls, valeurs null
   ambiguës et déclarations contradictoires. Tester les quatre moteurs.
2. Investigation : registre JSON de conclusions du LLM, sources officielles
   HTTPS, date et empreinte SHA-256. Aucun emprunt entre fournisseurs ou routes.
   Le registre livré documente MiMo ; un registre data/model-evidence.json
   peut compléter les recherches d'une invocation. Les sources sont relues,
   une modification ou indisponibilité exige une nouvelle investigation.
   Les exclusions inconnues déclenchent un diagnostic investigation_required ;
   l'agent applique le workflow de recherche avant sa restitution finale.
   Une conclusion d'absence de preuve reste une absence de preuve, jamais une
   déclaration d'incapacité physique. Une investigation complète sans contexte
   vérifiable exclut le modèle. Un champ vérifié ne déduit jamais l'autre.
3. Équivalences : l'acceptation officielle de HIGH/XHIGH suffit même sans
   intensité distincte. Un mapping documenté peut représenter HIGH par
   thinking.type=enabled sur Chat Completions ; protocole, paramètres et sens
   sont tracés. Il ne change ni URL, ni fournisseur, ni route publiée.
4. LM : supprimer les listes permanentes ; les valeurs initiales LM sont
   mimo-v2.5 et muse-spark-1.2-contributor, toutes deux retirables. Une politique
   existante ou explicitement vide reste souveraine. La migration utilisateur
   demandée a déjà ajouté muse par LM ADD ; les lectures ne migrent rien.
5. Distribution : synchronisation exacte des copies autonomes/embarquées,
   instructions de recherche dans skills/commandes, cadrages, README,
   CHANGELOG et release 0.7.11 dans VERSION, pyproject et les six manifestes.

## Validation et limites

Tests ciblés après chaque unité, puis suite globale Python 3.13/3.14,
compilation, validation des skills, parité, UTF-8/LF et OpenSpec strict.
Qualification des preuves sur documents officiels, sans benchmark fournisseur
ni installation utilisateur. Les rapports historiques restent inchangés.
Retour : restaurer les sources antérieures et conserver les données LM ;
une ancienne release peut réappliquer son exclusion permanente interne.

## Matrice documentaire

AGENTS et DEVOPS : inchangés, règles et environnement préservés. PROJECT,
TECHNICAL, BUILD, README et CHANGELOG : mises à jour dans ce périmètre.
OpenSpec : trois capacités synchronisées avant archivage du seul change ciblé.
