## MODIFIED Requirements

### Requirement: Invocation explicite et contrôle préalable
TCU SHALL fournir un skill autonome et embarqué invocable avec `$tcu` et
reconnaissant `/TCU`, plus une commande source de même rôle. Le script SHALL
vérifier sans mutation par défaut ; `--apply` SHALL appliquer ; `check` et `--check`
SHALL rester sans écriture. La combinaison `check --apply` SHALL être refusée
avant tout appel du moteur. Le skill SHALL lancer l'application pour une
demande explicite de mise à jour et SHALL NOT muter pour une explication.

#### Scenario: Contrôle seul
- **WHEN** TCU est lancé avec check ou --check
- **THEN** les sources distantes et versions peuvent être lues sans rafraîchir la marketplace ni écrire dans le profil
- **AND** les briques absentes sont signalées sans installation

#### Scenario: Modes contradictoires
- **WHEN** check et --apply sont fournis ensemble
- **THEN** le parseur refuse avant tout appel réseau, CLI ou écriture

