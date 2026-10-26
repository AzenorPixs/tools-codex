#!/usr/bin/env python3
"""Afficher ou modifier la liste noire partagée des modèles LLM."""

import argparse
import sys

from model_blacklist import BlacklistError, load_models, policy_path, update_models


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', nargs='?', default='LIST', choices=('LIST', 'ADD', 'REMOVE'))
    parser.add_argument('model', nargs='?')
    args = parser.parse_args(argv)
    if (args.action == 'LIST') != (args.model is None):
        parser.error('LIST ne prend pas de modèle ; ADD et REMOVE exigent un identifiant')
    try:
        models = load_models() if args.action == 'LIST' else update_models(args.action, args.model)
    except BlacklistError as error:
        print(str(error), file=sys.stderr)
        return 1
    print('# LM — Liste noire des modèles LLM\n')
    print('| Modèle exclu |\n|---|')
    for model in models:
        print('| ' + model + ' |')
    if not models:
        print('Aucun modèle dans la liste personnalisable.')
    print('\nStockage commun : ' + str(policy_path()))
    if args.action != 'LIST':
        print('Liste enregistrée ; TFL et PLLM l’appliqueront à leur prochaine invocation.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
