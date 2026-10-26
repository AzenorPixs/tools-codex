# Conception et unités

## Contrat de session
Un timer systemd --user déclenche à 00:00 et 12:00 Europe/Paris, avec
Persistent=false. Le runner ne lance pas Codex et ne rattrape pas une échéance
manquée. Il reconnaît l'application de bureau ou un CLI interactif vivant du
même UID ; un app-server, un codex exec ou un autre utilisateur ne suffit pas.
Les noms de session, transcriptions et secrets privés ne sont pas consultés.

## Installation
Chaque plugin embarque hooks/hooks.json et un module identique sous le skill.
SessionStart appelle le bootstrap après la confiance native de l'utilisateur.
TCU --apply utilise son module local déjà chargé, pas du code téléchargé, pour
installer ou actualiser le planning après les vérifications de sources. Check
décrit l'opération sans écrire, interroger les quotas ni exécuter un LLM.
Les installations autonomes disposent du même installateur, documenté dans
BUILD. La présence de TFL et PLLM est nécessaire ; aucune brique absente n'est
installée implicitement. Un checkout de développement n'est pas un paquet.

CODEX_HOME/llm-refresh contient runner, configuration, reçu et état filtré ;
XDG_CONFIG_HOME/systemd/user, ou ~/.config/systemd/user, contient uniquement
tools-codex-llm-refresh.service et .timer. Le reçu suit les empreintes des
fichiers gérés. Une source ou unité étrangère/divergente n'est pas écrasée.
Le retrait explicite ne touche que les fichiers reconnus et conserve les
rapports. Un rééquipement identique ne crée ni doublon ni réécriture inutile.
Échecs d'installation : état explicite, sauvegarde/restauration bornée des
fichiers gérés ; aucune promesse de transaction globale systemd/TCU.

## Exécution et quota
La sélection du paquet repose sur les racines autonomes enregistrées ou sur
codex plugin list --marketplace tools-codex --json, activation et version
réelles. Les chemins restent réguliers, appartenant à l'utilisateur et hors
checkout. Le runner verrouille la séquence et évite une application TCU
concurrente ; le verrou est non bloquant.

Un client JSONL dédié appelle initialize puis account/rateLimits/read sur
codex app-server --stdio. Il ne lance aucune conversation ni génération
Codex, n'ouvre pas auth.json et ne manipule aucune connexion ou crédit.
Le bucket codex de rateLimitsByLimitId prime sur la vue historique rateLimits ;
Spark ne remplace jamais Codex. Chaque fenêtre publiée doit être exploitable.
Une fenêtre épuisée bloque ; sans information vérifiable, ignorer avec cause.
Relire le quota avant PLLM : un épuisement partagé pendant TFL empêche PLLM.

Après succès TFL, vérifier la publication fraîche puis transmettre ce chemin
avec --tfl-catalog à PLLM normal, sans active. Les sorties restent dans les
rapports usuels. Les sous-processus sont bornés, leurs sorties brutes ne sont
pas journalisées ; l'état ne conserve que causes fixes, dates et codes retour.
Un refus/échec TFL arrête la séquence sans réutiliser un ancien catalogue.
Les seuils, modes, secrets fournisseur et blacklist LM restent inchangés.

## Sources vérifiées
- https://developers.openai.com/plugins/build/plugins : hooks de compatibilité,
  PLUGIN_ROOT, découverte et nécessité de confiance native.
- https://learn.chatgpt.com/docs/hooks : SessionStart, commande et timeout.
- https://learn.chatgpt.com/docs/app-server : initialize et account/rateLimits/read,
  fenêtres et bucket codex. La version CLI locale expose app-server --stdio.

## Unités testables
1. Spécifier et valider strictement avant code/tests.
2. Runner et tests : activité, quota, JSONL borné, ordre, fraîcheur, verrous,
   chemins, profils et préservation des données ; réseau simulé.
3. Installation, hooks et TCU : idempotence, conflits/repli, check sans effet,
   paquets copiés isolément, validation du calendrier systemd ; aucun timer réel.
4. Release 0.7.8 et documentation, parité des douze modules et six hooks,
   syntaxe, Python 3.13/3.14, skills, OpenSpec et matrice documentaire finale.
5. Synchroniser et archiver le seul change éligible, puis vérifier les six
   sections et les totaux de STATISTIQUES.md. Installation native réelle,
   confiance des hooks et exécution à une échéance restent des preuves distinctes.
