# Preuves des modèles et liste noire LM unique

## Why

TFL ignore les niveaux publiés dans reasoning_options de models.dev et exclut
ainsi des modèles dont HIGH/XHIGH est documenté. Les métadonnées de contexte
ou d'effort absentes ne déclenchent pas encore une investigation du LLM.
Les exclusions permanentes intégrées contredisent la gestion exclusive par LM.

## What Changes

- Normaliser les efforts publiés et accepter les équivalences documentées,
  notamment HIGH/XHIGH vers thinking activé pour MiMo, sans inventer de route.
- Rendre obligatoire l'investigation du LLM dans les sources officielles pour
  un contexte ou un effort invérifiable ; tracer ses preuves et sa conclusion.
- Exclure le modèle si son contexte reste invérifiable après investigation.
- Appliquer ces règles à Go, OpenCode général et OpenRouter ; conserver les
  seuils, comptes, quotas, transports et critères de performance existants.
- Faire de LM l'unique liste noire, avec retraits effectifs des anciennes
  exclusions permanentes, sans modifier les listes utilisateur en lecture.
- Synchroniser skills, plugins et commandes et aligner la release à 0.7.11.

## Impact

Spécifications : tfl-catalog, pllm-evaluation, lm-blacklist. Moteurs communs,
générateur TFL, consommateur PLLM, module LM, instructions et documentation.
Les preuves supplémentaires sont liées à un fournisseur, un ID et un protocole
exacts, vérifiées sur leur source courante et auditables dans le JSON.
Aucune installation de profil, publication distante ni opération Git.

## Autorisation

Périmètre autonome SCM proposé puis explicitement validé par le développeur
le 26 octobre 2026 : spécifier, implémenter, tester, versionner les métadonnées
locales, synchroniser, archiver et produire les statistiques de cette archive.
