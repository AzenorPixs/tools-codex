# Validation — 28 octobre 2026

## Résultat

Release locale 0.7.23. Le catalogue du plugin utilisé à 11:28 datait du 14 septembre. La collecte autonome du 28 octobre à 11:06:15 retient beam-free et deux gratuits OpenRouter. Le chemin explicite reste prioritaire ; le défaut voisin reste inchangé. Le correctif trace provenance, âge, dates non vérifiables et compteurs, sans inventer de péremption ni relancer TFL.

Le HTTP 401 de mode2 est localisé au contrôle des quotas. Les champs de provenance et de ressources sont remis à zéro pour chaque politique visitée. Le contrôle de ressources garde uniquement endpoint public, phase et diagnostic HTTP filtré. Les résultats et mémoires PLLM sont exclus de Git avec conservation locale.

## Contrôles hors ligne

- OpenSpec strict avant réalisation et avant clôture : change valide, puis 11 éléments sur 11 valides.
- Tests ciblés PLLM : 90 réussis, dont cinq nouveaux tests distincts exécutés sur les deux distributions.
- Suite globale finale : 352 tests réussis sous Python 3.13.5 et 352 sous Python 3.14.10 (704 exécutions, 352 tests distincts).
- Le premier passage global a échoué sur deux attentes de release encore à 0.7.22 ; elles ont été alignées sur 0.7.23 avant les deux passages finaux.
- Cinq fichiers Python modifiés compilés sous chacune des deux branches, avec cfile temporaire et nettoyage, sans artefact source.
- Deux paires evaluate.py / SKILL.md comparées octet pour octet ; VERSION, project.version et les six manifestes vérifiés à 0.7.23.
- Les huit colonnes sont conservées. Les tests couvrent chemin explicite contre voisin ancien, date absente/invalide/sans fuseau/future, sélection gratuite vide, HTTP 401 du quota mode2 avec mode4 indépendant et absence de traces historiques reprises.

## Contrôles réels bornés

Quatre lectures de diagnostic authentifiées ont été exécutées avec injection du secret en mémoire, sans affichage de compte ni de clé. Les routes publiques https://opencode.ai/zen/go/v1/usage et /models répondent 200 pour mode1 et 401 pour mode2. Aucune clé n'a été modifiée, copiée dans un fichier ou empruntée à un autre mode.

Commande d'évaluation : `python3 -B skills/pllm/scripts/evaluate.py --tfl-catalog /home/devops/datas/tools-codex/skills/tfl/data/tfl.json`. Catalogue daté du 28 octobre à 11:06:15 Europe/Paris. Évaluation réelle de 11:40 à 11:41, résultats locaux publiés dans skills/pllm/data et exclus de Git.

| Mode | Résultat | Mesures courantes et limite |
|---|---|---|
| 1 | Valide, muse-spark-1.3-contributor | TTFT 8,1 s ; 105,0 tokens/s ; palier 2048 |
| 2 | Invalide | HTTP 401 au quota ; aucune génération |
| 3 | Valide, beam-free | TTFT 3,1 s ; 306,5 tokens/s ; palier 4096 |
| 4 | Invalide, beam-free | HTTP 401 à la génération ; aucun quota consulté |
| 5 | Valide, scaledown/extract | Contrôles prix/contexte/solde ; aucune génération par contrat |
| 6 | Valide, nvidia/nemotron-3-ultra-550b-a55b:free | TTFT 0,9 s ; 35,4 tokens/s ; palier 2048 |
| 7 | Valide, deepseek-v4-flash | TTFT 2,4 s ; 69,3 tokens/s ; palier 1024 |

Les tentatives de génération tracées sont 2 + 0 + 3 + 1 + 0 + 2 + 1 = 9. Les gratuits 3/4/6 ont quotas=null, quota_status=not_applicable et aucun resource_control. Le refus mode4 est propre à sa requête de génération, indépendamment du refus mode2. Les mesures sont datées, pas une garantie future ; les portées de débit Go et OpenRouter/DeepSeek restent distinctes.

La remédiation de sélection rétablit les modes3/6. Le refus fournisseur des modes2/4 reste à résoudre sur l'accès du compte associé ; ni sa cause privée ni la validité d'une autre clé n'ont été supposées. Ce refus externe attendu ne bloque pas la qualification du diagnostic livré. Aucun profil installé, timer ou agent OpenCode n'a été modifié. Aucun nouveau TFL n'a été lancé.

## Cohérence documentaire

| Document | État et preuve |
|---|---|
| AGENTS.md | Inchangé : contraintes de secrets, OpenSpec, version et tests préservées. |
| PROJECT.md | Inchangé : architecture des extensions et séparation des installations préservées. |
| TECHNICAL.md | Données générées : champs de diagnostic et exclusion Git documentés. |
| BUILD.md | Installation : divergence des copies TFL et refus d'accès documentés. |
| DEVOPS.md | Inchangé : chemins Python et OpenSpec utilisés, aucune nouvelle dépendance. |
| README.md | Release 0.7.23, sélection du catalogue et indépendance mode4 documentées. |
| CHANGELOG.md | Entrée Unreleased pour provenance, contrôle et exclusion des résultats. |
| OpenSpec | Trois exigences additives pllm-evaluation, change validé avant le code. |
| Distributions et commande | Deux evaluate.py et SKILL.md identiques ; commande PLLM alignée. |

Les étapes natives d'archivage, rapport statistique et Git conditionnel sont vérifiées séparément après cette validation. La qualification des sources ne prouve pas une installation en profil ni une publication distante.
