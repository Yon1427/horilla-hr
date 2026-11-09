# 10 — Status & handoff (trust document)

**Read this first in a new session.** It records what is done, what is in
flight, what remains, and the exact commands. If this file and an older note
disagree, this file wins; if this file and the code disagree, the code wins.

## Snapshot

| Item | Value |
|---|---|
| Date | 2026-11-09 |
| Repo | `/home/sidali/sirh` |
| Fork | `github.com/Yon1427/horilla-hr` (from `horilla/horilla-hr`) |
| Working branch | **`sirh-v1`** (deploy branch; `algeria/m0-m1` archived at `1f234f0`) |
| HEAD | `e3a40d6` ci/tests: run check and smoke suite in English, golden payslips pin French |
| CI | **GREEN**: Unit Tests (smoke + coverage) and Image Publish on every push to `sirh-v1` |
| Production | **Railway `sanad-sirh`** — web + scheduler pinned to `ghcr.io/yon1427/horilla-hr:sha-e3a40d6`, domain `rh.ats-dz.dev` |
| Runtime | Railway image services (web: gunicorn; scheduler: `run_scheduler`), Postgres + Redis, `/app/media` volume |
| Python | 3.12 / Django 5.2.19 (image and CI) |
| Scope | Algerian **private sector only** (loi 90-11) |

## Production (Railway)

- `/health/` → `{"status": "ok", "product": "sanad", "api": 1}`; `/` → 302 → `/login/`.
- Release = push to `sirh-v1` → CI publishes `ghcr.io/yon1427/horilla-hr:sha-<short>` →
  re-pin the service image to the new `sha-` tag (Railway never re-pulls on its own).
- Email: Resend SMTP via `DynamicEmailConfiguration` (`noreply@mail.ats-dz.dev`); every
  send is logged in `EmailLog`. Reset flow verified working end to end.
- Prod DB has the Algerian payroll components seeded (`python manage.py
  seed_algeria_payroll`, idempotent) and the global 2026 parameter row from
  migration `0018` (SNMG 24 000, 6 IRG brackets).
- Superuser `sidali.boulezaz` / `boulezaz.sidali@gmail.com` — the temporary
  password set during the reset test must be changed after login.

## Source of truth

1. `00-index.md` — reading order and conflicts.
2. `05-product-spec.md` — rule catalogue (PAY/LEG/TRM/DEC/COST/LOC), §12 conflicts.
3. `06-gap-analysis.md` — defects B1–B8 and the Horilla build map.
4. `07-contrats-et-rotation.md` — contract types and shift/rotation rules.
5. `08-implementation-plan.md` — M0/M1 tasks, exact files and tests.
6. `09-m0-delivery-notes.md` — M0 evidence and decisions.
7. `01`–`04` — research (payroll, legal, workflow, localization).
8. `11-branch-graph-map.md` — multi-establishment org graph and table map.

## Agent squad (OpenCode, V2)

| Agent | Mode | Model | Purpose |
|---|---|---|---|
| `sirh-lead` | primary | `opencode-go/deepseek-v4-pro#high` | sequencing, review, money/migration/scoping gates |
| `sirh-payroll` | subagent | `opencode-go/deepseek-v4.1-flash#high` | M0 fixes + M1 payroll core |
| `sirh-legal` | subagent | `opencode-go/muse-spark-1.3-contributor#high` | law, declarations, data contracts (read-only code) |
| `sirh-qa` | subagent | `opencode-go/crouton-alpha-free#high` | regression suite, golden cases, CI gates |
| `sirh-explore` | subagent | `opencode-go/deepseek-v4.1-flash#high` | read-only reconnaissance |

Config: `.opencode/agents/*.md`, `.opencode/opencode.json` (`default_agent: sirh-lead`).

---

## Progress

### M0 — stabilisation: **complete** (8/8)

Evidence in `09-m0-delivery-notes.md`. Weekly-off Sunday-first, bulk period +
atomicity, CSV injection safety, leave lock, conflict blocking, Decimal money.

### M1 — Algerian payroll core: **9,10,11,12,13,14 done; 15 open**

| Task | State | Where |
|---|---|---|
| M1-9 parameter model | done | `payroll/models/tax_models.py`, migration `0017` |
| M1-10 2026 seed row | done | migration `0018` (reversible) |
| M1-11 IRG engine | done, **Decimal since `9c3271f`** | `payroll/methods/dz_irg.py` + `test_dz_irg.py` |
| M1-12 `FilingStatus.tax_engine` | done | `payroll/models/models.py`, `tax_calc.py`, migration `0019` |
| M1-13 component seed command | done | `seed_algeria_payroll.py` + `test_seed_algeria_payroll.py`; **run in prod** |
| M1-14 80 000 DA golden payslip | done | `test_dz_payroll_golden.py` — exact equality, 60 844 net |
| M1-15 employer cost | **done (`6655b78`)** | `payroll/methods/dz_cost.py` + `test_dz_cost.py`, golden §7.2; corrected the spec's 626,99→626,94 slip |
| M1-16 delivery notes + gate | done (this file) | CI gate green on `sirh-v1` |

**M1 complete.** Remaining scope is M2+ (declarations, contracts/shifts,
localization, CASNOS/BTPH, costisation UI, hardening).

Gate: CI runs `makemigrations --check` + `compilemessages -l fr` + the full
smoke suite (34 apps, coverage floor 26) on every `sirh-v1` push — **green at
`e3a40d6`**. Verified in the Railway web container before pushing: 187/187 on
the golden + locale-sensitive modules.

### M2–M7 — not started

Declarations; contracts & shifts; localization; CASNOS + BTPH + bank;
costisation UI; hardening. Acceptance criteria in the old handoff remain valid.

---

## Decisions (do not silently reverse)

1. **Week starts Sunday.** Algerian weekend is Friday–Saturday. `month_week_index`
   uses `(first.weekday() + 1) % 7`; calendar is `setfirstweekday(6)`.
2. **Money is Decimal end to end in the DZ IRG engine** (`9c3271f`, supersedes the
   old "Decimal at rest, float in engine" note): the barème, abattement and
   smoothing run in `Decimal`, quantized once at `0.01` `ROUND_HALF_UP`, returned
   as `float` only at the pipeline boundary. The broader runtime pipeline
   (`payslip_calc.py`, `payroll_run.py`) is still upstream float — do not convert
   it piecemeal; it is a whole-milestone job.
3. **Conflicts block.** `unresolved_conflicts > 0` raises `PayrollBlockedError`;
   `bulk_generate` reports per employee and continues.
4. **Leave approval is locked under the company-scoped manager** with
   `select_for_update(of=("self",))`.
5. **No `except: pass` around money writes.**
6. **Effective-dated parameters.** SNMG, IRG, CNAS, TFPC/TAPP, CASNOS are data
   rows with `effective_from` + `source_url`; never hard-coded.
7. **CNAS is a normal `Deduction`** (`rate=9`, `employer_rate=25.5`,
   `is_pretax=True`, `is_tax=False`) — no parallel engine.
8. **DZ IRG is a `FilingStatus.tax_engine` switch** (`standard` | `dz_irg`).
9. **All work happens on `sirh-v1`** (C21 in `05` §12). Every push builds an
   image; a Railway release is an explicit re-pin to the new `sha-` tag.
10. **CI locale strategy**: the suite asserts English strings, so CI runs the
    check and the tests with `LANGUAGE_CODE=en`; the two golden payslip tests pin
    `fr` via `override_settings`; `compilemessages` gates the catalogues.
    `LANGUAGE_CODE` is env-overridable, default stays `fr`.

## Known issues / risks

1. Background mail threads (`leave/threading.py`) render templates after the
   request; `default_currency` then inserts `PayrollSettings` for a company that
   may be gone. Tests log an FK `IntegrityError` without failing.
2. `leave_request_creation` uses `referer_parts[-2]` on an unvalidated referer
   (pre-existing `IndexError` risk).
3. The 2026 parameter values (SNMG 24 000, CASNOS base, IRG 35 000 boundary) come
   from research marked `REP/UNV`; confirm against primary texts before they
   become blocking rules.
4. **M0-8 breaks the demo payslip re-anchor.** `normalize_demo_payslips` calls
   `payroll_calculation` without catching `PayrollBlockedError`.
5. **Never generate migrations inside the deployed container.** Its filesystem
   can diverge from the branch (we generated a phantom `horilla_documents/0004`
   against a graph with `0001_initial.py` transiently missing; CI caught it and
   the migration was reverted). Generate migrations only in a complete checkout
   and let CI's `makemigrations --check` confirm.
6. `makemigrations --check` is locale-sensitive: lazy-translated field metadata
   resolves in the active locale, so the check must run with `LANGUAGE_CODE=en`.
7. **Subagent spawns for `sirh-qa` fail** with a `tool_choice` infrastructure
   error in this environment; run QA work in the primary session until fixed.
8. Railway ssh sessions are flaky for long commands: run long test suites inside
   the container with `nohup ... > log &`, then read the log file.

## Exact commands

```bash
# Railway exec (link lives in /tmp/opencode/railway-link, re-link after reboots):
cd /tmp/opencode/railway-link
railway ssh -s web -- python manage.py shell -c '<code>'
railway ssh -s web -- python manage.py test --noinput <module> -v 0   # one at a time

# CI-equivalent local run (fresh branch tree in the container):
#   SECURE_SSL_REDIRECT=false DEBUG=True LANGUAGE_CODE=en \
#   python manage.py test --noinput <labels>
```

## Resume here (next actions)

1. **M1 is complete.** Next milestone is M2: declarations golden files
   (DEA/DAC/DAS/G50/G29) per `02-legal-declarations.md` and `08` §M2+.
2. Change the `sidali.boulezaz` temporary password in prod.

## Ground rules for the next session

- One test command at a time on the shared test DB; CI is the sign-off gate.
- Record the test count in the commit body when the suite is large.
- Never change an asserted payroll number to make a test pass. Fix the engine or
  the fixture.
- Every rate/threshold gets `effective_from` + `source_url` + confidence tag.
- Migrations: `makemigrations --check` clean (with `LANGUAGE_CODE=en`); data
  migrations reversible; never generate them inside a deployed container.
- Company scoping and permissions are not optional.
- Push only after the touched app suite is green; a Railway release is an
  explicit re-pin, not automatic.

## Open client decisions

SME vs large/multi-company group; applicable collective agreement(s); BTPH in or
out; CASNOS depth; hosting (in-Algeria vs authorised transfer); e-signature
provider; bilingual depth; migration source (Excel vs incumbent payroll).
