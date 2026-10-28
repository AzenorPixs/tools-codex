# Changelog

## Unreleased

- Corriger le blocage PLLM sur une mémoire sans version : récupérer seulement
  la mémoire vide ou le seul mode7 DeepSeek Medium identifiable au protocole 8,
  sans réécriture au chargement. Garantir l'écriture atomique d'une mémoire
  au schéma 3 rechargeable ; préserver et refuser les données ambiguës ou
  corrompues. Isoler MEMORY_PATH dans le test Medium mode7 pour empêcher
  toute écriture dans les données source. Aligner la release et les six plugins sur 0.7.21.

- Réduire à 0,10 EUR/M inclus le plafond moyen OpenRouter payant dans TFL et
  PLLM mode5, y compris pour les anciens catalogues et rangs forcés ; vérifier
  le chemin de benchmark complet qui enregistre l'acceptation Medium et le débit,
  puis aligner la release locale et les six plugins sur 0.7.20.
- Conserver les sources d'enquête DeepSeek dans le diagnostic PLLM, refuser un
  alias Medium→High comme effort effectif et limiter les redirections de preuve
  HTTPS à la même origine. Qualifier la chaîne TFL→PLLM et aligner la release
  locale et les six plugins sur 0.7.19.
- Corriger le chemin de benchmark complet TFL/PLLM : importer `copy` pour
  enregistrer l'acceptation Medium et poursuivre la mesure du débit.
- Stabiliser les empreintes des preuves HTML sur leur texte visible normalisé,
  en conservant le hachage exact des octets pour les autres formats.
- Reconfigurer PLLM en sept priorités : mode5 paie OpenRouter sans benchmark ni Medium avec plafond 0,20 EUR/M et contexte 1M ; mode6 benchmarke les gratuits OpenRouter en Medium ; DeepSeek devient mode7. Conserver tous les payants OpenRouter admissibles dans TFL même sans preuve Medium et aligner la release locale sur 0.7.17.
- Corriger le filtrage PLLM qui rejetait les preuves Medium à cause d'anciens overrides/tentatives et OpenRouter à cause des arrondis binaires des prix ; conserver les décimales TFL de référence et aligner la release commune sur 0.7.16.
- Rendre effectif le contrat Medium dans les états PLLM anciens : invalider les requêtes et tentatives mesurées avec un autre effort même si la capacité du modèle inclut Medium, vider les résultats livrés devenus incompatibles et aligner les commandes, spécifications actives, documentation, distributions et release commune sur 0.7.15.
- Basculer TFL et PLLM vers Medium : exiger une preuve explicite, envoyer Medium sur chaque transport et arrêter les candidats sans repli High/XHigh. Conserver les anciennes mesures comme historique et aligner la release commune sur 0.7.14.
- Aligner VERSION, pyproject.toml, README et les six plugins sur 0.7.14.
- Déclarer les six commandes CM, PLLM, TFL, TCU, LM et PROMPT en majuscules dans leurs fichiers sources, déclencheurs et libellés ; compléter les métadonnées CM/PROMPT et conserver les identifiants techniques ainsi que les anciens alias.
- Adapter TCU aux nouveaux noms et aux copies historiques avec leurs reçus : créer seulement le nouveau wrapper PROMPT.md absent, actualiser les copies existantes sans doublon ni renommage, préserver liens, modifications locales et sauvegardes. Les liens personnels vers les anciens chemins sources nécessitent une réorientation explicite.
- Aligner VERSION, pyproject.toml, README et les six plugins sur 0.7.13. Cette correction des sources ne migre pas les profils installés et ne lance aucun benchmark fournisseur.

- Retirer entièrement OpenCode général du parcours TFL : disponibilité, tarifs, métadonnées, qualification gratuite et publication JSON/Markdown. Conserver les seuls catalogues Go et OpenRouter et leurs filtres.
- Limiter PLLM 1/2 aux payants Go et 3/4 aux gratuits Go, même avec un ancien catalogue, un résultat historique général ou un rang forcé. Le planning contrôle désormais les deux sections courantes, sans changer ses horaires ni ses autres gardes.
- Ajouter les familles inkling et inkling-small dans la liste LM utilisateur à la demande explicite du développeur ; préserver les autres entrées et les défauts distribués. L'exclusion couvre leurs variantes payantes/gratuites actuelles, sans joker fournisseur.
- Aligner les sources, distributions, métadonnées et six plugins sur 0.7.12. Qualification hors ligne ; les installations TFL/PLLM, les anciens rapports et le timer utilisateur ne sont pas actualisés par cette livraison locale.

- Corriger la lecture des niveaux reasoning_options de models.dev et accepter HIGH/XHIGH officiellement reconnus même sans intensité distincte. Livrer la preuve MiMo et son équivalence documentée vers thinking activé sur sa route Chat Completions, sans inventer d'endpoint ni qualifier ses performances.
- Imposer aux agents l'investigation des efforts et contextes inconnus pour Go, OpenCode général et OpenRouter ; conserver conclusions, sources, dates et empreintes, vérifier les sources courantes et exclure tout contexte encore invérifiable après investigation. Le CLI marque les recherches nécessaires et son rapport provisoire.
- Faire de LM l'unique liste noire et rendre muse-spark-1.2-contributor retirable ; préserver les listes existantes ou explicitement vides, sans migration implicite lors d'une lecture. Supprimer les anciennes métadonnées de listes permanentes du JSON TFL/PLLM.
- Aligner les skills, plugins, commandes, VERSION, pyproject.toml et les six manifestes sur 0.7.11. Qualification locale et documentaire, sans installation utilisateur, publication distante ni benchmark fournisseur.

- Publier les sélections TFL vides avant ou après qualification gratuite sans bloquer les autres catalogues, même si les trois sont vides : deux tableaux explicites, synthèses d'exclusions et états JSON disponibles, avec code zéro pour une collecte valide. Préserver les filtres et les échecs bloquants sur les erreurs réelles.
- Aligner la release locale et les six plugins sur 0.7.10 ; qualifier les deux distributions et les consommateurs PLLM hors ligne. Le planning reste inchangé et exige encore trois sélections non vides ; aucune installation utilisateur ni publication distante.

- Exiger une preuve publiée HIGH/XHIGH pour tout modèle gratuit ou payant TFL/PLLM ; exclure avant génération, sélection et affichage, y compris anciens catalogues, historiques, forçages et DeepSeek direct sans preuve. Garder les motifs dans les audits JSON ; un budget seul ne suffit plus.
- Retirer le tableau fournisseur général OpenCode de TFL tout en préservant sa collecte et sa section JSON pour PLLM 3/4. Afficher Go puis OpenRouter et les essais gratuits admissibles à l’effort.
- Appliquer à OpenRouter la moyenne de base ≤0,20 EUR/M après conversion non arrondie au dernier taux BCE publié ; afficher les prix en EUR, tracer taux/source/dates et prix USD, recontrôler dans PLLM et préserver les rapports si la conversion est invérifiable.
- Aligner la release locale, pyproject.toml, README et les six plugins sur 0.7.9 ; qualifier hors ligne sans installation de profil, activation du planning ou publication distante. Les métadonnées d’effort absentes peuvent vider un catalogue et bloquer sa nouvelle publication.

- Ajouter un planning systemd utilisateur TFL puis PLLM normal à 00 h et 12 h Europe/Paris, bootstrap idempotent des six plugins et de TCU, avec confiance native des hooks conservée et aucun rattrapage.
- Exiger Codex ouvert et un quota Codex frais non épuisé avant chaque étape ; ignorer les quotas nuls ou inconnus, arrêter après échec TFL et conserver les seuils, secrets et exclusions LM. Qualifier en profils isolés et aligner la release locale et les six plugins sur 0.7.8, sans activation utilisateur ni publication distante.

- Accepter les identifiants OpenRouter à préfixe `~` valide dans les six modules LM/TFL/PLLM, sans modifier leur identité canonique, les exclusions par défaut/personnalisées/permanentes ni les validations strictes.
- Qualifier les préfixes marqués, la persistance canonique et les gardes TFL/PLLM ; aligner VERSION, pyproject.toml, README et les six manifestes sur 0.7.7. La relance TFL depuis les sources corrigées est distincte de la mise à jour des sources installées dans le profil.

- Ajouter LM : plugin, skill autonome et embarqué, commande source /LM, LIST sans écriture, ADD/REMOVE atomiques et catalogue CM actualisé ; mimo-v2.5 exclu par défaut.
- Partager les exclusions via CODEX_HOME/lm/blacklist.json hors cache ; filtrer TFL/PLLM avant classement, sélection et tests, y compris catalogues anciens, rangs forcés et candidat direct. Préserver les exclusions permanentes et les données utilisateur ; une politique invalide bloque sans écrasement.
- Aligner VERSION, pyproject.toml, documentation et six manifestes sur 0.7.6. Qualification locale hors ligne ; aucune publication, installation utilisateur ni génération fournisseur réelle. Une ancienne release ignore la nouvelle politique LM.

- Après qualification du correctif de sélection PLLM, incrémenter la release commune de 0.7.4 à 0.7.5 dans VERSION, pyproject.toml, la documentation et les cinq manifestes ; aucune publication distante ni mise à jour de profil utilisateur.

- Arrêter chaque mode PLLM au premier candidat conforme aux tests actuels : payants 1/2/5 par coût moyen TFL croissant et ordre TFL à prix égal ; gratuits 3/4 dans l'ordre TFL Go puis général.
- Réserver le mode5 aux payants OpenRouter : un crédit épuisé le rend invalide sans repli gratuit. Préserver les seuils distincts, paliers, HIGH/XHIGH, contrôles, transports, mémoire, forçages de rang et publication ; active garde son arrêt à la première politique valide.
- Conserver dans le JSON les seuls candidats visités et leur stratégie de sélection. Cette qualification locale ne relance pas les fournisseurs et n'actualise pas les installations utilisateur.

- Classer les payants PLLM qualifiés par coût moyen TFL croissant ; utiliser le débit, le TTFT puis l'ordre TFL uniquement à prix égal. Conserver le classement des gratuits par performances et les priorités entre les six politiques.
- Conserver dans le JSON le coût vérifié et ses prix/provenances ; préserver les seuils, contrôles, forçages, mode active et protocole 8. Cette modification des sources ne met pas à jour les installations utilisateur ni la release distante.
- Incrémenter la release commune de 0.7.3 à 0.7.4 dans VERSION, pyproject.toml, la documentation et les cinq manifestes de plugins.

- Corriger les tokens/s PLLM/TFL face aux fragments reçus en rafale : comptage API sur la durée complète non arrondie de la requête, attente et TTFT inclus, sans soustraction du premier token ni écrêtage.
- Accepter une réponse complète reçue en un bloc avec mesures fiables ; tracer les durées et le profil request_average_v1/request_total, protocole 8 ; rendre les mesures invalides indisponibles sans réutiliser une ancienne valeur.
- Séparer la mémoire par profil de débit, préserver les succès historiques et les seuils numériques ; le nouveau débit moyen n'est pas directement comparable à l'ancien et peut modifier classement et éligibilité.
- Aligner les distributions, VERSION, pyproject.toml, README et cinq plugins sur 0.7.3. Qualification locale hors ligne, sans installation ni benchmark fournisseur réel.

- Harmoniser les gratuits PLLM/TFL : prix nuls vérifiés, contexte ≥1M, réponse complète, TTFT <30 s et débit >20 tokens/s, y compris le repli gratuit OpenRouter de PLLM 5.
- Tester en HIGH avec le seul repli XHIGH pris en charge ; appliquer ce défaut aux six modes PLLM et aux gratuits TFL, avec moteur streaming commun embarqué et mémoire séparée par raisonnement effectif.
- Exclure de TFL models les gratuits échoués ou non mesurables, conserver causes et tentatives dans les exclusions et ajouter le tableau de tous les essais gratuits ; aucun quota consulté par ces tests.
- Aligner les sources, la documentation, VERSION, pyproject.toml et les cinq plugins sur 0.7.2. Cette livraison locale n'actualise pas les installations et ne qualifie pas les performances fournisseur actuelles.

- Déclarer le nom d'affichage du skill PLLM en majuscules dans les distributions autonome et embarquée, sans changement de version ni d'identifiant technique.
- Séparer les gratuits Go et OpenCode général en modes PLLM 3/4, avec les comptes de 1/2, sans contrôle de quota ni solde : contexte ≥1M, réponse complète, TTFT <30 s et débit >20 tokens/s.
- Réserver 1/2 aux payants Go : un quota épuisé les rend rouges et invalides sans repli ; déplacer OpenRouter vers 5 et DeepSeek direct vers 6, avec leurs contrôles et seuils conservés.
- Adapter les historiques et mémoires au schéma 2 sans succès courant hérité, conserver les références des secrets et déplacer les forçages OpenRouter 31–33 vers 51–53 ; les nouveaux 31–33 et 41–43 ciblent les gratuits admissibles.
- Aligner les deux distributions, la documentation et les cinq manifestes sur 0.7.1. Le schéma 2 n'est pas lisible par l'ancien évaluateur ; conserver ses données avant retour de version. Cette livraison locale n'installe ni ne publie la release distante.


- Corriger le corps Chat Completions OpenCode Go/général : reasoning_effort=low sans thinking ; préserver les contrats Responses, Messages, DeepSeek direct et OpenRouter.
- Conserver des diagnostics HTTP bornés et filtrés, avec paramètre connu refusé et Retry-After numérique/date HTTP ; afficher l'échéance disponible sans corps brut ni contenu privé.
- Arrêter les paliers du candidat sur HTTP 400/429 et poursuivre les autres candidats autorisés ; préserver les reprises après troncature, quotas, classement, mémoire, forçages et silence de active.
- Qualifier les deux distributions et aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.6.1 ; aucune installation de profil ou publication distante n'est réalisée par cette livraison locale.

- Comparer les payants PLLM quand les ressources sont disponibles ; après épuisement confirmé, limiter les modes 1/2 aux gratuits TFL Go et OpenCode général, et le mode 3 aux gratuits OpenRouter. Revenir aux payants au rétablissement des ressources.
- Retenir le débit maximal puis le TTFT minimal parmi toutes les réussites d'un mode, avec ordre TFL pour dernier départage ; préserver priorités, Low, seuils stricts, forçages et silence de active.
- Afficher authentification refusée, accès refusé et repli gratuit dans État ; conserver quotas réels, candidats et tentatives dans le JSON, avec mémoire par configuration et sans secret dans les erreurs.
- Aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.6.0 ; synchroniser les deux distributions PLLM. Cette livraison locale n'installe pas les sources dans les profils utilisateur et ne qualifie pas les accès fournisseurs réels.

- Ajouter le catalogue général OpenCode à TFL par collecte publique indépendante de Go, avec tarifs Console et métadonnées `opencode` ; conserver contexte ≥ 1M, coût moyen maximal 0,50 USD/M, modalités, blacklist et exclusions motivées, y compris variantes gratuites 200K.
- Restituer Go, OpenCode général puis OpenRouter avec trois tableaux aux colonnes identiques ; ajouter la section JSON `opencode` sans changer les sections ni politiques PLLM existantes, et préserver les rapports si une collecte indispensable échoue.
- Aligner la release commune, pyproject.toml, README et les cinq plugins sur 0.5.6 ; synchroniser distributions, wrapper et descriptions CM/TFL, sans installation de profil ni publication distante.

- Collecter les modalités et le routage OpenCode Go depuis les déclarations API et models.dev, sans listes statiques de modèles ; conserver sources, dates, surcharges SDK/base API et informations inconnues explicites.
- Vérifier les contradictions de modalités, les contrats de transport génériques et les URL HTTPS d'origine OpenCode avant publication ; distinguer route documentée et génération testée, avec compatibilité des consommateurs PLLM inchangés.
- Qualifier les deux distributions TFL et aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.5, sans installation de profil, génération ni consultation des quotas.

- Sélectionner dynamiquement tous les modèles OpenRouter admissibles du catalogue API, sans liste d'identifiants, catégorie ni limite artificielle de nombre ; appliquer contexte ≥ 1M, moyenne de base ≤ 0,50 USD/M, modalités et blacklist, modèles gratuits vérifiés inclus.
- Supprimer l'échec lié à la disparition d'un ancien identifiant ; conserver les exclusions auditables, le tri, la provenance tarifaire, les variantes conditionnées par jours/horaires UTC et la préservation des rapports si aucun modèle n'est admissible.
- Qualifier cette sélection dans les deux distributions TFL et aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.3, sans modifier la précédente archive ni les installations utilisateur.

- Actualiser les tarifs OpenCode Go depuis sa documentation officielle à chaque exécution TFL, sans table statique ni repli historique ; vérifier unité, correspondances et doublons, ignorer les prix barrés et conserver les variantes dans le JSON.
- Tracer source et date tarifaires des deux fournisseurs ; conserver les prix de cache et les paliers OpenRouter sans changer son classement de base. Signaler les prix absents, préserver les rapports si la collecte échoue et laisser N/A les estimations Go non collectées.
- Qualifier les deux distributions TFL hors ligne et par une collecte réelle ; aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.2. Les installations utilisateur ne sont pas modifiées par cette livraison locale.

- Uniformiser la première colonne de CM avec des références aux skills et leurs noms lisibles, dont TCU ; conserver les syntaxes dans Utilisation et déclarer le nom d'affichage TCU dans les deux distributions.
- Aligner les cinq plugins, VERSION et la métadonnée Python sur 0.4.2.

- Gérer prompt comme composant TCU : installation ciblée du plugin absent, vérification du skill embarqué et déploiement du wrapper avec provenance dédiée ; conserver les autres briques absentes.
- Laisser les opérations indépendantes continuer malgré un conflit local, préserver les liens et rapporter les succès partiels avec un code non nul.
- Ajouter le wrapper `/cm` et son déclencheur dans le skill, en conservant une seule entrée prompt ; aligner les cinq plugins et la release commune sur 0.4.1.

- Ajouter le plugin et le skill prompt, leur résolveur et la commande source `/prompt`, avec référentiel exclusif DEVOPS.md du projet courant et LIST issu de son index.
- Ajouter les 38 actions en MAJUSCULE, les alias GCM/GCMP et les variantes 1CISMP1 à 1CISMP8 : un change complet, archivage, statistiques puis arrêt de la session de codage.
- Ajouter prompt au catalogue CM et aligner les cinq plugins, VERSION et la métadonnée Python sur 0.4.0.

- Accepter `/tcu check` et `$tcu check` sans tirets pour le contrôle sans écriture ; conserver `--check` compatible et refuser `check --apply` avant toute opération.

- Ajouter TCU (nom final de TFU), son plugin, son skill autonome et embarqué, son script et la commande source `/TCU` ; `$tcu` met à jour les briques présentes depuis marketplace et GitHub.
- Ajouter le contrôle `--check`, les sauvegardes, la provenance, l’adoption explicite et la gestion des conflits ; préserver les données générées et distinguer les succès partiels.
- Ajouter TCU au catalogue CM et aligner les quatre plugins, VERSION et la métadonnée Python sur 0.3.0.

- Ajouter le plugin `cm` à la marketplace Tools Codex en conservant le skill autonome et son lien local ; synchroniser les deux copies du catalogue.
- Documenter l'installation et la mise à jour du plugin CM ainsi que le risque de double entrée avec une copie autonome ; distinguer les contrôles locaux d'une installation réelle.
- Aligner la release commune, la métadonnée Python et les trois manifestes CM/PLLM/TFL sur 0.2.3.

- Remplacer `/cm` par le skill `$cm`, avec un catalogue français des invocations `$cm`, `$pllm` et `$tfl`, sans lancer les générateurs. Supprimer l'ancienne commande source.
- Exposer `skills/cm/` dans le projet par le lien relatif `.agents/skills/cm` et documenter l'installation autonome ; le contrôle local ne prouve pas une invocation dans une nouvelle session Codex.
- Aligner la release Tools Codex, les manifestes PLLM/TFL et la métadonnée Python sur 0.2.2.

- Déclarer le support Python 3.13/3.14 (`>=3.13,<3.15`) et aligner la métadonnée Python sur la release 0.2.1 de VERSION, sans packaging ou publication Python supplémentaire.

- Ajouter `--tfl-catalog CHEMIN` à PLLM en conservant le chemin voisin par défaut, et initialiser les quatre politiques lorsqu'aucun fichier courant n'existe ; préserver les fichiers corrompus.
- Recalculer les paliers après repli HTTP 429 et exiger les mesures du remplaçant avant toute sélection valide.
- Exclure les prix OpenRouter non finis et les débordements ; empêcher la publication d'un catalogue TFL non conforme au JSON strict.
- Qualifier ces comportements hors ligne dans les deux distributions ; l'installation réelle et les accès fournisseurs restent non vérifiés.

## 0.2.1 — 2026-10-10

- Porter le seuil strict de TTFT PLLM de 60 à 90 secondes, avec couleur et critères publiés cohérents.
- Aligner la release du projet et les manifestes PLLM/TFL sur 0.2.1.
