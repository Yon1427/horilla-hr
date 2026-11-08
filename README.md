# Sanad — SIRH Algérie

**SIRH pour le secteur privé algérien** (loi 90-11) : dossier du personnel,
contrats, congés, temps, paie et coût employeur. Interface bilingue
français / arabe, montants en dinars.

Ce dépôt est une adaptation algérienne d'Horilla HRMS (LGPL-2.1). Il n'est plus
synchronisé avec le dépôt amont : les correctifs et évolutions sont gérés ici.

## Périmètre

- Secteur **privé uniquement** ; les statuts de la fonction publique sont hors
  périmètre.
- Paie : SNMG, CNAS (9 % salarié / 25 % employeur + 0,5 % FNPOS), IRG
  progressif (0/23/27/30/33/35 %), abattement 40 %, TFPC/TAPP, CASNOS.
- Les paramètres légaux sont des **données datées** (`AlgeriaPayrollParameter`,
  `effective_from`, `source_url`), jamais des constantes dans le code.
- Les chiffres non vérifiés restent des paramètres sans valeur par défaut et
  sont suivis dans `algeria-sirh/05-product-spec.md` §12.

## Démarrage rapide

### Docker (recommandé)

```bash
cp .env.dist .env          # puis renseigner les secrets
make dev                   # web + db + redis, code monté en volume
# http://localhost:8000/health/
```

Production :

```bash
make prod                  # docker-compose.prod.yml, nécessite .env
```

### Sans Docker

```bash
python -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.dist .env          # éditer la configuration
python manage.py migrate
python manage.py runserver
```

Le planificateur de tâches (`python manage.py run_scheduler`) tourne dans un
service séparé et **ne doit pas être répliqué** : les traitements de paie et de
sauvegarde ne sont pas idempotents.

## Configuration

Les variables de `.env.dist` couvrent le déploiement. L'identité produit est
surchargeable sans toucher au code :

```dotenv
SIRH_BRAND_NAME=Sanad
SIRH_BRAND_NAME_AR=سند
SIRH_BRAND_TAGLINE=SIRH Algérie
SIRH_SUPPORT_EMAIL=support@example.dz
SIRH_TERMS_URL=
```

La source unique est `horilla/settings/base.py` ; les modèles lisent
`brand_name` / `brand_name_ar` via `base.context_processors.sirh_brand`.

## Tests

```bash
make test-smoke            # suite fumée des applications first-party
make test-cov              # suite fumée sous couverture
make test-unit UNIT_LABELS="payroll base leave"
```

Contrôles avant livraison :

```bash
python manage.py makemigrations --check --dry-run
python manage.py test payroll --keepdb
```

Les cas de référence (bulletin 80 000 DA, bornes IRG) vivent dans
`payroll/tests/`.

## Documentation

| Fichier | Contenu |
|---|---|
| `algeria-sirh/00-index.md` | Index et chiffres clés 2026 |
| `algeria-sirh/01-payroll-costisation.md` | Paie, CNAS, IRG, CASNOS, coût employeur |
| `algeria-sirh/02-legal-declarations.md` | Contrats, temps de travail, déclarations |
| `algeria-sirh/05-product-spec.md` | Spécification produit et registre des conflits (§12) |
| `algeria-sirh/06-gap-analysis.md` | Écarts avec la base Horilla (défauts B1-B8) |
| `algeria-sirh/08-implementation-plan.md` | Plan d'implémentation M0/M1 |
| `algeria-sirh/10-status-and-handoff.md` | État courant et reprise |

## Licence et attribution

Ce logiciel est distribué sous **GNU Lesser General Public License v2.1**
(voir `LICENSE`). Il s'agit d'une œuvre dérivée d'Horilla HRMS
(https://github.com/horilla/horilla-hr), dont les mentions de copyright et de
licence sont conservées conformément à la licence.

Toute redistribution, y compris modifiée, doit rester sous LGPL-2.1 et conserver
`LICENSE` ainsi que les en-têtes de copyright d'origine.
