# Algeria — Labour Law & Statutory Declarations (SIRH spec input)

**Version:** 2026-11-07  
**Scope:** Private-sector salaried employment in Algeria (loi 90-11), social-security declarations (CNAS), employment/ANEM declarations, tax-withholding declarations (G50), occupational medicine, records, and personal-data protection. Public-sector statuts, CASNOS (non-salaried), and sector-specific régimes (journalists, maritime, home workers, etc.) are out of scope except where they change a rule below.  
**Purpose:** Product requirements for an Algerian SIRH/HCM: data fields, documents, deadlines, state machines, alerts, permissions and audit.

> **Legal disclaimer:** This is a research input, not legal advice. Every rule below is tagged. Anything not confirmed against a primary text is marked `UNVERIFIED`. Before shipping a rule that computes money or blocks a hire/fire action, have it reviewed by Algerian counsel and re-check the Journal Officiel.

---

## Confidence-tag legend

| Tag | Meaning |
|---|---|
| `[LAW]` | Text of a law/ordonnance read in a primary or official consolidated source (Journal Officiel, ministry full-text page). |
| `[DECREE]` | Executive decree/arrêté read in a primary/official source, or in a reliable reproduction where the JO scan was unreadable. |
| `[SECONDARY]` | Reputable secondary source (CNAS page, DGI calendar, APS, university reproduction). Good enough for a spec, confirm before hard-coding. |
| `[PRACTICE]` | Common practice, collective agreement, or vendor/industry convention. **No statutory basis found.** Must be configurable, never presented as law. |
| `[UNVERIFIED]` | Could not confirm article, number, duration or deadline. Do not implement as a hard rule. |

**Citation style:** `(Loi 90-11, art. 18) [1]` means the rule is in article 18 of loi 90-11 and source [1] is listed under `## Sources`. French/Arabic legal terms are kept as-is.

---

## 1. Employment contracts

> Contract-type matrix, trial rules and part-time mechanics: see `07-contrats-et-rotation.md` Part A.

### 1.1 Contract types and the written-form rule

- The employment relationship can arise from a **written or oral** contract. It exists in any case **from the sole fact of working for an employer**. `[LAW]` (Loi 90-11, arts. 8–10) [1]
- A contract is **presumed indefinite (CDI)** unless the parties have provided otherwise **in writing**. If there is no written contract, the relationship is presumed CDI. `[LAW]` (Loi 90-11, art. 11) [1]
- Therefore, **a written CDI is not a legal requirement**. A written contract is nevertheless required for CDD (to state duration and motive), apprenticeship, and is strongly advisable for proof. `[LAW]` (Loi 90-11, arts. 11–12; Loi 81-07, art. 11) [1][13]
- The law does not impose a general list of mandatory CDI clauses. Mandatory content is limited to specific contract types and to the payslip (art. 86). `[LAW]` [1]

### 1.2 CDI

- Open-ended by default. No maximum duration. `[LAW]` (Loi 90-11, art. 11) [1]
- Termination modes are listed exhaustively in art. 66: nullity/abrogation, expiry of CDD, resignation, dismissal, total incapacity, economic layoff, legal cessation of the employer, retirement, death. **Mutual agreement is not listed as a termination mode.** `[LAW]` (Loi 90-11, art. 66) [1]
- A **rupture conventionnelle** (French-style mutually agreed termination) is **not provided for** in loi 90-11. `[LAW]` (absence from art. 66) [1] — any "rupture conventionnelle" feature must be labelled `PRACTICE/UNVERIFIED`.

### 1.3 CDD (contrat à durée déterminée)

**Permitted cases (limitative list):** `[LAW]` (Loi 90-11, art. 12, as supplemented by Ordonnance 96-21) [1]

1. Work linked to **non-renewable works or service contracts**.
2. **Replacement** of an absent employee whose post the employer must keep.
3. **Periodic/discontinuous work** of the employer.
4. **Work overload** or **seasonal** reasons.
5. **Activities or jobs of limited duration** or **temporary by nature**.

**Mandatory content:** the contract must state the **duration** of the relationship **and the motive** for the fixed term. `[LAW]` (Loi 90-11, art. 12) [1]

**Maximum duration / renewals:** **No statutory maximum duration and no statutory renewal cap in loi 90-11.** The law only requires a lawful motive and a stated duration. `[LAW]` (Loi 90-11, art. 12; no provision in the text) [1]  
→ Do **not** hard-code "3 years" or "one renewal". Those figures circulate in vendor content but are not in the law. `UNVERIFIED` whether a sectoral collective agreement adds a cap.

**Sanction for abuse:** a CDD concluded in breach of the law is **reclassified as a CDI**. `[LAW]` (Loi 90-11, art. 14) [1]

**Inspection control:** the labour inspector verifies that the CDD falls within one of the art. 12 cases and that the duration matches the activity. `[LAW]` (Loi 90-11, art. 12 bis, inserted by Ordonnance 96-21) [1]

**Visa/registration:** no general visa or deposit of the CDD with the labour inspectorate. The control is a posteriori by the inspector. `[LAW]` (art. 12 bis) [1]

### 1.4 Contrat d'apprentissage

- Governed by **loi 81-07 du 27 juin 1981 relative à l'apprentissage**. `[LAW]` [13]
- Definition: employer undertakes to provide **methodical and complete vocational training**; apprentice undertakes to work for the employer for the contract duration in return for a **presalaire**. `[LAW]` (Loi 81-07, art. 10) [13]
- **Written** contract, signed by the **employer, the apprentice and the legal guardian**. It is **registered with the commune (APC)** of the place of apprenticeship, which transmits it for **validation** to the nearest vocational-training institution. `[LAW]` (Loi 81-07, art. 11) [13]
- **Duration:** minimum **1 year**, maximum **3 years**; per-specialty duration set by regulation. `[LAW]` (Loi 81-07, art. 4) [13]
- **Age:** minimum **15**, maximum **18** at signature; maximum extended to **20** for persons with a physical disability. `[LAW]` (Loi 81-07, art. 12) [13]
- **Presalaire:** paid by the **State** for the first 6–12 months, then a progressive presalaire indexed to the SNMG and paid by the **employer**. `[LAW]` (Loi 81-07, art. 16) [13]
- **Social contributions:** employer exempt for the apprentice for social insurance, work-accident insurance and family allowances; these are borne by the State during the contract. `[LAW]` (Loi 81-07, art. 20) [13]
- **Headcount obligation:** apprenticeship quotas apply by employer size (e.g. 1–5 employees → at least 1 apprentice, max 3; 21–40 → at least 2, max 6; etc.). `[LAW]` (Loi 81-07, art. 9) [13]
- **Termination:** automatic in listed cases (death, bankruptcy, definitive cessation, permanent incapacity, etc.) and at expiry; otherwise unilateral, amicable or judicial. `[LAW]` (Loi 81-07, arts. 23–24) [13]
- SIRH note: apprenticeship is **not** a normal CDD; it has its own register, presalaire, school calendar and age checks.

### 1.5 Contrat de travail temporaire / intérim

- No general statutory "travail temporaire" contract type in loi 90-11. `[LAW]` (absence from arts. 11–14) [1]
- Private placement agencies are regulated by **loi 04-19 du 25 décembre 2004 relative au placement des travailleurs et au contrôle de l'emploi**. `[LAW]` [15][25]
- `UNVERIFIED`: whether a separate legal regime for *entreprises de travail temporaire* (ETT) exists beyond loi 04-19. Until confirmed, model intérim as a **CDD** with the user employer and a commercial supply contract with the agency; do not create a statutory "temp" status.

### 1.6 Période d'essai (trial period)

- A newly recruited employee may be subject to a trial period whose duration **may not exceed six (06) months**. It may be extended to **twelve (12) months** for **high-qualification posts**. `[LAW]` (Loi 90-11, art. 18) [1]
  - ⚠️ The MTESS consolidated text prints **"dix (06) mois"**, which is internally contradictory. Read it as **six months**; the rectificatif published at JO p. 488 should be checked. `UNVERIFIED` wording, `LAW` substance.
- The trial period is **set by collective bargaining**, for each category of workers or for all workers. There is **no statutory per-category table** (ouvrier/employé/cadre). `[LAW]` (Loi 90-11, art. 18) [1]
- During trial, the employee has the same rights and obligations as similar employees; the trial counts toward **seniority** if confirmed. `[LAW]` (Loi 90-11, art. 19) [1]
- During trial, either party may terminate **at any time, without notice and without indemnity**. `[LAW]` (Loi 90-11, art. 20) [1]
- Does art. 18 apply to CDD? The text says "travailleur nouvellement recruté", not "CDI". In practice, a trial clause in a CDD must fit inside the CDD duration. `[PRACTICE]` / `UNVERIFIED` for short CDDs.

### 1.7 Language of the contract

- Loi 90-11 contains **no language requirement** for the contract. `[LAW]` (absence) [1]
- Arabic is the **official language** of the State; French is widely used in private-sector HR and payroll. `[LAW]` Constitution, but not a contract-form rule.
- `UNVERIFIED`: whether a private-sector employment contract must be drafted in Arabic (or translated/legalised). Do not block a hire on language; store `contract_language` and produce a bilingual template if the customer requires it. `[PRACTICE]`

### 1.8 Foreign workers

- Employment of foreigners requires a **work permit / temporary work authorisation** under **loi 81-10 du 11 juillet 1981** and **décret 82-510 du 25 décembre 1982**. `[LAW]` [25]
- Employer must first establish that no qualified national labour is available. `[LAW]` (Loi 90-11, art. 21) [1]
- SIRH: separate document set (permit, residence, contract visa) and expiry alerts. Details of the permit procedure are `UNVERIFIED` here.

---

## 2. Working time

### 2.1 Legal duration

- **40 hours per week** in normal conditions. `[LAW/DECREE]` (Ordonnance 97-03 du 11 janvier 1997, art. 2; MTESS summary) [3][24]
- The 40 hours are distributed over **at least five working days**. `[LAW/DECREE]` (Ordonnance 97-03, art. 2) [3][24]
- Ordonnance 97-03 **abrogated articles 22–26 of loi 90-11** (the old 44-hour regime). `[LAW]` (Ordonnance 97-03, art. 8) [3]
- **Daily amplitude:** 12 hours maximum. `[SECONDARY]` (MTESS summary; the original art. 26 of loi 90-11 was abrogated by Ordonnance 97-03 art. 8 — the 12-hour cap is restated in the applicable schedule rules). Article number in Ordonnance 97-03: `UNVERIFIED`. [24]
- **Continuous shift (séance continue):** a break of no more than one hour, of which **half an hour is counted as working time**. `[SECONDARY]` (MTESS summary; the original loi 90-11 art. 25 was abrogated by Ordonnance 97-03 art. 8, so the rule is restated in the applicable schedule rules). Article number in Ordonnance 97-03: `UNVERIFIED`. [24]

### 2.2 Weekend and weekly rest

- One **full day of rest per week**. The normal weekly rest day is **Friday**. `[LAW]` (Loi 90-11, art. 33) [1]
- The weekly rest may be **deferred or taken on another day** where economic/organisational imperatives require it; rotating rest is allowed for activities that cannot stop on the normal rest day. `[LAW]` (Loi 90-11, art. 37) [1]
- Retail: the weekly rest day for all or part of the staff is set by **arrêté du wali**. `[LAW]` (Loi 90-11, art. 38) [1]
- **Saturday is not a statutory rest day.** The two-day (Friday–Saturday) weekend is administrative/public-sector practice and widespread private practice. `[PRACTICE]` `[UNVERIFIED]` as a general private-sector legal rule.
- SIRH: model `weekly_rest_day` (default Friday) and `non_working_days[]` separately. Do not assume Sat/Sun.

### 2.3 Night work

- Night work is work performed **between 21:00 and 05:00**. `[LAW]` (Loi 90-11, art. 27) [1]
- Workers of either sex **under 19** may not perform night work. `[LAW]` (Loi 90-11, art. 28) [1]
- The law **prohibits employers from using female staff for night work**, subject to **special derogations granted by the territorially competent labour inspector** where the nature of the activity and the post justify it. `[LAW]` (Loi 90-11, art. 29) [1]  
  → This is still the literal text. Implement it as a **legal restriction with an inspector-derogation flag**, not as a silent gender rule. Counsel should confirm current enforcement/non-discrimination interpretation.
- Night work rules, conditions and rights are set by **collective agreements**. `[LAW]` (Loi 90-11, art. 27) [1]

### 2.4 Shift work

- The employer may organise **successive teams / travail posté** where production or service needs require it. `[LAW]` (Loi 90-11, art. 30) [1]
- Shift work gives right to an **indemnity**. `[LAW]` (Loi 90-11, art. 30) [1]

### 2.5 Overtime (heures supplémentaires)

- Recourse to overtime must respond to an **absolute necessity of service** and be **exceptional**. `[LAW]` (Loi 90-11, art. 31) [1]
- Cap: overtime may not exceed **20% of the legal duration** (i.e. **8 hours/week** on a 40-hour base). `[LAW]` (Loi 90-11, art. 31) [1]
- Minimum majoration: **50% of the normal hourly wage**. `[LAW]` (Loi 90-11, art. 32) [1]
- Exceptions above the 20% cap are allowed only to:
  - prevent imminent accidents or repair damage from accidents;
  - finish works whose interruption would, by their nature, cause damage.  
  In those cases, **workers' representatives must be consulted** and the **labour inspector informed**. `[LAW]` (Loi 90-11, art. 31, as supplemented by Ordonnance 96-21) [1]
- No prior administrative authorisation for normal overtime; the inspector is informed only in the exception cases. `[LAW]` (art. 31) [1]
- SIRH: cap alert at 8h/week; block/require override reason + representative consultation + inspector notification for exception overtime.

### 2.6 Work on weekly rest day / public holiday

- An employee who works on a **legal rest day** is entitled to **compensatory rest of equal duration** and to the **overtime majoration**. `[LAW]` (Loi 90-11, art. 36) [1]
- Public holidays are **legal rest days**. `[LAW]` (Loi 90-11, art. 35) [1]

### 2.7 Ramadan

- **Private sector only:** there is **no general statutory reduction** of working time during Ramadan. The employer sets the timetable by internal rules or collective agreement; a 1–2 hour reduction is common but not a legal right. `[PRACTICE]` / `UNVERIFIED`. (Public-sector schedules are out of scope.)
- **Private sector:** **no general statutory reduction of working time during Ramadan was found.** `[LAW]` (absence) [1]  
  → Model Ramadan hours as a **company policy / collective-agreement rule**, with a default "no change" and an optional 35h/week or 6h/day template. `[PRACTICE]`
- Ramadan start/end depend on the lunar calendar and official announcement (see §4).

---

## 3. Leave

### 3.1 Annual paid leave (congé annuel)

- Every employee has a right to **paid annual leave**; any waiver by the employee is **null**. `[LAW]` (Loi 90-11, art. 39) [1]
- **Accrual:** **2.5 days per month of work**, global duration **not exceeding 30 calendar days per work year**. `[LAW]` (Loi 90-11, art. 41) [1]
- **Reference period:** **1 July of the previous year to 30 June of the leave year**. For new hires, the reference period starts on the **hire date**. `[LAW]` (Loi 90-11, art. 40) [1]
- **First month of a new hire:** a period **greater than 15 working days** in the first month counts as **one month** of work for leave accrual. `[LAW]` (Loi 90-11, art. 44, as amended by Ordonnance 96-21) [1]
- **Equivalence:** any period equal to **24 working days or 4 weeks** = one month; **180 working hours** for seasonal/part-time workers. `[LAW]` (Loi 90-11, art. 43) [1]
- **South (wilayas du Sud):** additional leave of **not less than 10 days per work year**. `[LAW]` (Loi 90-11, art. 42, as amended) [1]
- **Arduous/dangerous work:** main leave may be increased; modalities by collective agreement. `[LAW]` (Loi 90-11, art. 45) [1]
- **Leave indemnity:** equal to **one twelfth (1/12) of the total remuneration** received during the reference year (or the year preceding the leave). `[LAW]` (Loi 90-11, art. 52) [1]
- **Leave schedule/fractioning:** fixed by the employer after consulting the participation committee where it exists. `[LAW]` (Loi 90-11, art. 51) [1]
- **Suspension/interruption:** the relationship cannot be suspended or terminated during annual leave; the employee may interrupt leave because of illness and move to sick leave. `[LAW]` (Loi 90-11, arts. 49–50) [1]
- **Carry-over:** **not addressed by loi 90-11.** `UNVERIFIED` / `[PRACTICE]`. Implement a configurable carry-over rule (e.g. 12 months) and an accrual cap; do not present it as statutory.
- **Payment on exit for untaken leave:** the law prohibits waiver, so unused leave must be compensated; the **calculation method on exit is not specified**. Apply the art. 52 one-twelfth formula pro rata. `[LAW]` principle + `UNVERIFIED` exit formula. [1]
- **Long sick leave:** a long sick leave can open right to **no more than one month** of annual leave, whatever the duration of the sick leave. `[LAW]` (Loi 90-11, art. 47) [1]

### 3.2 Sick leave (congé de maladie)

- The employment relationship is **suspended by law** during sick leave as provided by social-security legislation. `[LAW]` (Loi 90-11, art. 64) [1]
- **CNAS daily indemnity (indemnité journalière):**
  - **50%** of the contributory wage (after social contribution and IRG) for the **first 15 days** of absence.
  - **100%** from the **16th day**, and in case of **hospitalisation** or **long-term illness (affection de longue durée)**. `[SECONDARY]` (CNAS, Assurance Maladie) [9]
- **Declaration to CNAS:** the employee must declare the work stoppage to the fund **within 2 working days** (the day fixed for the stoppage not included), by deposit or post of the medical certificate. `[SECONDARY]` (CNAS, Assurance Maladie) [9]
- **Employer role:** historically the employer pays the daily indemnities on behalf of CNAS and is reimbursed (décret exécutif 91-339). `[SECONDARY]` [9] / `[DECREE]` (Décret 91-339) — text not re-read here.
- **Employer top-up:** **no general statutory obligation** to maintain full salary beyond CNAS. Collective agreements or the règlement intérieur may provide a complement. `[LAW]` (absence) + `[PRACTICE]`.
- **Maximum duration:** not set in loi 90-11. CNAS long-term illness rules apply; exact maximum `UNVERIFIED`. Do not cap the case in the SIRH without a configuration/medical rule.
- **Return-to-work medical visit:** mandatory after occupational disease/accident, maternity, **21 days or more** of non-occupational illness, and repeated absences. `[DECREE]` (Décret 93-120) [12]

### 3.3 Maternity leave

- **150 consecutive days**, indemnified at **100%** of the daily wage (after social contribution and IRG). It starts **at the earliest 42 days before the expected delivery date**. If delivery occurs earlier, the 150-day period is **not reduced**. `[LAW]` (Loi 25-08 du 19 juillet 2025, art. 29, modifying loi 83-11 art. 29) [7]
- **Extensions for a newborn with disability, congenital malformation or serious illness requiring mandatory support/medical intervention:**
  - first extension: **50 consecutive days** after the legal maternity leave, subject to a medical file deposited at least **15 days** before the end of the initial period;
  - second extension: up to **165 additional days**, subject to a further medical file. `[LAW]` (Loi 25-08, art. 29) [7]
- CNAS summarises this as **21 weeks (150 days)** at 100%, from the effective cessation of work. `[SECONDARY]` (CNAS, Assurance Maternité) [10]
- **Employer obligations:** the employment relationship is suspended; the employer must keep the post and allow return. `[LAW]` (Loi 90-11, arts. 55, 64–65) [1]
- ⚠️ The MTESS "Législation du travail" summary still says **14 weeks**; that summary predates loi 25-08. For 2026, use **150 days**. `[LAW]` [7] over `[SECONDARY]` [24].
- **Maternity is a suspension cause** and counts as working time for annual leave. `[LAW]` (Loi 90-11, art. 46) [1]

### 3.4 Paternity leave

- **No separate statutory paternity leave.** The father is entitled to the **3 working days** paid exceptional leave for the **birth of a child**. `[LAW]` (Loi 90-11, art. 54) [1]
- Any longer paternity leave is `[PRACTICE]` / collective agreement / `UNVERIFIED`.

### 3.5 Exceptional paid leave (absences exceptionnelles)

- **3 working days paid**, on each of the following family events: `[LAW]` (Loi 90-11, art. 54, as amended by Ordonnance 96-21) [1]
  - marriage of the employee;
  - birth of an employee's child;
  - marriage of a descendant of the employee;
  - death of an ascendant, descendant, or **first-degree collateral** of the employee or spouse;
  - death of the spouse;
  - **circumcision** of an employee's child.
- For **birth** or **death**, justification may be provided **afterwards**. `[LAW]` (art. 54) [1]
- Also paid leave for: union/staff-representation tasks; authorised professional or union training; academic/professional exams. `[LAW]` (art. 54) [1]
- **Hajj (pilgrimage):** once during the employee's professional career. `[LAW]` (Loi 90-11, art. 54) [1]  
  → Duration is **not specified** in the law. `UNVERIFIED`; common practice is the actual pilgrimage period (often ~1 month). Make it a configurable leave type.

### 3.6 Unpaid leave

- Special **unpaid** absences may be granted by the employer to employees with an imperative need, under the conditions of the **règlement intérieur**. `[LAW]` (Loi 90-11, art. 56) [1]
- Unpaid leave is a **suspension cause**. `[LAW]` (Loi 90-11, art. 64) [1]

### 3.7 Union / staff-representative leave

- Paid absences for union or staff-representation tasks, within the durations set by law or collective agreement. `[LAW]` (Loi 90-11, art. 54) [1]
- **Staff delegates** have a monthly **10-hour paid credit** for their mandate, except during annual leave. Credits may be pooled with the employer's agreement. `[LAW]` (Loi 90-11, arts. 106–107) [1]
- Time spent in meetings convened/accepted by the employer does not count against the 10-hour credit. `[LAW]` (Loi 90-11, art. 108) [1]

### 3.8 Religious leave / holidays for non-Muslim staff

- Christian and Jewish employees (Algerian or foreign) are entitled to the specific legal holidays listed in §4. `[LAW]` (Loi 63-278, arts. 3–4, as summarised by MTESS) [5][24]
- No general "religious leave" beyond those holidays and Hajj. `[LAW]` (absence) [1]

---

## 4. Public holidays

### 4.1 Statutory list

Legal holidays are fixed by **loi 63-278 du 26 juillet 1963, modifiée et complétée**, in particular by **loi 23-10 du 26 juin 2023** (Aïd durations) and **loi 18-12 du 2 juillet 2018** (Yennayer). `[LAW]` [4][5][6]

**Fixed national holidays** `[LAW]` (Loi 63-278, art. 1; MTESS summary) [5][24]

| Date | Holiday | Days |
|---|---|---|
| 1 January | New Year (Gregorian) | 1 |
| 12 January | **Yennayer** (Amazigh New Year) — added by loi 18-12 (2018) | 1 |
| 1 May | Labour Day | 1 |
| 5 July | Independence Day | 1 |
| 1 November | Revolution Day | 1 |

**Religious holidays (Muslim)** `[LAW]` (Loi 63-278, art. 1, as modified by loi 23-10 du 26 juin 2023) [4][5]

| Holiday | Days |
|---|---|
| Aïd el-Fitr (Eid al-Fitr) | **3 days** (was 2 before 2023) |
| Aïd el-Adha (Eid al-Adha) | **3 days** (was 2 before 2023) |
| Awal Moharram (Hijri New Year) | 1 |
| Achoura (10 Moharram) | 1 |
| El Mawlid Ennabaoui (Prophet's birthday) | 1 |

**Christian employees** `[LAW]` (Loi 63-278, arts. 3–4, per MTESS) [5][24]

- Easter Monday
- Ascension
- 15 August (Assumption)
- 25 December (Christmas)

**Jewish employees** `[LAW]` (Loi 63-278, arts. 3–4, per MTESS) [5][24]

- Rosh Hashanah
- Yom Kippur
- Passover

> Note: the MTESS summary still says Aïd = 2 days. Loi 23-10 (2023) raised both to **3 days**. Use 3 days for 2026. `[LAW]` [4] over `[SECONDARY]` [24].

### 4.2 How religious dates are officially confirmed

- The **Commission nationale d'observation du croissant lunaire et des calendriers religieux**, under the **Ministère des Affaires religieuses et des Wakfs**, is the body that observes the crescent and announces the start/end of Ramadan and the dates of Aïd. `[SECONDARY]` (multiple Algerian press reports; commission meeting at Dar El-Imam, Alger) [21]
- The announcement is made by official communiqué and broadcast by national media, usually after the Maghrib prayer on the "night of doubt" (nuit du doute). `[SECONDARY]` [21]
- Example: for 2026 the commission announced **Aïd el-Fitr on Friday 20 March 2026**. `[SECONDARY]` [21]  
  → This is an example, **not** a rule to hard-code for future years.

### 4.3 How a SIRH should model movable holidays

Recommended model:

1. Store a **holiday definition** (`code`, `name_fr`, `name_ar`, `type = FIXED | HIJRI | CHRISTIAN | JEWISH`, `duration_days`, `legal_basis`).
2. For **fixed** holidays, generate occurrences from the Gregorian date every year.
3. For **Hijri** holidays, store the **Hijri year + month + day**, compute an **expected Gregorian window** from a lunar-calendar library, and require a **confirmed date** record with:
   - `confirmed_date`, `confirmed_by = Commission nationale...`, `announcement_source`, `announcement_at`, `status = EXPECTED | CONFIRMED`.
4. Never block payroll on an `EXPECTED` date. Run payroll on `CONFIRMED`; keep an override with a reason and audit trail.
5. Support **multi-day spans** (Aïd = 3 days) and **per-religion eligibility** (Christian/Jewish holidays apply only to declared members of those confessions; do not infer religion silently — see §9).
6. Handle **holiday falling on the weekly rest day**: no statutory substitution rule was found. `UNVERIFIED`. Make it a policy flag; do not automatically add a replacement day.
7. Keep a **calendar version** per year and per establishment, so retroactive corrections do not silently rewrite past payroll.

---

## 5. Termination

### 5.1 Termination modes

Exhaustive list in **art. 66**: nullity/abrogation, CDD expiry, resignation, dismissal, total incapacity, economic layoff, legal cessation of the employer, retirement, death. `[LAW]` (Loi 90-11, art. 66) [1]

### 5.2 Resignation (démission)

- Resignation is a **right** of the employee. It must be **in writing**. `[LAW]` (Loi 90-11, art. 68) [1]
- The employee leaves after a **notice period** whose conditions are fixed by **collective agreements**. `[LAW]` (Loi 90-11, art. 68) [1]
- **No statutory notice duration** in loi 90-11. `[LAW]` (absence) [1]  
  → Common practice is **1 month** for employees and **3 months** for cadres, but this is `[PRACTICE]`/collective agreement. `UNVERIFIED` as a general legal rule.

### 5.3 Dismissal for serious fault (licenciement disciplinaire)

- Dismissal for **serious fault (faute grave)** is governed by the **règlement intérieur**. `[LAW]` (Loi 90-11, art. 73) [1]
- Non-exhaustive list of serious faults (art. 73, as modified by loi 91-29): `[LAW]` [1]
  - unjustified refusal to execute professional instructions;
  - disclosure of professional/technical/internal information;
  - participation in a collective and concerted stoppage in breach of the law;
  - violence;
  - intentional damage to buildings, machines, tools, raw materials, etc.;
  - refusal to execute a requisition order;
  - consumption of alcohol or drugs at the workplace.
- The employer must consider the **circumstances**, **extent**, **gravity**, **harm caused**, and the employee's **previous conduct** when qualifying the fault. `[LAW]` (Loi 90-11, art. 73-1) [1]
- **Procedure (mandatory):** `[LAW]` (Loi 90-11, art. 73-2) [1]
  1. **Written notification** of the dismissal decision;
  2. **Hearing** of the employee by the employer;
  3. the employee may be **assisted by a worker of their choice** from the same employer.
- Any individual dismissal in breach of the law is **presumed abusive**, with the burden of proof on the employer. `[LAW]` (Loi 90-11, art. 73-3) [1]
- **Remedies:** `[LAW]` (Loi 90-11, art. 73-4, as amended by Ordonnance 96-21) [1]
  - If the dismissal violates mandatory legal/conventional **procedure**, the court **annuls** it, orders the employer to complete the procedure, and awards compensation **not less than the salary the employee would have earned had they continued working**.
  - If the dismissal violates **art. 73** (no serious fault), it is **presumed abusive**; the court orders **reinstatement with acquired benefits**, or, if either party refuses, compensation **not less than 6 months' salary**, plus possible damages.
- **Notice:** a dismissed employee who has not committed a serious fault is entitled to a **délai-congé** whose **minimum duration is fixed by collective agreements**. `[LAW]` (Loi 90-11, art. 73-5) [1]
- During notice, the employee has **2 hours per day, cumulative and paid**, to look for another job. The employer may pay the equivalent remuneration in lieu of notice. `[LAW]` (Loi 90-11, art. 73-6) [1]

### 5.4 Economic dismissal / compression d'effectifs

- Permitted where **economic reasons** justify it. `[LAW]` (Loi 90-11, art. 69) [1]
- Before layoffs, the employer must use all means to reduce the number of dismissals: reduce hours, part-time, retirement, transfers to other activities/companies. `[LAW]` (Loi 90-11, art. 70) [1]
- Layoff modalities are set after **collective negotiation**, based on **seniority, experience and qualification** for each post. `[LAW]` (Loi 90-11, art. 71) [1]
- The employer must be **up to date with social-security contributions**, including unemployment and early-retirement regimes, before implementing layoffs. `[DECREE]` (Décret législatif 94-09, art. 20) [16]
- **Indemnity:** an employee dismissed in a compression d'effectifs and **admitted to unemployment insurance** is entitled to **3 months' salary** at the employer's charge, paid at dismissal. `[DECREE]` (Décret législatif 94-09, art. 22) [16]
- **Important:** art. 72 of loi 90-11 (1 month per year, capped at 15 months) was **abrogated** by Décret législatif 94-09, art. 35. Do **not** implement the old 1-month/15-month formula as the statutory rule. `[LAW]` (94-09, art. 35) [16]

### 5.5 Abusive dismissal — compensation formula

- Minimum **6 months' salary** where the dismissal is abusive and reinstatement is refused. `[LAW]` (Loi 90-11, art. 73-4) [1]
- Plus **damages** where applicable. `[LAW]` (art. 73-4) [1]
- If the procedure was violated: compensation **not less than the salary since dismissal** (i.e. as if the employee had continued working). `[LAW]` (art. 73-4, first paragraph) [1]

### 5.6 Certificates and documents on exit

- **Certificat de travail** is mandatory on cessation: it must state the **hire date**, **cessation date**, **posts held** and **corresponding periods**. `[LAW]` (Loi 90-11, art. 67) [1]
- Delivery of the certificate does **not** extinguish the parties' rights/obligations under the contract, unless otherwise agreed in writing. `[LAW]` (art. 67) [1]
- **Attestation de salaire:** required in practice for CNAS benefits (daily indemnities, maternity, etc.); CNAS provides an online service to verify/download declared salaries. `[SECONDARY]` (CNAS) [8][26] — no single loi 90-11 article; `[PRACTICE]`/CNAS form.
- **Payslip (fiche de paie):** mandatory, itemised, with all remuneration elements named. `[LAW]` (Loi 90-11, art. 86) [1]

### 5.7 CNAS notification on hire/exit

- **Hire:** employer must request affiliation of the beneficiary **within 10 days of recruitment**. `[LAW]` (Loi 83-14, art. 10, per CNAS) [8]
- **Exit / cessation:** the employer must declare the cessation and update the employee's situation. The **exact deadline is not stated on the CNAS page reviewed** and was not confirmed in loi 83-14. `UNVERIFIED`.  
  → Product rule: create a "cessation declaration" task with a **10-day default** (mirroring affiliation), flagged as configurable; do not claim it is statutory until confirmed.

### 5.8 Labour court procedure and deadlines

- **Mandatory prior conciliation** before the **bureau de conciliation** at the labour inspectorate; no court action without it. `[LAW]` (Loi 90-04, per MTESS summary, arts. 26–32) [24]
- The employee may seize the inspector by **written request** or by appearing; the inspector draws up a **procès-verbal** of the declaration. `[LAW]` (Loi 90-04, per MTESS) [24]
- Within **3 days** of seizure, the inspector convenes the parties; at least **8 days** between convocation and hearing. `[LAW]` (Loi 90-04, per MTESS) [24]
- If the defendant does not appear, a new conciliation meeting is held **within 8 days**. `[LAW]` (Loi 90-04, per MTESS) [24]
- If the claimant does not appear, the case may be **radiated**. `[LAW]` (Loi 90-04, per MTESS) [24]
- Agreement or non-conciliation is recorded in a **procès-verbal**. A conciliation agreement must be executed **within 30 days**; if not, the social-court president may order execution after a **15-day grace period**, with a daily astreinte **not less than 25% of the SNMG**. `[LAW]` (Loi 90-04, per MTESS) [24]
- If conciliation fails, the competent party seizes the **tribunal siégeant en matière sociale**. The **first hearing is fixed within 15 days** of the introductory claim. `[LAW]` (Loi 90-04, per MTESS) [24]
- The social court is composed of a magistrate and **two worker assessors + two employer assessors**. `[LAW]` (Loi 90-04, per MTESS) [24]
- **Legal aid** is granted as of right to any worker/apprentice whose salary is **below twice the SNMG**. `[LAW]` (Loi 90-04, per MTESS) [24]
- **Time limit to bring a claim:** not found in the reviewed texts. `UNVERIFIED`. Do not display a limitation period in the UI without counsel confirmation.

---

## 6. Discipline

### 6.1 Règlement intérieur (RI)

- **Mandatory** for employers with **20 or more employees**. The employer must draft it and submit it for **opinion** to the participation bodies, or failing that, to staff representatives, before implementation. `[LAW]` (Loi 90-11, art. 75) [1]
- **Optional** for employers with **fewer than 20** employees, depending on the activity. `[LAW]` (Loi 90-11, art. 76) [1]
- The RI must fix: work organisation, hygiene, safety and **discipline**. In disciplinary matters it must fix the **qualification of professional faults**, the **degrees of corresponding sanctions**, and the **implementation procedures**. `[LAW]` (Loi 90-11, art. 77) [1]
- RI clauses that remove or limit employees' statutory/conventional rights are **null**. `[LAW]` (Loi 90-11, art. 78) [1]
- The RI must be **deposited with the territorially competent labour inspectorate for approval of conformity within 8 days**. It takes effect from deposit; the employer must give it **wide publicity** to employees. `[LAW]` (Loi 90-11, art. 79) [1]

### 6.2 Sanctions ladder

- **No statutory ladder of sanctions** in loi 90-11. The ladder is defined by the **RI** (or collective agreement). `[LAW]` (Loi 90-11, art. 77) [1]
- Typical ladder found in Algerian RIs (practice, not law): `[PRACTICE]`
  1. avertissement écrit;
  2. blâme;
  3. mise à pied (suspension) with or without pay for a fixed short period;
  4. rétrogradation / changement de poste;
  5. licenciement disciplinaire.
- The only **statutory** sanction framework is the **serious-fault dismissal** procedure (art. 73-2: written notification + hearing + assistance) and the **suspensive disciplinary decision** which suspends the contract (art. 64). `[LAW]` [1]

### 6.3 Procedure and time limits

- Mandatory for dismissal: written notification, hearing, assistance by a coworker. `[LAW]` (Loi 90-11, art. 73-2) [1]
- **Time limits for sanctions (prescription of fault, delay between facts and sanction):** not set by loi 90-11. `UNVERIFIED`. Set them in the RI (e.g. 1 month/3 months) and make them configurable. `[PRACTICE]`
- The employee must be able to see the file? Loi 90-11 does not grant a general "dossier disciplinaire" access right. Data-protection access rights apply to personal data (§9). `[LAW]` (absence) + `[LAW]` (loi 18-07, art. 34) [1][17]

### 6.4 Employee file

- No statutory "employee file" format or retention in loi 90-11. `[LAW]` (absence) [1]
- The employer must be able to present **registers and documents** to the labour inspector (loi 88-07, art. 32), and to CNAS controllers (CNAS control page). `[LAW]` (Loi 88-07, art. 32) [11]; `[SECONDARY]` (CNAS) [8]
- SIRH: keep disciplinary decisions, hearing minutes, notifications and proof of delivery in a restricted folder; log every read/write.

---

## 7. Statutory declarations (backbone of the module)

### 7.1 CNAS — employer affiliation

- **When:** as soon as the employer occupies one or more workers, regardless of the legal nature, duration or form of the relationship. `[SECONDARY]` (CNAS, Employeur) [8]
- **Deadline:** deposit the employer activity declaration at the CNAS agency of the place of establishment **within 10 days of recruiting the first employee**. `[SECONDARY]` (CNAS, Employeur) [8]
- **File:** activity declaration; birth certificate No. 12 of the manager/owner; copy of commercial register/creation decision/agreement/artisan card; articles of association; tax identification card; statistical identification number (NIS); bank/postal RIB/RIP. `[SECONDARY]` (CNAS) [8]

### 7.2 CNAS — employee affiliation (déclaration d'embauche, "DEA")

- **Deadline:** request affiliation of the social-security beneficiary **within 10 days of recruitment**. `[LAW]` (Loi 83-14, art. 10, per CNAS) [8]
- **Who:** any person, whatever their nationality, who performs a remunerated activity, whatever the amount or nature of the remuneration, full-time, part-time or occasional. `[LAW]` (Loi 83-14, art. 8, per CNAS) [8]
- **File:** affiliation request; birth certificate No. 12 (if not already registered); family record if married. `[SECONDARY]` (CNAS) [8]
- **Special categories:** home workers, domestic staff, artists/authors, seafarers paid by share, **apprentices**, students, disabled persons, etc. `[SECONDARY]` (CNAS) [8]
- **Automatic affiliation:** if the employer fails to declare within the deadline, CNAS may affiliate **ex officio** (own initiative, administrative control, employee/union request). `[LAW]` (Loi 83-14, art. 12, per CNAS) [8]
- **Sanction risk:** undeclared work exposure, CNAS penalties, back contributions. `[SECONDARY]` [8]

### 7.3 CNAS — contributions (DAC)

- **Contribution base:** all salary elements / proportional income, excluding family benefits, expense reimbursements, exceptional indemnities, certain residence/isolation allowances. Monthly base cannot be below the **SNMG**. `[SECONDARY]` (CNAS) [8]
- **Rate (general case):** **34.5%** of the contribution base:
  - **25%** employer;
  - **9%** employee;
  - **0.5%** of gross payroll for social works. `[SECONDARY]` (CNAS, page last modified 29/04/2025) [8]
  - ⚠️ Some older sources state 26% employer / 9% employee = 35%. Use the current CNAS 34.5% split but make rates **table-driven by effective date**; verify with the current DAC and any 2026 finance law.
- **Declaration and payment (DAC — Déclaration d'Assiette de Cotisation):**
  - employers with **fewer than 10 employees**: within **30 days after each quarter**;
  - employers with **more than 10 employees**: within **30 days after each month**. `[SECONDARY]` (CNAS, Loi 83-14 art. 21) [8]
  - Filing online via the **Télédéclaration** portal or on the DAC form. `[SECONDARY]` (CNAS) [8][26]
- **Late payment:** majorations and penalties. `[SECONDARY]` (CNAS) [8]
- **Abatements:** employer-share reductions exist for new recruitment; see CNAS "Abattements sur taux de cotisations". `[SECONDARY]` [8] — not detailed here.

### 7.4 CNAS — annual declaration (DAS)

- **DAS = Déclaration Annuelle des Salaires et des salariés.** The employer must send to the CNAS collection agency, **within 30 days after the end of each calendar year**, a nominative declaration of salaries and employees showing remuneration received between 1 January and 31 December, **by quarter**, and the contributions due. `[LAW]` (Loi 83-14, art. 14, per CNAS) [8]
- Filed **electronically**; CNAS provides extraction software; submission via the Télédéclaration portal. `[SECONDARY]` (CNAS) [8][26]
- Practical deadline: **30 January** of the following year (30 days after 31 December). `[SECONDARY]` — if the 30th falls on a weekend/holiday, confirm the shift with CNAS; `UNVERIFIED`.
- SIRH: DAS is per-employee, per-quarter; it is not the same as the monthly DAC. Keep both.

### 7.5 IRG — monthly declaration G50

- **G50** is the monthly tax declaration (série G No. 50) covering **IRG withheld on salaries**, VAT, IBS instalments, stamp duty, etc. `[SECONDARY]` (DGI calendar; tax practitioners) [19]
- **Deadline:** filing and payment **from the 1st to the 20th of the month following** the operations month. Example: October salaries → G50 filed/paid 1–20 November. `[SECONDARY]` (DGI official tax calendar) [19]
- Filing is available via **Jibaya'tic / Moussahama'tic** (DGI portals). `[SECONDARY]` (DGI) [19]
- **Electronic filing:** the DGI has been pushing online filing; the 2026 calendar shows monthly withholding payment windows. `[SECONDARY]` [19] — `UNVERIFIED` whether paper filing is still accepted for all taxpayers in 2026.
- **Penalty for late payment:** a 10% penalty is commonly cited; `[SECONDARY]`/`UNVERIFIED` exact rate and base. Do not compute penalties in the SIRH; show a warning and link to the DGI.
- SIRH: produce a G50 pre-fill extract: taxable base, IRG withheld, employer/employee contributions, exempt items. Keep the filed receipt.

### 7.6 ANEM — employment declarations

- **Legal basis:** **loi 04-19 du 25 décembre 2004 relative au placement des travailleurs et au contrôle de l'emploi**, and **décret exécutif 09-94 du 22 février 2009**. `[LAW]` [15][14]
- **Employer obligations:** `[DECREE]` (Décret 09-94, arts. 2–3) [14]
  - transmit to the **wilaya employment agency (ANEM)** information on **manpower needs**:
    - **quarterly**, at the latest **one month before** the quarter concerned;
  - inform ANEM of **all recruitments performed**:
    - **monthly**, at the latest **10 days after the end of the month concerned**.
- **Modification:** inform the ANEM wilaya agency **immediately** of any change to the information and the reasons. `[DECREE]` (Décret 09-94, art. 4) [14]
- **Content:** branch of activity, socio-professional categories, age, nature and number of posts, type of contract, employer information; for recruitments also gender. `[DECREE]` (Décret 09-94, arts. 5–6) [14]
- **Forms:** models fixed by ministerial arrêté. `[DECREE]` (Décret 09-94, art. 7) [14]
- ⚠️ Vendor content claims an "8-day declaration of recruitment" and a "declaration of vacant post before recruitment". The **verified** rule is the **monthly within 10 days after month-end** declaration of recruitments and the **quarterly forecast one month before the quarter**. Use the decree, not the vendor claim. `[DECREE]` [14]
- **State-aided schemes** (DAIP, CNAC, etc.) may add specific declarations; out of scope here. `[PRACTICE]`

### 7.7 Labour inspection registers

- **No statutory "registre d'employeur"** was found in loi 90-11 or loi 90-03. `[LAW]` (absence) [1] — the term is used by inspectors/vendors as a checklist, not as a named statutory register. `UNVERIFIED` legal basis.
- What **is** statutory:
  - **Payslip (fiche de paie)** per employee, itemised. `[LAW]` (Loi 90-11, art. 86) [1]
  - **Règlement intérieur** deposited with the labour inspectorate (8 days). `[LAW]` (Loi 90-11, art. 79) [1]
  - **Hygiene/safety registers and documents** that the employer must present to the labour inspector on request. `[LAW]` (Loi 88-07, art. 32) [11]
  - **Medical registers** kept by the occupational physician: individual medical file, individual visit sheet, daily activity/visits register, exposed-posts register, vaccination register, occupational-disease register, workshop-visit register. `[DECREE]` (Décret 93-120) [12]
- SIRH recommendation: provide a **"registre du personnel"** and a **"registre de paie"** as *product* registers (useful for inspection and CNAS control), clearly labelled as management tools, not as a named statutory obligation. `[PRACTICE]`

### 7.8 Workplace accident declaration (AT/MP)

- The employer must declare **any workplace accident within 48 hours of becoming aware of it**. `[SECONDARY]` (CNAS, Employeur) [8]
- This is a **CNAS** declaration; the employee/beneficiaries also have duties. `[SECONDARY]` [8]
- The 48-hour clock is a **hard alert**. SIRH must allow declaration by:
  - employee/manager incident report;
  - HSE validation;
  - CNAS form generation;
  - proof of deposit (receipt/acknowledgement);
  - link to the medical certificate and the occupational-disease file.
- `UNVERIFIED`: whether a separate declaration to the labour inspectorate is required within the same 48 hours. Loi 83-13 was not re-read; do not assert it.

### 7.9 Occupational medicine visits

- **Pre-employment visit (visite d'embauchage):** mandatory for every worker and apprentice; full clinical exam and appropriate para-clinical exams; verifies fitness for the envisaged post and proposes adaptations. `[DECREE]` (Décret 93-120, §"Prérogatives du médecin du travail") [12]; `[LAW]` (Loi 88-07, art. 17) [11]
- **Periodic visit:** at least **once per year** for all workers; **at least twice per year** for workers required to undergo reinforced surveillance (the decree lists exposed workers, safety-critical posts, under-18, over-55, catering staff, disabled/chronic patients, pregnant women and mothers of a child under 2). `[DECREE]` (Décret 93-120) [12]
- **Return-to-work visit (visite de reprise):** after occupational disease or work accident, maternity leave, **21 days or more** of non-occupational illness/accident, and repeated non-occupational absences. The employer must inform the occupational physician **before** the return. `[DECREE]` (Décret 93-120) [12]
- **Reassignment:** any change of post requires a new medical visit to confirm fitness. `[DECREE]` (Décret 93-120) [12]
- **Time spent on medical exams counts as working time.** `[DECREE]` (Décret 93-120) [12]
- **Confidentiality:** medical data is held by the occupational physician (individual medical file), not by HR. HR should only receive **fitness/inaptitude/adaptation** conclusions, not diagnoses. `[DECREE]` (Décret 93-120) [12] + `[LAW]` (Loi 18-07, art. 18 sensitive data) [17]
- **Employer obligation to organise the service:** create an in-house service, join an inter-company service, or contract with a health structure/authorised physician. `[LAW]` (Loi 88-07, arts. 13–14) [11]

### 7.10 Declaration calendar (default SIRH rules)

| Declaration | Trigger | Deadline | Source |
|---|---|---|---|
| Employer CNAS affiliation | First employee | **D+10** after first hire | [8] |
| Employee CNAS affiliation (DEA) | Each hire | **D+10** after hire | [8] |
| DAC (contributions) | Month/quarter end | **+30 days** (monthly if >10 employees; quarterly if <10) | [8] |
| DAS (annual salaries/employees) | 31 December | **+30 days** (≈30 January) | [8] |
| G50 (IRG + other taxes) | Month end | **1st–20th** of following month | [19] |
| ANEM recruitment declaration | Month end | **+10 days** after month end | [14] |
| ANEM manpower forecast | Quarter | **1 month before** quarter | [14] |
| Workplace accident | Employer's knowledge | **+48 hours** | [8] |
| Occupational medicine — pre-employment | Before/at hiring | Before taking up the post | [12] |
| Occupational medicine — periodic | Calendar | **12 months** (6 months for reinforced categories) | [12] |
| Return-to-work visit | Resume after AT/MP, maternity, ≥21 days sick | Before return | [12] |
| Règlement intérieur deposit | Adoption | **+8 days** | [1] |
| CDD expiry | Contract end | Alert J-60/J-30 | product rule |
| Trial end | Contract start + trial | Alert J-15 | product rule |

---

## 8. Records and retention

### 8.1 What must be kept

- **Payslips (fiches de paie)** per employee, itemised, with all remuneration elements. `[LAW]` (Loi 90-11, art. 86) [1]
- **Employment contracts**, CDD motive/duration, trial clauses, amendments. `[LAW]` (Loi 90-11, arts. 11–12) [1]
- **Règlement intérieur** and proof of deposit/publicity. `[LAW]` (Loi 90-11, art. 79) [1]
- **Hygiene/safety registers and documents** presented to the labour inspector. `[LAW]` (Loi 88-07, art. 32) [11]
- **Occupational-medicine records** (kept by the physician): individual medical file, visit sheet, registers. `[DECREE]` (Décret 93-120) [12]
- **CNAS declarations and receipts**: affiliation, DAC, DAS, accident declarations, attestations. `[SECONDARY]` (CNAS) [8]
- **ANEM declarations** and proofs. `[DECREE]` (Décret 09-94) [14]
- **G50 returns and payment receipts.** `[SECONDARY]` (DGI) [19]
- **Disciplinary file**: notification, hearing minutes, decision, proof of delivery. `[LAW]` (Loi 90-11, art. 73-2) [1]
- **Payroll journals, general ledger, bank proofs.** `[SECONDARY]` (accounting practice) [22]

### 8.2 Retention periods

- **Accounting books and supporting documents:** **10 years** under **article 12 of the Code de commerce**. `[SECONDARY]` (Code de commerce, art. 12, as cited by Algerian practitioners) [22] — the article number is consistent across secondary sources but the Code itself was not re-read; treat as `[SECONDARY]`.
- **Payroll records:** payroll is an accounting supporting document → align with the **10-year** accounting retention. `[SECONDARY]`/`[PRACTICE]` [22]
- **CNAS control:** CNAS may control **any period of affiliation** ("toutes les périodes d'assujettissement") and require documents. `[SECONDARY]` (CNAS control page) [8] → practical consequence: **do not purge social-security records at 10 years** if the employee's career/benefits may still be challenged. Keep at least **10 years after departure**, preferably **indefinitely** for pension-relevant data. `[PRACTICE]`
- **Personnel register:** commonly stated as **10 years after the employee leaves**. `[PRACTICE]`/`UNVERIFIED` statutory basis.
- **Medical records:** retention is a medical-professional rule, not an HR rule. Keep the **individual medical file** with the occupational physician; HR keeps only fitness conclusions and visit dates. `[DECREE]` (Décret 93-120) [12] + `[PRACTICE]`
- **Data-protection retention:** personal data must not be kept longer than necessary for the purpose. `[LAW]` (Loi 18-07, art. 9(e), as amended) [17] → retention must be **purpose-based** and documented; "keep everything forever" is a compliance risk.

### 8.3 Paper vs electronic / legal value

- **Electronic signature and certification** are governed by **loi 15-04** (cited in the preamble of loi 18-07). `[LAW]` (Loi 18-07 preamble; Loi 15-04) [17][23]
- A payroll record or contract stored electronically should be:
  - **readable and reproducible** over the retention period;
  - **integrity-protected** (hash, WORM/immutable storage, or qualified e-signature);
  - **traceable** (who created/modified, when, from where);
  - **available** to inspectors/CNAS/auditors in a legible format.
- `UNVERIFIED`: whether a labour inspector must be given **paper** payslips in 2026, or whether a signed electronic version is accepted in all wilayas. Product rule: generate a **PDF/A** version and keep the original; allow export/print on demand. `[PRACTICE]`
- **E-archiving** must also satisfy loi 18-07 security and confidentiality duties (art. 38). `[LAW]` [17]

### 8.4 Payroll record legal value

- The payslip is **mandatory** and must itemise the remuneration. `[LAW]` (Loi 90-11, art. 86) [1]
- The law does not expressly state the **probative value** of a payslip or of an electronic payroll record. `[LAW]` (absence) [1]
- Practical rule: the payslip is the employee's primary evidence of remuneration; a signed/acknowledged payslip or an electronically certified record with audit trail is stronger. `[PRACTICE]`
- Keep the **calculation basis** (hours, rates, contributions, IRG) alongside the payslip, not just the PDF.

---

## 9. Data protection (loi 18-07, as amended by loi 25-11)

### 9.1 Framework

- **Loi 18-07 du 10 juin 2018 relative à la protection des personnes physiques dans le traitement des données à caractère personnel**, **modified and supplemented by loi 25-11 du 24 juillet 2025**. `[LAW]` (ANPDP consolidated text) [17]
- Regulator: **Autorité nationale de protection des données à caractère personnel (ANPDP)**. `[LAW]` (Loi 18-07, art. 22) [17]; portal: [18]

### 9.2 Legal basis for employee data

- Processing requires the **explicit consent** of the data subject, **unless** it is necessary for: `[LAW]` (Loi 18-07, art. 7) [17]
  - compliance with a legal obligation to which the subject or controller is subject;
  - protection of the subject's life;
  - performance of a contract to which the subject is a party, or pre-contractual steps at their request;
  - vital interests;
  - a public-interest mission or public authority;
  - the controller's legitimate interest, respecting the subject's rights.
- **HR consequence:** do **not** rely on blanket employee consent for payroll, CNAS, tax or attendance. Use **legal obligation** and **contract**. Consent is appropriate only for optional processing (e.g. optional benefits, photos, some wellness features). Subordination makes "free" consent fragile.
- **Transparency:** the subject must be informed in advance, clearly, of the controller's identity, purposes, recipients, mandatory nature of responses, consequences, rights, and any transfer abroad. `[LAW]` (Loi 18-07, art. 32) [17]

### 9.3 Sensitive data (health, biometrics, etc.)

- Processing of **sensitive data is prohibited**, except for public-interest reasons, with **explicit consent**, or where a **legal text** or **ANPDP authorisation** allows it. `[LAW]` (Loi 18-07, art. 18) [17]
- Sensitive data includes health data, biometric data, and other categories listed in the law. `[LAW]` (art. 18) [17]
- **HR consequence:** occupational-medicine data, sickness certificates, disability data, biometric attendance/fingerprint/face templates, and union membership are **sensitive or high-risk**. They need:
  - a documented legal basis;
  - **ANPDP authorisation** where required;
  - strict access control;
  - minimisation (HR should not see diagnoses);
  - a **DPIA** (see below).

### 9.4 Prior declaration / authorisation

- Every processing operation is subject to **prior declaration** to ANPDP or **authorisation** by ANPDP, unless a legal exception applies. `[LAW]` (Loi 18-07, art. 12) [17]
- Declaration content is specified in art. 14; simplified declaration exists for certain categories. `[LAW]` (arts. 13–16) [17]
- **Authorisation** is required in particular for:
  - sensitive data (art. 18);
  - file interconnection;
  - transfers abroad (art. 45 bis 13). `[LAW]` [17]
- **ANPDP portal** for declarations/authorisations: `https://portail.anpdp.dz/`. `[SECONDARY]` (ANPDP) [18]

### 9.5 DPO (délégué à la protection des données)

- Since loi 25-11, **every data controller and competent authority must appoint a DPO**, chosen for professional qualities and specialised knowledge of data-protection law/practice. `[LAW]` (Loi 18-07, art. 41 bis, inserted by loi 25-11) [17]
- A **single DPO may be shared** across several controllers/authorities, depending on organisational structure and size. `[LAW]` (art. 41 bis) [17]
- The controller must **notify ANPDP of the DPO's contact details**. `[LAW]` (art. 41 bis) [17]
- DPO tasks: inform/advise, monitor compliance, advise on DPIA, act as ANPDP contact. `[LAW]` (art. 41 bis 1) [17]
- Courts are exempt when performing judicial functions. `[LAW]` (art. 41 bis) [17]

### 9.6 DPIA (analyse d'impact)

- A **DPIA** is required for processing likely to present **high risk** to rights and freedoms, taking into account nature, scope, context and purposes. `[LAW]` (Loi 18-07, art. 45 bis 6, inserted by loi 25-11) [17]
- The DPIA must describe the processing, assess risks, list safeguards/security measures and evidence of compliance. `[LAW]` (art. 45 bis 6) [17]
- **HR use cases that likely need a DPIA:** biometric attendance, geolocation of field staff, video surveillance, health/occupational-medicine data, whistleblowing, AI-based performance scoring, cross-border HR SaaS.

### 9.7 Breach notification

- In case of a **personal-data breach**, the controller must notify **ANPDP within 5 days** of becoming aware. If late, the notification must explain the delay. `[LAW]` (Loi 18-07, art. 45 bis 8, inserted by loi 25-11) [17]
- The processor must notify the controller **immediately** on becoming aware. `[LAW]` (art. 45 bis 8) [17]
- Notification content: nature of the breach, likely consequences, measures taken/proposed. `[LAW]` (art. 45 bis 8) [17]
- If the breach is likely to create **high risk** for data subjects, the controller must also inform them in **simple, clear terms**, describing the consequences. `[LAW]` (art. 45 bis 10) [17]
- The controller must **document** every breach, its effects and remedial actions. `[LAW]` (art. 45 bis 9) [17]
- **SIRH requirement:** incident register, 5-day countdown, notification templates, evidence pack, DPO approval.

### 9.8 Cross-border transfer

- Transfer to a foreign country/international organisation requires an assessment of the **adequate level of protection** in the destination, considering human rights, legal framework, security measures, and the existence of an independent data-protection authority. `[LAW]` (Loi 18-07, art. 45 bis 13, inserted by loi 25-11) [17]
- If adequate protection is absent, transfer may still be authorised where necessary for: `[LAW]` (art. 45 bis 13) [17]
  - protection of the subject's vital interests or another person's;
  - protection of the subject's legitimate interests;
  - prevention of an imminent and serious threat to public security;
  - specific criminal-law purposes/rights of defence.
- **Onward transfer** of data received from abroad to another country/organisation requires the **prior consent of the sending authority/organisation**, unless impossible in time and necessary for essential State interests or to prevent a serious imminent threat; the sending authority must then be informed immediately. `[LAW]` (art. 45 bis 14) [17]
- ANPDP may be consulted before transfer. `[LAW]` (art. 45 bis 14) [17]
- **HR consequence:** hosting employee data outside Algeria (EU/US cloud, shared-services centre, global HR SaaS) is a **restricted transfer**. Map every sub-processor, country, data category and safeguard; obtain ANPDP authorisation where required. Do not assume EU adequacy is recognised by Algeria. `[LAW]` + `[PRACTICE]`

### 9.9 Data-subject rights

- **Information:** art. 32. `[LAW]` [17]
- **Access:** the subject may obtain confirmation, purposes, categories, recipients, and the data itself. `[LAW]` (art. 34) [17]
- **Rectification/erasure/closure:** free of charge; the controller must correct within **10 days** of notification; if refused or no response, the subject may apply to ANPDP. `[LAW]` (art. 35) [17]
- **Objection:** for legitimate reasons; absolute right to object to direct marketing. `[LAW]` (art. 36) [17]
- **SIRH:** employee self-service for access/rectification, with identity verification and audit; do not let a manager edit another employee's data without a request workflow.

### 9.10 Security and retention

- The controller/processor must implement appropriate **technical and organisational measures** against accidental or unlawful destruction, loss, alteration, unauthorised disclosure/access, especially for data sent over a network. `[LAW]` (Loi 18-07, art. 38; art. 45 bis 7) [17]
- Data must be kept in a form allowing identification **only for the time necessary** for the purposes; ANPDP may authorise longer retention for historical/statistical/scientific purposes. `[LAW]` (art. 9(e)) [17]
- **HR consequence:** define retention per data category (payroll, health, recruitment, CCTV, biometrics, timekeeping) and implement automated deletion/anonymisation with legal-hold exceptions.

---

## 10. SIRH implications

### 10.1 Core data model (minimum)

**Employer / establishment**
- `employer_id`, `legal_name_fr`, `legal_name_ar`, `NIF`, `NIS`, `CNAS_employer_number`, `CASNOS` (if applicable), `activity_code`, `address`, `wilaya`, `collective_agreement_id`, `ri_deposit_date`, `cnas_affiliation_date`.

**Employee**
- Identity: `employee_id`, `first_name_fr/ar`, `last_name_fr/ar`, `birth_date`, `birth_place`, `nationality`, `national_id`, `passport` (foreign), `photo`, `gender`, `marital_status`, `address`, `phone`, `email`, `emergency_contact`.
- Social: `cnas_number`, `social_security_number`, `mutuelle_id`, `bank_rib`, `family_members[]` (for allocations), `disability_flag` (sensitive), `religion_declared` (optional/voluntary, sensitive — only for holiday eligibility if the employee chooses).
- Employment: `hire_date`, `seniority_date`, `category`, `position`, `establishment`, `manager_id`, `contract_type`, `probation_start/end`, `notice_period_rule`, `collective_agreement_id`.
- Exit: `exit_date`, `exit_reason`, `notice_start/end`, `certificate_issued_at`, `cnas_cessation_declared_at`, `final_payroll_id`.

**Contract**
- `contract_id`, `type = CDI | CDD | APPRENTICESHIP | INTERIM`, `start_date`, `end_date`, `cdd_motive_code` (art. 12), `trial_duration_months`, `trial_end_date`, `weekly_hours`, `part_time_flag`, `night_work_flag`, `shift_flag`, `collective_agreement_id`, `signed_at`, `language`, `documents[]`.

**Time & attendance**
- `timesheet_id`, `employee_id`, `date`, `planned_hours`, `worked_hours`, `overtime_hours`, `night_hours`, `rest_day_work`, `holiday_work`, `absence_type`, `absence_reason`, `approved_by`, `source = MANUAL | CLOCK | BIOMETRIC | MOBILE`.

**Payroll**
- `payroll_period`, `employee_id`, `base_salary`, `allowances[]`, `overtime_amount`, `leave_indemnity`, `gross`, `cnas_employee`, `cnas_employer`, `irg_base`, `irg_withheld`, `net`, `payslip_document_id`, `payment_date`, `bank_file_id`.

**Leave**
- `leave_type`, `accrual_rule`, `balance`, `requested_days`, `approved_days`, `start/end`, `reference_period`, `carryover_days`, `justification_document_id`.

**Medical**
- `visit_type = PRE_EMPLOYMENT | PERIODIC | RETURN_TO_WORK | SPONTANEOUS | REASSIGNMENT`, `due_date`, `done_date`, `fit_status = FIT | FIT_WITH_ADAPTATION | TEMPORARILY_UNFIT | PERMANENTLY_UNFIT`, `restrictions` (no diagnosis), `physician_id`, `certificate_document_id`, `next_due_date`.

**Declarations**
- `declaration_type = CNAS_AFFILIATION | CNAS_DAC | CNAS_DAS | G50 | ANEM_RECRUITMENT | ANEM_FORECAST | WORK_ACCIDENT | RI_DEPOSIT`, `period`, `due_date`, `submitted_at`, `receipt_ref`, `status`, `amount`, `evidence_document_id`, `rejection_reason`.

### 10.2 State machines

**Employee lifecycle**
`PREBOARDING → ACTIVE_PROBATION → ACTIVE_CONFIRMED → SUSPENDED (sick/maternity/unpaid/disciplinary) → NOTICE → TERMINATED → ARCHIVED`

Rules:
- `ACTIVE_PROBATION → ACTIVE_CONFIRMED` automatic at `trial_end_date` **only if** a confirmation decision exists; otherwise alert HR. Do not auto-confirm silently (art. 19).
- `ACTIVE_PROBATION → TERMINATED` allowed **without notice/indemnity** (art. 20), but require a reason and audit.
- `ACTIVE_CONFIRMED → NOTICE` requires a valid `exit_reason` and, for dismissal, a **procedure checklist** (notification, hearing, assistance, minutes) (art. 73-2).
- `NOTICE → TERMINATED` only after notice end or payment in lieu; generate certificate and final payroll.
- `CDD ACTIVE → EXPIRED` at `end_date`; if renewal/extension is chosen, require a new motive and a reclassification-risk warning (art. 14).

**CDD lifecycle**
`DRAFT → ACTIVE → EXPIRING (J-60) → RENEWAL_PENDING | CONVERSION_PENDING | EXPIRED → ARCHIVED`

- Block `ACTIVE` without `cdd_motive_code` and `end_date` (art. 12).
- Flag any chain of CDDs/renewals as **requalification risk**; require HR/legal approval.

**Declaration lifecycle**
`DRAFT → VALIDATED → SUBMITTED → ACCEPTED | REJECTED → PAID → ARCHIVED`

- `SUBMITTED` requires `receipt_ref` and `evidence_document_id`.
- `REJECTED` reopens `DRAFT` with a reason and a new due date (do not lose the original submission).

**Medical visit lifecycle**
`DUE → SCHEDULED → DONE → FIT/UNFIT → NEXT_DUE_SET`

- Block return-to-work `ACTIVE` if a required return visit is `DUE`.
- Never expose diagnosis to the manager; only `fit_status` + restrictions.

### 10.3 Alerts (default thresholds)

| Alert | Trigger | Default | Severity |
|---|---|---|---|
| CDD expiry | `end_date` | J-60, J-30, J-7 | High |
| Trial end | `trial_end_date` | J-15, J-3 | High |
| CNAS affiliation missing | Hire date | J+1, J+5, J+10 | Critical |
| ANEM recruitment declaration | Month end | J+5, J+10 | High |
| DAC due | Period end | J+20, J+28, J+30 | Critical |
| DAS due | 31 Dec | J-30, J-10, J+30 | Critical |
| G50 due | Month end | Day 10, 15, 20 | Critical |
| Work accident 48h | Incident timestamp | H+12, H+24, H+36, H+48 | Critical |
| Medical visit due | `next_due_date` | J-30, J-7 | High |
| Return-to-work visit | Absence end | J-3 | High |
| Maternity end | `expected_end_date` | J-30, J-7 | Medium |
| RI deposit | RI adoption | J+8 | High |
| Data retention | `retention_end_date` | J-30 | Medium |
| DPO/ANPDP authorisation expiry | `expiry_date` | J-60 | Medium |

### 10.4 Documents the SIRH must generate

- CDI contract (bilingual template).
- CDD contract with **motive** and duration.
- Trial-period clause/addendum.
- Apprenticeship contract + APC registration/validation pack.
- Amendment (salary, post, hours, establishment).
- Payslip (itemised, French/Arabic).
- Annual leave request/approval; leave indemnity statement.
- Sick-leave declaration pack (employee certificate + CNAS form + employer attestation).
- Maternity leave notification + CNAS file.
- Exceptional leave notification (marriage, birth, death, circumcision).
- Disciplinary notification, hearing convocation, minutes, decision.
- Dismissal letter with procedure proof; resignation acknowledgement.
- **Certificat de travail** (art. 67).
- **Attestation de salaire** (CNAS).
- CNAS affiliation form; DAC; DAS export.
- G50 pre-fill extract.
- ANEM recruitment declaration; ANEM forecast.
- Workplace accident declaration (CNAS) + internal incident report.
- Occupational-medicine visit certificate/aptitude sheet (restricted).
- Règlement intérieur + deposit receipt.
- Data-protection notices, consent forms (optional processing), access/rectification request forms, breach notification template.

### 10.5 Permissions and audit

**Role separation**
- `PAYROLL_ADMIN`: payroll data, bank files, CNAS/DAS/G50 extracts. No medical data.
- `HR_ADMIN`: contracts, leave, discipline, declarations. No bank file approval.
- `HSE / OCCUPATIONAL_HEALTH`: medical visit scheduling and fitness status. No pay data.
- `MANAGER`: team attendance, leave approval, no salary/medical/discipline detail beyond their need.
- `DPO`: audit logs, DPIA, breach register, retention rules.
- `AUDITOR`: read-only, time-boxed, no exports without approval.

**Hard controls**
- **Medical data**: field-level encryption; separate table; access logged; HR sees only `fit_status` and `restrictions`. `[LAW]` (Loi 18-07, art. 18) [17]
- **Biometric data**: separate consent/authorisation, template protection, alternative clock-in method, deletion on exit. `[LAW]` (art. 18) [17]
- **Payroll changes**: maker-checker; no self-approval; immutable audit trail.
- **Declarations**: four-eyes before submission; receipt stored; no deletion of rejected submissions.
- **Retention**: legal hold overrides deletion; deletion jobs logged; DPO approval for exceptions.
- **Cross-border**: flag any data flow outside Algeria; require DPO/legal approval and ANPDP authorisation where needed. `[LAW]` (art. 45 bis 13) [17]
- **Breach**: one-click incident creation, 5-day countdown, notification evidence. `[LAW]` (art. 45 bis 8) [17]
- **Audit**: who viewed/changed which employee field, when, from where; export logs; failed-login monitoring.

### 10.6 Localisation / hosting

- Loi 18-07 applies to processing by entities established/operating in Algeria and to foreign controllers targeting Algerian data subjects. `[LAW]` (Loi 18-07, scope provisions) [17]
- Cross-border transfer rules apply to HR SaaS, shared services and offshore support. `[LAW]` (art. 45 bis 13) [17]
- Product rule: offer **in-Algeria hosting** as the default for payroll/medical data; make offshore hosting a **documented transfer** with ANPDP authorisation. `[PRACTICE]`/`[LAW]`

---

## Sources

All URLs retrieved **2026-11-07** unless otherwise stated.

1. **Loi n° 90-11 du 21 avril 1990 relative aux relations de travail, modifiée et complétée** — Ministère du Travail, de l'Emploi et de la Sécurité Sociale (full text, consolidated, with evolution notes). https://www.mtess.gov.dz/fr/loi-n-90-11-du-21-avril-1990-relative-aux-relations-de-travail-page-488-rectificatif/
2. **Journal Officiel n° 17 du 25 avril 1990** (loi 90-11, scanned original). https://www.joradp.dz/FTP/Jo-Francais/1990/F1990017.pdf
3. **Ordonnance n° 97-03 du 11 janvier 1997 fixant la durée légale du travail** — NATLEX record (40 h/week; abrogation of arts. 22–26 of loi 90-11). https://natlex.ilo.org/dyn/natlex2/r/natlex/fe/details?p3_isn=46293
4. **Loi n° 23-10 du 26 juin 2023 modifiant la loi n° 63-278** — Journal Officiel n° 43 du 2023 (Aïd el-Fitr and Aïd el-Adha = 3 days). https://www.joradp.dz/FTP/jo-francais/2023/F2023043.pdf
5. **Loi n° 63-278 du 26 juillet 1963 fixant la liste des fêtes légales** — as summarised in the MTESS "Législation du travail" page (fixed and religious holidays; Christian/Jewish holidays). https://www.mtess.gov.dz/fr/legislation-du-travail/
6. **Loi n° 18-12 du 2 juillet 2018** (Yennayer, 12 January) — cited in UNESCO, *4th consolidated report on multilingualism: Algeria* (official report), p. on Yennayer. https://www.unesco.org/sites/default/files/medias/files/2021/12/4th_consolidated_report_multilingualism_algeria.pdf
7. **Loi n° 25-08 du 19 juillet 2025 modifiant et complétant la loi n° 83-11 relative aux assurances sociales** — Journal Officiel n° 47 du 22 juillet 2025 (maternity 150 days, 100%, extensions). https://www.joradp.dz/FTP/jo-francais/2025/F2025047.pdf
8. **CNAS — Employeur** (affiliation 10 days; DAS 30 days; DAC 30 days; rates 34.5%; work accident 48 h; contribution base; control powers). https://cnas.dz/fr/employeur/
9. **CNAS — Assurance Maladie** (sick-leave daily indemnity 50% first 15 days, 100% from day 16/hospitalisation/long-term; declaration within 2 working days). https://cnas.dz/fr/assurance-maladie/
10. **CNAS — Assurance Maternité** (21 weeks / 150 days at 100%). https://cnas.dz/fr/assurance-maternite/
11. **Loi n° 88-07 du 26 janvier 1988 relative à l'hygiène, à la sécurité et à la médecine du travail** — MTESS full text (arts. 13–17, 23, 32). https://www.mtess.gov.dz/fr/loi-n-88-07-du-26-janvier-1988-relative-a-lhygiene-a-la-securite-et-a-la-medecine-du-travail/
12. **Décret exécutif n° 93-120 du 15 mai 1993 relatif à l'organisation de la médecine du travail** — reproduction (DOCX) of the JO text; pre-employment, annual/semi-annual periodic visits, return-to-work after 21 days, medical registers. https://staff.univ-batna2.dz/sites/default/files/benhassine-wissal/files/decret_executif_ndeg_93-120_du_15_mai_1993_relatif_a_lorganisation_de_la_medecine_du_travail_reference_jora_ndeg_33_1991.docx
13. **Loi n° 81-07 du 27 juin 1981 relative à l'apprentissage** — NATLEX full text (arts. 4, 9–12, 16, 20, 23–24). https://natlex.ilo.org/dyn/natlex2/natlex2/files/download/11049/DZA-11049.pdf
14. **Décret exécutif n° 09-94 du 22 février 2009** définissant la périodicité et les caractéristiques des informations et données statistiques transmises à l'ANEM — Journal Officiel n° 13 du 25 février 2009, arts. 2–9 (quarterly forecast; monthly recruitment within 10 days). https://www.joradp.dz/FTP/jo-francais/2009/F2009013.pdf
15. **Loi n° 04-19 du 25 décembre 2004 relative au placement des travailleurs et au contrôle de l'emploi** — MTESS employment legislation page. https://www.mtess.gov.dz/fr/legislation-et-reglementation-de-lemploi/
16. **Décret législatif n° 94-09 du 26 mai 1994 portant préservation de l'emploi et protection des salariés** — NATLEX (art. 20 contribution up-to-date; art. 22 three months' salary; art. 35 abrogation of loi 90-11 art. 72). https://natlex.ilo.org/dyn/natlex2/natlex2/files/download/38027/DZA-38027.pdf
17. **Loi n° 18-07 du 10 juin 2018 relative à la protection des personnes physiques dans le traitement des données à caractère personnel, modifiée et complétée par la loi n° 25-11 du 24 juillet 2025** — ANPDP consolidated Arabic text (arts. 7, 9, 12–18, 22, 32–36, 38, 41 bis, 45 bis 6–14). https://anpdp.dz/ar/storage/2025/08/18-07-Edited.pdf
18. **ANPDP — Autorité nationale de protection des données à caractère personnel** (declaration/authorisation portal, texts, guides). https://anpdp.dz/fr/conformite-avec-la-loi-n18-07/ and https://portail.anpdp.dz/
19. **Direction Générale des Impôts — calendrier fiscal** (monthly withholding payment/filing window 1–20 of the following month; Jibaya'tic/Moussahama'tic). https://www.mfdgi.gov.dz/
20. *(public sector — out of scope)* **APS — "Les horaires de travail dans les institutions et administrations publiques fixés"**, 16 February 2026. https://www.aps.dz/fr/algerie/societe/mlpa3n85-les-horaires-de-travail-dans-les-institutions-et-administrations-publiques-fixes
21. **Algerie360 — "Officiel : l'Algérie célébrera l'Aïd el-Fitr vendredi 20 mars 2026"**, 19 March 2026 (Commission nationale d'observation du croissant lunaire; official announcement). https://www.algerie360.com/officiel-lalgerie-celebrera-laid-el-fitr-vendredi-20-mars-2026/ — see also Radio Algérie tag page: https://news.radioalgerie.dz/fr/blog/tags/commission-nationale-dobservation-du-croissant-lunaire
22. **Code de commerce algérien — article 12 (10-year retention of accounting books and supporting documents)** — Ministère du Commerce, recueil du Code de commerce; article number cross-checked in Algerian practitioner sources. https://www.commerce.gov.dz/fr/reglementation/recueil/code-commerce
23. **Loi n° 15-04 du 1er février 2015 fixant les règles générales relatives à la signature et à la certification électroniques** — cited in the preamble of loi 18-07 (source [17]).
24. **MTESS — "Législation du travail"** (synthesis: 40 h, 12 h amplitude, night 21h–5h, Friday rest, 2.5 days/month, 14 weeks maternity [pre-2025], 3 days exceptional leave, holiday list, labour-court conciliation deadlines). https://www.mtess.gov.dz/fr/legislation-du-travail/
25. **MTESS — "Législation et réglementation de l'emploi"** (loi 04-19; décret 09-94; foreign-worker texts: loi 81-10, décret 82-510). https://www.mtess.gov.dz/fr/legislation-et-reglementation-de-lemploi/
26. **CNAS — Télédéclaration** (online DAC/DAS/affiliation portal). https://teledeclaration.cnas.dz/
27. **CNAS — Nos services numériques** (attestation de salaires déclarés; online verification). https://cnas.dz/fr/nos-services-numeriques/

---

## Open questions / UNVERIFIED

The following items are **not** safe to hard-code. Each needs a primary-text check or counsel confirmation.

1. **CDD maximum duration and renewal cap.** Loi 90-11 sets no maximum and no renewal limit; only the motive and written duration. Any "3 years/one renewal" rule is not in the law. Confirm whether a sectoral collective agreement applies. `UNVERIFIED`.
2. **Notice periods (resignation and dismissal).** Loi 90-11 refers to collective agreements (arts. 68 and 73-5). No statutory minimum duration. Common 1 month/3 months is practice. `UNVERIFIED` absent a collective agreement.
3. **CNAS cessation declaration deadline.** Affiliation is 10 days; the exit/cessation deadline is not stated on the CNAS page reviewed and was not confirmed in loi 83-14. `UNVERIFIED`.
4. **"Registre d'employeur" legal basis.** No such named statutory register found in loi 90-11/loi 90-03. Payslips, RI, H&S registers and medical registers are statutory; a "registre du personnel/registre de paie" is a management/inspection tool. `UNVERIFIED`.
5. **Annual-leave carry-over and payment on exit.** Loi 90-11 is silent on carry-over and on the exit calculation. The art. 52 one-twelfth formula is the only statutory basis. `UNVERIFIED`.
6. **Sick-leave maximum duration and employer top-up.** CNAS rates are clear (50%/100%); the maximum duration and any employer complement are not in loi 90-11. `UNVERIFIED`.
7. **Language of the employment contract.** No language clause in loi 90-11; Arabic is the official language. Whether a private-sector contract must be in Arabic is `UNVERIFIED`.
8. **Temporary work / intérim regime.** No general statutory contract type in loi 90-11; private placement is regulated by loi 04-19. Whether a separate ETT regime exists is `UNVERIFIED`.
9. **Time limit to bring a labour claim.** Not found in the reviewed texts. `UNVERIFIED`.
10. **Holiday falling on the weekly rest day.** No statutory substitution rule found. `UNVERIFIED`; make it policy-configurable.
11. **Ramadan hours in the private sector.** The 2026 APS communiqué covers public institutions only. No general private-sector statutory reduction found. `UNVERIFIED`/`PRACTICE`.
12. **DAS exact practical date.** 30 days after 31 December = 30 January; whether weekends/holidays shift the deadline is `UNVERIFIED`.
13. **Employee-file retention.** 10 years is commonly stated, and accounting records are 10 years (Code de commerce art. 12, secondary), but there is no labour-law article fixing a personnel-file retention period. CNAS can control "any period of affiliation". `UNVERIFIED`.
14. **Loi 25-11 entry into force / transitional rules.** The consolidated ANPDP text is dated 2025; the exact entry-into-force and any grace period for existing processing were not confirmed. `UNVERIFIED`.
15. **Aïd 3-day application details.** Loi 23-10 sets 3 days for both Aïd; how the 3 days map to the actual holiday (e.g. day of Aïd + two following days) is `UNVERIFIED`; confirm with the annual official holiday communiqué.
16. **Article 18 trial-period wording.** The MTESS consolidated text prints "dix (06) mois" — read as six months, but the rectificatif at JO p. 488 should be checked. `UNVERIFIED` wording.
17. **Occupational-medicine visit frequency for "reinforced" categories.** The decree says "at least twice per year" for a list of categories, but the sentence is garbled in the reproduction. Confirm the exact list and frequency against the JO n° 33/1993. `[DECREE]` substance, `UNVERIFIED` details.
18. **CNAS contribution rate split.** The current CNAS page says 34.5% = 25% employer + 9% employee + 0.5% social works. Older sources say 26% + 9%. Make rates effective-dated and verify with the current DAC/finance law. `[SECONDARY]`.
