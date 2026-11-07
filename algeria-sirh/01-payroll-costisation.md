# Algérie — Paie & costisation / Algeria Payroll & Costing

**Document type:** research input for a SIRH (HRIS) product spec  
**Target regime:** rules in force for calendar year **2026** (with 2024–2026 changes flagged)  
**Retrieval date for every source:** **2026-11-07**  
**Currency:** Algerian dinar (DZD / DA). All amounts monthly unless stated.

---

## Scope

This file covers the **private-sector salaried regime** in Algeria:

- legal framework and minimum wage (SNMG);
- the gross-to-net engine (pay elements, taxable/cotisable treatment, overtime, absences, advances);
- IRG withholding (barème, abattements, declarations);
- CNAS contributions and declarations;
- CASNOS for non-salaried persons (needed because the SIRH will hold gérants, auto-entrepreneurs, consultants);
- other payroll-borne levies (TAP status, TFPC, TAPP, CNAC);
- full employer costisation, cost per hour, cost of a raise, cost of overtime;
- payslip obligations;
- the declarations calendar;
- what an Algerian payroll module must implement.

**Private sector only:** this pack applies to private-sector salaried employment
under loi 90-11. Public-sector pay grids and statutory regimes are out of scope.

**Out of scope:** public-sector statutory pay grids (fonction publique, ordonnance 06-03), mining/hydrocarbon-specific regimes, expatriate tax treaties in detail, and sectoral conventions collectives (only their *mechanism* is described).

---

## How to read confidence tags

Every figure below carries a tag. No figure is invented: when a value could not be confirmed, it is written `UNVERIFIED` with an explanation.

| Tag | Meaning | Examples |
|---|---|---|
| **[OFF]** | Official: law, ordinance, decree, Journal Officiel (JORADP), or a page published by the administrating body (DGI, CNAS, CASNOS, MTESS). | Loi 90-11; décret 26-01; DGI IRG page |
| **[REP]** | Reputable interpretation by a recognised third party (CLEISS, ILO, ISSA, Big-4, Business France, specialised Algerian payroll firms). Consistent with official text but not itself the text. | CLEISS rate table; KPMG LF note |
| **[PRAC]** | Common market practice. No legal text fixes it; it varies by company, sector and collective agreement. | 1–3 month notice periods; transport allowance treatment |
| **[UNVERIFIED]** | A number that circulates but could not be tied to a source of sufficient authority. Do not implement without confirmation. | CASNOS 2026 transitional base; 1/5 advance cap |

Two distinct concepts must never be merged:

- **Assiette CNAS** (social contribution base) — defined by ordonnance 95-01 and décret 96-208.
- **Assiette IRG** (tax base) — defined by CIDTA arts. 69–73.

An allowance can be **excluded from CNAS and still taxable at IRG**, or the reverse. The SIRH must store two independent flags per pay element.

---

## 0. 2026 snapshot (the numbers an engine needs on day one)

| Item | Value 2026 | Legal basis / effective date | Src | Conf. |
|---|---|---|---|---|
| SNMG (salaire national minimum garanti) | **24 000 DA/month** | Décret présidentiel n° 26-01 of 7 Jan 2026, effective **1 Jan 2026** | S1 | OFF |
| SNMG hourly | **138,46 DA/h** | Same decree; 40 h/week = **173,33 h/month** | S1 | OFF |
| Legal working week | **40 h**, min. 5 days | Ordonnance 97-03 of 11 Jan 1997, art. 2 (repeals art. 22–26 of loi 90-11) | S12, S13 | OFF |
| Max overtime | **20 % of legal duration** → 8 h/week (≈34,67 h/month) | Loi 90-11 art. 31 | S12 | OFF |
| Overtime minimum premium | **+50 %** of normal hourly wage | Loi 90-11 art. 32 | S12 | OFF |
| Night work window | **21:00–05:00** | Loi 90-11 art. 27 | S12 | OFF |
| CNAS total | **34,5 %** = 25 % employer + 9 % employee + 0,5 % FNPOS | Décret exécutif 94-187 art. 2 as rewritten by décret 15-236 (JO 49/2015), unchanged in 2026 | S7, S9 | OFF |
| CNAS ceiling | **None** in the general regime | Ordonnance 95-01 art. 1 (no cap) | S19 | OFF |
| IRG monthly barème | 0 / 23 / 27 / 30 / 33 / 35 % | CIDTA art. 104 as rewritten by LF 2022 (loi 21-16), unchanged through LF 2026 | S2, S4, S6 | OFF |
| IRG exemption threshold | taxable salary **≤ 30 000 DA/month** | CIDTA art. 104-3 (LF 2022) | S2 | OFF |
| IRG abattement | **40 % of the tax**, floor 1 000, cap 1 500 DA/month | CIDTA art. 104-3 | S2 | OFF |
| TAP | **Abolished** since 1 Jan 2024 | LF 2024 arts. 14 and 24 | S14, S15 | OFF |
| TFPC (formation) | **1 %** of gross half-year payroll, employers ≥ 20 | CIDTA art. 196 bis as rewritten by LF 2026 art. 18 | S6 | OFF |
| TAPP (apprentissage/stages) | **1 %** of gross half-year payroll, all employers | Same article | S6 | OFF |
| CASNOS rate | **15 %** (7,5 % social insurance + 7,5 % retirement) | Décret exécutif 15-289 art. 14, rewritten by décret 26-257 (JO 53 of 23 Jul 2026) | S23 | REP |
| CASNOS base 2026 | min **288 000**, max **5 760 000** DA/year | 12 × SNMG and 20 × 12 × SNMG | S23 | REP |
| Paid leave | **2,5 days/month**, max **30 calendar days/year** | Loi 90-11 arts. 40–41 | S12 | OFF |

> **Answer to the SNMG question:** the 20 000 DA figure was **not** raised in 2024 or 2025. It stayed at 20 000 DA (décret 21-137) until **31 Dec 2025**, then moved to **24 000 DA** by décret 26-01, effective **1 Jan 2026** [S1, OFF]. Any 2024–2025 document quoting 20 000 is describing the earlier period.

---

## 1. Legal framework

### 1.1 Core texts

| Domain | Text | Notes |
|---|---|---|
| Employment relations | **Loi n° 90-11 du 21 avril 1990** relative aux relations de travail, modified (ord. 96-21 of 9 Jul 1996; ord. 97-02 of 11 Jan 1997) | Pay definition art. 81; payslip art. 86; payment art. 88; leave arts. 39–52; overtime arts. 31–32; dismissal art. 73 [S12, OFF] |
| Working time | **Ordonnance n° 97-03 du 11 janvier 1997** | 40 h/week; repeals arts. 22–26 of loi 90-11 [S12, S13, OFF] |
| Social insurance | **Loi 83-11** (assurances sociales), **83-12** (retraite), **83-13** (accidents du travail / maladies professionnelles), **83-14** (obligations des assujettis), **83-15** (contentieux) — all 2 Jul 1983, all modified | 83-14 is the text that creates DAS/DAC and their penalties [S18, S32, OFF] |
| Contribution base | **Ordonnance n° 95-01 du 21 janvier 1995**; **décret exécutif n° 96-208 du 5 juin 1996** | Defines inclusions/exclusions from the CNAS base [S19, OFF] |
| Contribution rates | **Décret exécutif n° 94-187 du 6 juillet 1994**, art. 2 rewritten by **décret exécutif n° 15-236 du 3 septembre 2015** | The 25 / 9 / 0,5 split [S7, S9, OFF] |
| Collective dismissals / unemployment | **Décret législatif n° 94-09 du 26 mai 1994** | Repealed art. 72 of loi 90-11; creates the 3-month indemnity for economic dismissal [S12, REP] |
| Minimum wage | **Décret présidentiel n° 26-01 du 7 janvier 2026** | 24 000 DA from 1 Jan 2026; abrogates décret 21-137 [S1, OFF] |
| Public holidays | **Loi n° 63-278 du 26 juillet 1963**, modified by lois 05-06, 18-12, 23-10 | 14 paid days in 2026; Aïd raised to 3 days each by loi 23-10 (2023) [S21, S22, OFF] |
| Tax | **CIDTA** (Code des impôts directs et taxes assimilées), arts. 66–75 (salaries), 104 (barème), 129 (payment), 196 bis–sexies (TFPC/TAPP) | Consolidated 2026 text [S5, OFF] |
| Finance laws | LF 2022 (loi 21-16), LF 2024, LF 2025, LF 2026 (loi 25-17 of 14 Dec 2025) | 2024–2026 changes below [S4, S6, S14] |
| Placement / ANEM | **Loi n° 04-19 du 25 décembre 2004**; **décret exécutif n° 09-94** | Vacancy notification and recruitment reporting [S20, REP] |
| Foreign workers | **Loi n° 81-10 du 11 juillet 1981**; décret 82-510 | Work permit is issued by the labour administration, **not** ANEM [S36, REP] |
| Experience allowance | **Décret n° 85-58 du 23 mars 1985** (IEP) | Historically public sector; private sector adopts it via collective agreement [S35, OFF/PRAC] |

### 1.2 What changed 2024–2026 (and when)

| Date | Change | Text | Impact on payroll |
|---|---|---|---|
| **1 Jan 2024** | **TAP abolished** (taxe sur l'activité professionnelle) | LF 2024 arts. 14 and 24; DGI circular | Remove TAP from cost models. Replaced by *taxe locale de solidarité* (TLS) only for hydrocarbon pipelines (3 %) and mining (1,5 %) [S14, S15, OFF] |
| 2024 | CASNOS: decree 24-49 introduces the real-income base and the **24 000 DA/year auto-entrepreneur flat option** | Décret 24-49 | Only affects non-salaried [S23, REP] |
| **1 Jan 2025** | IRG annual declaration (G n°1) deadline moved from 30 April to **30 June** | LF 2025 art. 7 (CIDTA art. 99) | Employee-side only; employer G29 stays 30 April [S2, OFF] |
| 2025 | G29 late-filing penalty raised / confirmed at **5 % of annual payroll** | LF 2024 art. 13; LF 2025 art. 16 | Employer risk [S2, OFF] |
| **1 Jan 2026** | **SNMG 24 000 DA** | Décret 26-01 | Raises the CNAS floor and the CASNOS base [S1, OFF] |
| **1 Jan 2026** | **TFPC and TAPP become half-yearly** (base = gross half-year payroll; deadlines 20 July and 20 January) | LF 2026 arts. 18–21 | Two declarations per year instead of one [S6, OFF] |
| **1 Jan 2026** | **NIN mandatory** on the G29 for every beneficiary | LF 2026 art. 8 | Requires NIN in the employee master data [S2, OFF] |
| **1 Jan 2026** | **Electronic filing mandatory** for réel / réel simplifié taxpayers connected to Jibaya'tic | LF 2026 art. 111; DGI communiqué | G50, G29 online [S27, S33, OFF] |
| **23 Jul 2026** | CASNOS base re-indexed on SNMG: **288 000 – 5 760 000 DA/year** | Décret 26-257 (JO 53/2026) | Non-salaried only; 2026 transitional treatment to confirm [S23, REP] |
| 2023–2026 | **No change to the IRG salary barème** | LF 2026 art. 11 marks salaries "sans changement" | 2022 barème still applies [S6, S2, OFF] |

### 1.3 Minimum wage (SNMG) — mechanics

- **Value:** 24 000 DA/month for 40 h/week, i.e. 173,33 h/month and **138,46 DA/h**, effective 1 Jan 2026 [S1, OFF].
- **Composition:** SNMG is not "base salary only". It includes base salary + allowances and bonuses of any kind, **excluding reimbursement of expenses** (loi 90-11 art. 87 bis as reproduced by MTESS) [S13, OFF].
- **Legal consequence:** an employer may not pay below SNMG; breach is an offence (loi 90-11 art. 149). The SNMG is also the **floor of the CNAS contribution base** [S13, S31, OFF].
- **Hourly reference:** 173,33 h/month is the divisor used by the decree itself; it is also the standard divisor for overtime and absence calculations [S1, PRAC].

> **SIRH note:** store SNMG as a dated parameter (2020-06-01 → 20 000; 2026-01-01 → 24 000), never as a constant. Every derived floor (CNAS minimum base, panier, CASNOS bounds) must recompute from it.

---

## 2. Gross-to-net engine

### 2.1 Pay elements recognised by law

Loi 90-11 art. 81 defines "salaire" as [S12, OFF]:

1. **salaire de base** — from the employer's job classification;
2. **indemnités** linked to seniority, overtime, or particular working conditions (poste, nuisance, astreinte, night work, **indemnité de zone**);
3. **primes** linked to productivity and results.

Art. 82 adds **revenu proportionnel aux résultats** (piecework, commission, output). Art. 83 distinguishes **remboursements de frais** (mission, personal vehicle for business, similar constraints) — these are not salary.

Practice adds: prime de rendement (individual/collective), prime d'ancienneté / **IEP** (indemnité d'expérience professionnelle), prime de panier, prime de transport, prime de poste, prime de nuisance, prime d'astreinte, indemnité de zone, indemnité de logement, avantages en nature [S13, PRAC].

### 2.2 Taxable vs non-taxable, cotisable vs non-cotisable

This is the single most dangerous table in Algerian payroll. It is a **two-axis** decision.

| Element | CNAS base | IRG base | Legal basis | Conf. |
|---|---|---|---|---|
| Salaire de base | **In** | **In** | Ord. 95-01 art. 1; CIDTA art. 69 | OFF |
| Prime de rendement / productivité (monthly) | **In** | **In** | Ord. 95-01 | OFF |
| IEP / prime d'ancienneté | **In** | **In** | Ord. 95-01; art. 81 | OFF |
| Heures supplémentaires | **In** | **In** | Ord. 95-01; art. 81 | OFF |
| Indemnité de poste / nuisance / astreinte | **In** | **In** | Art. 81 | OFF |
| **Indemnité de zone géographique** | In, subject to conditions | **Out** | CIDTA art. 68-1-f | OFF |
| **Indemnité de déplacement / mission** | **Out** | **Out** | Ord. 95-01; CIDTA art. 68-1-e | OFF |
| **Prime de panier** (genuine meal cost) | **Out** | **Out in practice** | Ord. 95-01 ("indemnités représentatives de frais") | OFF/PRAC |
| **Prime de transport** (flat monthly) | **Out** (representative of expense) | **Contested** — not listed in art. 68 | Ord. 95-01; CIDTA art. 68 | PRAC / see §2.3 |
| **Indemnités à caractère familial** (allocations familiales, salaire unique, maternité) | **Out** | **Out** | Ord. 95-01; CIDTA art. 68-1-g | OFF |
| **Indemnité de licenciement** | **Out** | **Out** | Ord. 95-01; CIDTA art. 68-1-m | OFF |
| **Indemnité de départ à la retraite** | **Out** | Out by analogy | Ord. 95-01 | OFF/REP |
| **Indemnités de résidence / isolement** | **Out** under 3 cumulative conditions | **Out up to 70 % of base salary** | Ord. 95-01; CIDTA art. 68-1-n | OFF |
| **Avantages en nature** (food, housing, clothing, heating, lighting) | **In** (valued) | **In** (valued) | CIDTA arts. 69–71 | OFF |
| Food benefit in kind | In | In, **min. 400 DA/meal** if unjustified | CIDTA art. 71 | OFF |
| Food + housing in "zones à promouvoir" | In? (not expressly excluded) | **Out** | CIDTA art. 72 | OFF |
| **Prime de fin d'année / gratification non mensuelle** | In | **10 % flat** as a separate monthly payment | CIDTA art. 67-4 + art. 104-3-b | OFF |
| Remboursement de frais réels (justified) | **Out** | **Out** | Ord. 95-01; art. 83 | OFF |

**Three structural rules** for the engine:

1. **CNAS base** = all salary elements **minus** family benefits, expense reimbursements, exceptional bonuses (dismissal, retirement), and residence/isolation allowances meeting the legal conditions [S19, OFF].
2. **IRG base** = gross taxable elements **minus** the employee's 9 % CNAS contribution **minus** pension/retirement contributions withheld by the employer [S2, OFF, CIDTA art. 73].
3. **SNMG test** uses base + all allowances/bonuses **except** expense reimbursements [S13, OFF].

### 2.3 The two genuinely ambiguous allowances

| Item | Problem | Practical rule used by most Algerian payrolls | Status |
|---|---|---|---|
| **Prime de transport** | Art. 68 does not list "transport" — only "frais de déplacement ou de mission". A flat monthly transport allowance is therefore, strictly, **taxable at IRG** even though it is excluded from CNAS as a reimbursement of expense. | Most employers treat it as **exempt from both**, on the theory that it reimburses a professional expense. Some payroll software taxes it. | **[PRAC] + UNVERIFIED** |
| **Prime de panier** | Same structure: excluded from CNAS as "indemnité représentative de frais", but not expressly exempted by CIDTA art. 68. | Treated as **exempt from both** when it genuinely compensates a meal taken on site (no canteen / compulsory presence). The commonly applied amount is **1,5 × hourly SNMG per day worked** (≈ **207,69 DA/day** at SNMG 24 000 → 138,46 × 1,5), prorated to days worked, **not paid during Ramadan** to Muslim staff on normal day shift, not cumulable with mission meal expenses. | **[PRAC] + UNVERIFIED** (amount derives from practice, not from décret 26-01) |

> **Do not hard-code these.** Expose them as per-company parameters with a documented legal opinion. A tax audit can reclassify a flat "transport" or "panier" allowance as salary.

### 2.4 Overtime

| Rule | Value | Basis | Conf. |
|---|---|---|---|
| Trigger | hours beyond **40 h/week** (or beyond the contractual/collective duration if lower) | Ord. 97-03 art. 2 | OFF |
| Cap | **20 %** of legal duration → **8 h/week**, ≈ 34,67 h/month | Loi 90-11 art. 31 | OFF |
| Exceptions to cap | imminent accident prevention / finishing works whose interruption would cause damage; staff representatives consulted, labour inspector informed | Loi 90-11 art. 31 al. 3 | OFF |
| Minimum premium | **+50 %** of normal hourly wage | Loi 90-11 art. 32 | OFF |
| Higher premiums | Only by **convention/accord collectif**. No statutory +100 % general rate. | Loi 90-11 art. 32 (floor, not ceiling) | OFF |
| Work on weekly rest day | Compensatory rest of equal duration **+** overtime premium | Loi 90-11 art. 36 | OFF |
| Public holiday worked | Day is paid; premium/compensation set by collective agreement | Loi 63-278; CCN | OFF/PRAC |
| Night premium | **None in the law**; set by CCN (night = 21:00–05:00) | Loi 90-11 art. 27 | OFF/PRAC |
| Daily amplitude | **12 h max** | Ord. 97-03 art. 7 | OFF |
| Base for the hourly rate | "salaire horaire normal" — practice uses **monthly reference salary ÷ 173,33**; some CCNs use base salary only | Loi 90-11 art. 32 + practice | PRAC |
| CNAS / IRG | Overtime is **cotisable and taxable**; it does **not** count toward reaching SNMG | Ord. 95-01; MTESS | OFF |

**Implementation rule:** compute `hourly = reference_monthly / 173.33`; pay `hours × hourly × (1 + m)` with `m ≥ 0.50`; then apply CNAS 9 % and IRG on the total.

### 2.5 Absences, advances, loans, fines

| Item | Rule | Conf. |
|---|---|---|
| **Unpaid absence** | No remuneration for time not worked unless law/regulation/CCN provides otherwise (loi 90-11 art. 53). Deduction is the **mirror of the pay element** (base + permanent allowances), prorated. | OFF |
| Daily rate | **No statutory divisor.** Practice: monthly / 30 for calendar-day absence, or / 173,33 for hourly absence. Must be consistent with the hiring/leave rules. | PRAC |
| **Acompte** (advance on work already done) | Employee may request an advance on the half-month already worked; it is salary paid early, therefore **fully cotisable and taxable in the month**. | PRAC |
| **Avance** (loan) | Employer's decision; a debt, **not** salary → no CNAS/IRG at disbursement; repayment is a net deduction. Written agreement recommended. | PRAC |
| Repayment cap | Circulating guides claim **1/5 of net salary under art. 85 loi 90-11**. The actual art. 85 says remuneration is expressed and paid in money only. **The citation is wrong; no statutory cap was located.** | **UNVERIFIED** |
| Salary protection | Remuneration is paid in preference to other debts (art. 89) and cannot be seized/withheld to the prejudice of workers (art. 90). | OFF |
| **Fines / disciplinary deductions** | No express prohibition located in loi 90-11, but disciplinary sanctions are listed in the règlement intérieur (art. 77) and are non-pecuniary in practice. A deduction must correspond to time not worked or a documented debt. **Treat fines as legally unsafe.** | **UNVERIFIED** |
| **Sick leave** | CNAS pays the indemnité journalière: **50 %** of daily reference wage for days 1–15, **100 % from day 16**; **100 % from day 1** for hospitalisation or long-term illness; max 3 years. Employer does **not** pay salary during the suspension unless the CCN provides a top-up. | OFF [S10, S11, S24] |
| **Maternity** | **98 days (14 weeks)**, paid by CNAS at 100 % of reference wage. | OFF [S11, S24] |
| **Work accident** | 100 % from day 1; employer declares to CNAS within **48 h**; day of accident paid by employer. | OFF [S8] |
| **Family events** | 3 paid working days (marriage, birth, marriage of descendant, death of ascendant/descendant/1st-degree collateral/spouse, circumcision); pilgrimage once in career. | OFF [S12, S13] |
| **Public holidays** | 14 paid days in 2026 (5 fixed civil + 9 religious/January). No automatic carry-over when a holiday falls on the weekend. | OFF [S21, S22] |

**Public holiday list (loi 63-278 as amended, 2026):** 1 Jan; 12 Jan (Yennayer); 1 May; 5 Jul; 1 Nov; Aïd el-Fitr **3 days**; Aïd el-Adha **3 days**; 1 Mouharram; Achoura; Mawlid. Christian and Jewish staff also get their own feasts under arts. 3–4 [S21, OFF].

> **Note:** the MTESS web page still shows Aïd at 2 days. **Loi 23-10 of 26 June 2023 raised each Aïd to 3 days** (JO 43/2023). The law prevails [S22, OFF].

### 2.6 Benefits in kind

- Valued at **real value**, apportioned to the pay period (month, fortnight, day, hour) [CIDTA art. 71, OFF].
- **Food:** minimum **400 DA per meal** if no justification [CIDTA art. 71, OFF]. This is a floor, not a flat rate.
- **Housing:** no statutory formula in the CIDTA beyond "real value"; practice uses rental value or a contractual valuation. **UNVERIFIED** for a single national method.
- **Vehicle:** only the **private use** is a benefit; a pool/service vehicle is not. No statutory scale → valuation by the employer, defensible on real cost. **PRAC/UNVERIFIED**.
- Benefits in kind are **cotisable** at CNAS (they are elements of salary) and **taxable** at IRG [S19, OFF].

---

## 3. IRG — impôt sur le revenu global (salaries)

### 3.1 The 2022 reform

LF 2022 (loi 21-16 of 30 Dec 2021, art. 31) rewrote **CIDTA art. 104** with effect from **1 January 2022**. It replaced the previous schedule with six brackets, introduced the **40 % abattement on the tax** (1 000–1 500 DA/month), kept the **30 000 DA/month exemption**, and added a smoothing formula for the 30 001–35 000 DA band [S2, S4, OFF]. **No later finance law changed the salary schedule through 2026** [S6, OFF].

### 3.2 Monthly barème (article 104 CIDTA)

| Monthly taxable slice (DA) | Annual equivalent (DA) | Rate | Tax on the slice (DA) | Cumulative tax (DA) |
|---|---|---|---|---|
| 0 – 20 000 | 0 – 240 000 | **0 %** | 0 | 0 |
| 20 001 – 40 000 | 240 001 – 480 000 | **23 %** | 4 600 | 4 600 |
| 40 001 – 80 000 | 480 001 – 960 000 | **27 %** | 10 800 | 15 400 |
| 80 001 – 160 000 | 960 001 – 1 920 000 | **30 %** | 24 000 | 39 400 |
| 160 001 – 320 000 | 1 920 001 – 3 840 000 | **33 %** | 52 800 | 92 200 |
| Above 320 000 | Above 3 840 000 | **35 %** | — | — |

Source: DGI, CIDTA art. 104 [S2, S3, OFF]. "Taxable" = gross **minus** employee CNAS 9 % and any pension contribution withheld (art. 73).

### 3.3 Computation order (must be implemented exactly in this order)

```
1. taxable = gross_taxable_elements
              − employee_CNAS (9 % of CNAS base)
              − employee_pension_withholding (if any)

2. if taxable ≤ 30 000:
        IRG = 0                                    # exonération totale
   else:
        tax = progressive_barème(taxable)          # table above
        abattement = clamp(0.40 × tax, 1 000, 1 500)
        IRG = max(0, tax − abattement)

3. if 30 000 < taxable < 35 000 (ordinary employee):
        IRG = IRG × (137/51) − (27 925/8)          # second abattement
        IRG = max(0, IRG)

4. if 30 000 < taxable < 42 500 (disabled worker or pensioner):
        IRG = IRG × (93/61) − (81 213/41)          # replaces, never cumulates
        IRG = max(0, IRG)
```

[S2, OFF]

### 3.4 The 40 % abattement — conditions

- It applies to **the tax**, not to the income.
- It is available to **all salary/pension/annuity recipients**, with no condition of family status.
- Floor **1 000 DA/month**, cap **1 500 DA/month** → annual floor 12 000, annual cap 18 000 [S2, OFF].
- Because of the cap, it is worth exactly 1 500 DA for any taxable income above ≈ 36 300 DA/month; for very low tax it is worth 1 000 DA and can wipe the tax out.

### 3.5 Family / children

**There is no family quotient and no per-child IRG reduction.** A "1 500 DA per child" figure circulates online and is **not** in the DGI barème. What is exempt is the **allocation familiale / salaire unique / allocation de maternité** themselves [S2, S37, OFF/REP]. The employer must still record the **number of dependants** on payroll records and on the G29/G1 (CIDTA art. 75-2), but it has **no effect on the monthly IRG**.

### 3.6 Exemptions and special rates

| Item | Treatment | Basis | Conf. |
|---|---|---|---|
| Taxable salary ≤ 30 000 DA/month | 0 % IRG | CIDTA art. 104-3 | OFF |
| Mission/travel allowances | exempt | art. 68-1-e | OFF |
| Geographic zone allowance | exempt | art. 68-1-f | OFF |
| Family allowances | exempt | art. 68-1-g | OFF |
| Work-accident benefits/annuities | exempt | art. 68-1-h | OFF |
| Unemployment benefits | exempt | art. 68-1-i | OFF |
| Dismissal indemnity | exempt | art. 68-1-m | OFF |
| Residence/isolation allowance | exempt up to **70 % of base salary** | art. 68-1-n | OFF |
| Non-monthly bonuses, gratuities, arrears | **10 % flat**, treated as a separate monthly payment, **no abattement** | art. 67-4 + art. 104-3-b | OFF |
| Occasional teaching/research/invigilation | 10 % final | art. 104-3-c | OFF |
| Other occasional intellectual work | 15 % final | art. 104-3-c | OFF |
| Foreign artists' fees/royalties | 15 % (exceptions) | art. 104-3-c | OFF |
| Young-employment programme wages | exempt | art. 68-1-c | OFF |

> **Architectural consequence:** a **non-monthly** bonus is **not** annualised through the barème. It is a separate payment taxed at **10 %**. A monthly bonus is inside the barème. The SIRH must classify each bonus as "monthly recurring" vs "exceptional/non-monthly" *before* computing.

### 3.7 Employer withholding and filing

| Obligation | Detail | Basis | Conf. |
|---|---|---|---|
| Monthly withholding | On **each payment**; the employer is the withholding agent | CIDTA art. 74–75 | OFF |
| Payment to Treasury | **1st–20th of the following month**; quarterly (1st–20th after quarter) for IFU / régime simplifié employers | CIDTA art. 129; DGI calendar | OFF |
| Monthly return | **G n°50** (série G 50) — includes IRG, VAT and other taxes; **G n°50 ter** quarterly for IFU/simplified IRG only | DGI | OFF |
| Annual salary return | **G n°29** — by **30 April** of N+1; per beneficiary: name, NIN, job, address, family situation, gross, net, IRG withheld; **NIN mandatory since 2026**; electronic filing mandatory where Jibaya'tic is deployed | CIDTA art. 75-3; LF 2026 art. 8 | OFF |
| G29 late / missing | Penalty **5 % of the annual payroll** | LF 2024 art. 13; LF 2025 art. 16 | OFF |
| G29 special deadlines | Cession/cessation: 10 days; death of employer: heirs within 6 months | CIDTA art. 132 | OFF |
| Payslip mention | IRG amount, or the exact wording **« retenue IRG – traitements et salaires : néant »** | CIDTA art. 75-2 | OFF |
| Record retention | Until the **end of the 4th year** following the withholding year (≈ 5 years) | CIDTA art. 75-2 | OFF |

### 3.8 Annual regularisation

- For an employee whose **only** income is salary, the monthly withholding is **definitive**; there is no annual IRG return and no refund exercise.
- If the employee has **other income**, they file **G n°1 by 30 June** (LF 2025 moved it from 30 April) and receive a **credit** for the IRG already withheld on the main salary [S2, OFF].
- The employer's G29 is **informational** for the tax administration; it does not generate a reassessment of each employee.
- **Practical consequence:** the SIRH does not need a year-end IRG "regularisation" engine, but it **does** need a reliable annual G29 extract and a per-employee cumulative IRG figure.

### 3.9 Known pitfall: the 30 001–35 000 band

The published smoothing formula produces a value at 35 000 DA that is **below** the ordinary barème + 40 % abattement result, so the tax appears to **jump** just above 35 000. Sources disagree on whether the band "rejoins" the normal barème at 35 000.

- **Do not implement the formula alone.** Implement the **official DGI monthly table** (TABLE_IRG_2022 / the 2026 calculette) as a lookup, and unit-test the boundaries 30 000 / 30 001 / 34 999 / 35 000 / 35 001.
- Flagged **UNVERIFIED** at the 35 000 boundary.

---

## 4. CNAS — salaried social security

### 4.1 Rates (unchanged since 1 Sep 2015, still in force 2026)

| Branch | Employer | Employee | FNPOS (œuvres sociales) | Total |
|---|---|---|---|---|
| Assurances sociales (maladie, maternité, invalidité, décès) | 11,50 % | 1,50 % | — | 13,00 % |
| Accidents du travail / maladies professionnelles | 1,25 % | — | — | 1,25 % |
| Retraite (CNR) | 11,00 % | 6,75 % | 0,50 % | 18,25 % |
| Retraite anticipée | 0,25 % | 0,25 % | — | 0,50 % |
| Assurance chômage (CNAC) | 1,00 % | 0,50 % | — | 1,50 % |
| **Total** | **25,00 %** | **9,00 %** | **0,50 %** | **34,50 %** |

Basis: décret exécutif 94-187 art. 2 as rewritten by **décret exécutif 15-236 of 3 Sep 2015** (JO 49/2015) [S7, S9, OFF]. The 0,50 % FNPOS is **employer-borne** and is not part of the employee's 9 %.

> **Recurring error:** many sites publish "26 % employer / 35 % total". That comes from allocating 12,5 % to health and 10,5 % to retirement, which double-counts. The official table sums to **25,0 / 9,0 / 0,5**. Use 25 % + 0,5 % = **25,5 % employer**.

### 4.2 Base, floor, ceiling

| Item | Rule | Basis | Conf. |
|---|---|---|---|
| Base | "Ensemble des éléments du salaire ou du revenu proportionnel aux résultats du travail" | Ord. 95-01 art. 1 | OFF |
| Excluded | family benefits; expense reimbursements (panier, transport, mission, tools, work clothing); exceptional bonuses (dismissal, retirement); residence/isolation allowances under 3 cumulative conditions | Ord. 95-01; décret 96-208 | OFF |
| Floor | Taxable salary may **not be below SNMG** → 24 000 DA in 2026 | CNAS | OFF |
| Ceiling | **None** in the general regime | Ord. 95-01 (no cap) | OFF |
| Special categories | Base may be fixed at SNMG | CNAS | OFF |
| Part-time | Prorated salary, but the SNMG floor logic must be checked (CNAS practice) | CNAS | PRAC |

> A "ceiling of 8 × SNMG" claim circulates on one aggregator. It contradicts ordonnance 95-01 and the CNAS page. Treat it as **UNVERIFIED / probably false**.

### 4.3 Special case: BTPH (construction, public works, hydraulics)

Employers in BTPH are affiliated to **CACOBATPH** for paid leave and bad-weather unemployment, **in addition to** CNAS:

| Contribution | Rate | Bearer |
|---|---|---|
| Congés payés (CACOBATPH) | **12,21 %** | Employer only |
| Chômage-intempéries (CACOBATPH) | **0,75 %** (0,375 % employer + 0,375 % employee) | Split |

[S17, S7, OFF]

**Cost consequence:** BTPH employer charge = 25 % + 0,5 % + 12,21 % + 0,375 % = **38,085 %** of the CNAS base, and the employer **does not provision** paid leave itself (CACOBATPH pays it). Outside BTPH, the employer provisions ≈ 8,33 % instead.

### 4.4 Affiliation and declarations

| Obligation | Deadline | Basis | Conf. |
|---|---|---|---|
| Employer activity declaration (first employee) | **10 days** after recruitment | Loi 83-14 art. 6 | OFF |
| Employee affiliation | **10 days** after hire | Loi 83-14 art. 10 | OFF |
| **DAC** (déclaration d'assiette des cotisations) — ≥ 10 employees | Monthly, within **30 days** of month end | CNAS télédéclaration guide; loi 83-14 art. 21 (text says 15 days) | OFF, see note |
| **DAC** — ≤ 9 employees | Quarterly, within **30 days** of quarter end | Same | OFF |
| **DAS** (déclaration annuelle des salaires et salariés) | **1–31 January** of N+1 (30 days after year end) | Loi 83-14 art. 14 | OFF |
| Work accident | **48 h** to CNAS (24 h to employer) | Loi 83-13 / CNAS | OFF |
| Payment of contributions | With the DAC | CNAS guide | OFF |
| DAS for BTPH (CACOBATPH) | Reference year **1 July – 30 June**, DAS by **31 July** | CACOBATPH | OFF |

> **Deadline ambiguity to flag:** loi 83-14 art. 21 says payment within **15 days** after the month/quarter; the CNAS télédéclaration guide and operational practice say **30 days**. The portal enforces 30 days. Implement 30 days, but keep the legal 15-day rule visible in the compliance notes.

### 4.5 Penalties

| Breach | Penalty | Basis | Conf. |
|---|---|---|---|
| DAS not filed / late | **15 % of contributions due + 5 % per month of delay** | Loi 83-14 art. 16 (as amended by loi 04-17 art. 11) | OFF |
| Employee omitted or salary misstated | **1 000 DA per worker and/or per inaccuracy** | Loi 83-14 art. 16 bis | OFF |
| Penalties unpaid 3 months after notification | Court action + fine **10 000–20 000 DA** | Loi 83-14 art. 41 | OFF |
| Repeat offence within 12 months | Penalties doubled | Loi 83-14 art. 42 bis | OFF |
| Late payment of contributions | Late-payment increases (taux fixed by regulation; commonly quoted 5 %/month) | Loi 83-14 | REP/UNVERIFIED |

> One press source quotes **2 %/month** instead of 5 %. The CACOBATPH and CNAS texts quote **5 %**. Use 5 % and flag.

### 4.6 DAC and DAS data content

**DAC** (monthly/quarterly): employer identifier, period, headcount, per-employee CNAS base, rates, employee/employer/FNPOS split, total to pay, payment mode.

**DAS** (annual): per employee — social security number, identity, employment period, **entry and exit dates**, time worked, **salary per quarter**, contributions. It is the source of the employee's retirement and benefit rights; an omitted DAS line creates a hole in the career record [S9, S18, OFF].

---

## 5. CASNOS — non-salaried persons

### 5.1 Who is covered

Traders, artisans, **professions libérales**, farmers, transporters, **gérants majoritaires de SARL**, and **auto-entrepreneurs** — anyone exercising a non-salaried activity for their own account [S23, S30, REP].

**Interaction with salaried status:** being salaried does **not** exempt from CASNOS if the person also carries a non-salaried activity. The two regimes coexist: CNAS on salary, CASNOS on the non-salary income. A gérant majoritaire who draws no salary is CASNOS-only; if he draws a salary and is not affiliated to CNAS as an employee, the qualification is fact-specific (risk of reclassification). **Flag for legal review per case.**

### 5.2 Rate and base (2026)

| Item | Rule | 2026 value |
|---|---|---|
| Rate | **15 %** of the annual base: 7,5 % assurances sociales + 7,5 % retraite | 15 % |
| Minimum base | Annual SNMG | **288 000 DA** |
| Maximum base | 20 × annual SNMG | **5 760 000 DA** |
| Minimum contribution | 15 % × 288 000 | **43 200 DA/year** |
| Maximum contribution | 15 % × 5 760 000 | **864 000 DA/year** |
| First year of activity | Base fixed at annual SNMG | 288 000 DA |
| Forfait regime | Base = 25 % of turnover (goods/production) or 35 % (services) | — |
| Auto-entrepreneur option | Flat **24 000 DA/year** instead of the 15 % computation | 24 000 DA |
| From 3rd year | Contribution cannot be below the average contribution of the same activity in the same wilaya (arrêtés not yet published) | Not quantifiable |

Basis: décret exécutif 15-289 art. 14 as rewritten by **décret exécutif 26-257 of 15 Jul 2026** (JO 53 of 23 Jul 2026) [S23, REP]. The decree applies **from 23 July 2026 without retroactivity**; the 2026 transitional computation (Jan–Jul at the old 216 000 / 4 320 000 base?) is **UNVERIFIED** — confirm with CASNOS.

> The older figures **216 000 / 4 320 000** and **32 400 / 648 000** that still appear on many sites (including CLEISS, 2024 edition) are computed on the pre-2020 SNMG. They are **obsolete for 2026**.

### 5.3 Declarations and payment

| Obligation | Deadline | Basis | Conf. |
|---|---|---|---|
| Activity declaration (= affiliation request) | **10 days** after start of activity | Loi 83-14 art. 6/10 | OFF |
| Late activity declaration | **5 000 DA + 20 %/month** | Loi 83-14 art. 7 | OFF |
| Declaration of contribution base | **Before 31 January** of the year | Décret 15-289 art. 14 | REP |
| Payment of annual contribution | **Before 30 June** (1 October for purely agricultural activity) | Décret 15-289 art. 15; décret 22-121 | REP |
| No declaration | Provisional contribution on previous year's base **+ 5 %** (definitively acquired) | Décret 26-257 | REP |

> A 2026 press piece quotes **28 February** as the declaration deadline. The decree text says 31 January. Implement **31 January** and flag the variant.

---

## 6. Other levies

### 6.1 TAP — abolished

**Taxe sur l'activité professionnelle is abolished for all taxpayers** by **LF 2024 arts. 14 and 24**, effective **1 January 2024**. The articles 217–231 and 357–364 of the CIDTA were repealed. In 2026 there is **no TAP to compute or declare** [S14, S15, S25, OFF].

It was replaced by the **taxe locale de solidarité (TLS)**, which applies **only** to:
- hydrocarbon pipeline transport: **3 %** of turnover excluding VAT;
- mining activities: **1,5 %**.

TLS is declared and paid on the **G50** (monthly or quarterly), not on payroll. It is irrelevant to a standard SIRH except as a company-level tax flag.

### 6.2 TFPC and TAPP — the two payroll-borne training taxes

| Parameter | 2026 regime | Basis |
|---|---|---|
| Nature | TFPC = taxe de formation professionnelle continue; TAPP = taxe d'apprentissage et de stages | CIDTA arts. 196 bis–sexies |
| Rate | **1 %** each of gross **half-year** payroll | Art. 196 bis (LF 2026 art. 18) |
| TFPC scope | Employers with **20 employees or more** | Art. 196 bis |
| TFPC exemption | Employers with **1–19 employees** — but **the declaration remains mandatory** | Art. 196 ter |
| TAPP scope | **All employers** (no small-employer exemption) | Art. 196 bis |
| Base | Gross remuneration **paid** during the half-year, **before** social contributions, pension and IRG | Art. 196 quater (LF 2026 art. 19) |
| Effective rate | `max(0 ; 1 % − actual training spend / gross half-year payroll)` | Art. 196 quinquies (LF 2026 art. 20) |
| Eligible TFPC spend | training, transport, accommodation, catering, insurance of trainees | Art. 196 quinquies |
| Eligible TAPP spend | apprenticeships, student internships, trainer bonuses, apprentice pre-salaries, supplies, work clothing, tools | Art. 196 quinquies |
| Declaration | **Semestrial**: S1 by **20 July**, S2 by **20 January N+1** | Art. 196 sexies (LF 2026 art. 21) |
| Zero declaration | Mandatory even when nothing is due | Art. 196 sexies |
| Former regime | Annual, by 20 February N+1, on annual payroll | Repealed for 2026 |

[S6, OFF; S28, S29, REP]

**Cost impact:** for a company with no training spend, the payroll-borne tax load is **2 % of gross payroll** on top of CNAS. If the company genuinely spends 1 % + 1 %, the taxes fall to zero — but it still files.

### 6.3 CNAC / unemployment

There is **no separate "participation CNAC" levy** on top of the CNAS table. CNAC is financed by the **1,5 % unemployment contribution** inside the 34,5 % (1 % employer + 0,5 % employee) [S7, OFF].

The employer has two additional CNAC-related obligations in an economic dismissal:
- pay the employee an indemnity of **3 months' salary** (calculated on the average gross of the last 12 months) at the moment of dismissal;
- the employee then accesses CNAC unemployment benefit.

Basis: décret législatif 94-09 arts. 22–23 [S12, REP].

CNAC also grants **employer contribution reductions** for hires of at least 6 months (rates and eligibility vary by scheme and year; **UNVERIFIED** for 2026 — do not implement without the current CNAC circular).

### 6.4 Levies that do **not** exist (avoid inventing them)

- No "taxe sur les salaires" separate from IRG.
- No "versement forfaitaire" on salaries (historic, abolished).
- No "taxe d'apprentissage" separate from TAPP.
- No "contribution au fonds de formation" separate from TFPC.
- No "cotisation patronale de 26 %" — the correct employer rate is 25 % + 0,5 % FNPOS.

---

## 7. Employer costisation

### 7.1 The formula

Let:

- `G` = gross remuneration (all cash elements paid);
- `A` = **CNAS base** (subset of `G`; excludes non-cotisable items);
- `N` = non-cotisable cash allowances (transport, panier, mission, family…);
- `s` = 0,255 (25 % + 0,5 % FNPOS), or 0,38085 in BTPH (25 % + 0,5 % + 12,21 % + 0,375 %);
- `t` = TFPC + TAPP effective rate (0 % to 2 %; 2 % if no training spend);
- `p` = paid-leave provision (8,33 % outside BTPH; 0 % in BTPH because CACOBATPH finances it);
- `r` = other provisions (dismissal indemnity, notice, CCN bonuses) — company-specific.

```
Monthly employer cost = G + s × A + t × G + p × G + r
Annual employer cost  = 12 × monthly cost  (+ 13th month if the CCN provides one)
Cost per paid hour     = monthly cost / 173.33
```

Notes:

- `G = A + N` if every non-cotisable element is also non-taxable. If a non-cotisable element is taxable, it still adds to `G` but not to `A`.
- **IRG is not an employer cost.** It is withheld from the employee's gross.
- The 13th month is **not statutory**; it exists only by CCN, contract or custom [PRAC].
- `r` for dismissal: notice 1–3 months (CCN), unused leave, CCN indemnity, plus 3 months for economic dismissal. There is **no general statutory dismissal indemnity** — art. 72 of loi 90-11 was **repealed by décret législatif 94-09 art. 35** [S12, REP].

### 7.2 Worked example — clearly illustrative

> **Hypothetical employee**, not a market benchmark: CDI, 40 h/week, no dependants, no CCN premium, **gross 80 000 DA/month**, non-BTPH, employer ≥ 20 employees, **zero training spend**.

**Gross-to-net**

| Line | Amount (DA) | Rule |
|---|---:|---|
| Salaire de base / brut | 80 000,00 | input |
| CNAS salariale (9 %) | −7 200,00 | 80 000 × 9 % |
| Salaire imposable | 72 800,00 | 80 000 − 7 200 |
| Barème IRG | 13 456,00 | 20 000 × 23 % + 32 800 × 27 % |
| Abattement 40 % (capped) | −1 500,00 | 5 382,40 capped at 1 500 |
| **IRG retenu** | **11 956,00** | |
| **Net à payer** | **60 844,00** | 80 000 − 7 200 − 11 956 |

**Employer cost**

| Line | Amount (DA) | Rule |
|---|---:|---|
| Brut | 80 000,00 | |
| CNAS patronale 25 % | 20 000,00 | |
| FNPOS 0,5 % | 400,00 | |
| **Subtotal cash + social** | **100 400,00** | |
| TFPC 1 % | 800,00 | no training spend |
| TAPP 1 % | 800,00 | no apprenticeship/internship |
| **Subtotal** | **102 000,00** | |
| Provision congés payés 8,33 % | 6 666,67 | 80 000 / 12 |
| **Total employer cost / month** | **108 666,67** | **135,8 % of gross** |
| Cost per paid hour | **626,99** | 108 666,67 / 173,33 |
| Annual cost | **1 304 000,00** | × 12 |

**Cost of a 1 000 DA raise**

```
1 000 × (1 + 0,255 + 0,02 + 0,0833) = 1 358,33 DA/month
```
i.e. **135,8 %** of the raise, because CNAS has no ceiling and the paid-leave provision scales with gross.

**Cost of one overtime hour** (same employee, +50 %)

```
hourly base = 80 000 / 173,33 = 461,55
paid hour   = 461,55 × 1,50 = 692,33
employer cost = 692,33 × (1 + 0,255 + 0,02) = 882,72 DA
```
≈ **883 DA per overtime hour** (≈ 869 DA if TFPC/TAPP are fully offset by training spend). The employee additionally bears 9 % CNAS and IRG on the overtime.

### 7.3 Cost per productive hour (not just paid hour)

Paid hours = 173,33/month. **Productive** hours are lower:

```
productive hours = paid hours − leave − public holidays − average sick leave − training
```

With 30 calendar days of leave (≈ 173,33 h) and 14 public holidays (≈ 80 h), a full-time employee works roughly **1 828 h/year** instead of 2 080 h. The **cost per productive hour** is therefore ≈ `annual cost / 1 828`, i.e. **13,8 % higher** than the paid-hour figure [PRAC, arithmetic].

### 7.4 Budgeting rules

- **Monthly budget** = Σ employer cost of active employees + Σ cost of leavers in the month + employer cost of overtime.
- **Annual budget** = 12 × monthly + CCN 13th month + expected raises × 1,358 + expected overtime + dismissal provisions.
- **Raise campaign:** apply the marginal factor **1,255 + t + 0,0833** to the gross increase, not to the gross salary. A 5 % general raise on a 100 M DA payroll costs **≈ 6,79 M DA/month** extra (5 % × 1,358), not 5 M.
- **Hiring:** first-year cost includes recruitment, onboarding, and the fact that the CNAS floor is SNMG (24 000 DA) even for a part-time salary below it.
- **BTPH:** replace the 8,33 % leave provision by the 12,21 % CACOBATPH contribution; the total employer load is **38,085 %** + 2 % taxes.

---

## 8. Bulletin de paie (payslip)

### 8.1 Legal basis

- **Loi 90-11 art. 86:** "Le montant de la rémunération ainsi que celui de tous les éléments qui la composent figurent, **nommément**, dans la fiche de paie périodique établie par l'employeur." The article does **not** apply to reimbursement of expenses [S12, OFF].
- **Loi 90-11 art. 88:** salary paid **regularly and at term** (à terme échu).
- **CIDTA art. 75-2:** the payslip must show the IRG amount **very visibly**, or the exact mention **« retenue de l'impôt sur le revenu global – traitements et salaires – : néant »** [S2, OFF].
- **No decree fixes a single national payslip template.** The structure below is **practice**, built on the legal minimum [S8, PRAC].

### 8.2 Mandatory and near-mandatory content

| Block | Content | Status |
|---|---|---|
| Employer | Legal name, address, **NIF**, **CNAS employer number**, collective agreement reference | PRAC (NIF/CNAS required for filings) |
| Employee | Name, first name, **matricule**, job title and classification, **CNAS social security number**, **NIN** (since 2026 for G29), hire date, family situation / dependants | PRAC + OFF (NIN, dependants) |
| Period | Pay month, days/hours worked, overtime hours | PRAC |
| Earnings | Base salary; each allowance and bonus **named separately**; overtime with hours and rate; benefits in kind | **OFF** (art. 86 "nommément") |
| Deductions | Employee CNAS 9 % (optionally split by branch); IRG (amount and base); advances/loans repayments; other deductions | OFF/PRAC |
| Totals | Gross, total deductions, **net à payer**, payment method and date | PRAC |
| Cumuls | Year-to-date gross, taxable, CNAS, IRG | PRAC |
| Leave | Acquired, taken, balance (in days) | PRAC |
| IRG mention | Amount, or the "néant" wording | **OFF** |

### 8.3 Structure recommended for the SIRH

1. Header — employer + employee + period.
2. **Gains** — base, IEP/seniority, performance, post/nuisance/night, zone, housing, benefits in kind, overtime (by rate), bonuses (monthly vs exceptional separated).
3. **Non-taxable / non-cotisable** — panier, transport, mission, family, with their own legal qualification.
4. **Brut** total.
5. **Retenues salariales** — CNAS 9 % (detail by branch optional), IRG, advances, loans, other.
6. **Net à payer**.
7. **Cumuls annuels** and **solde de congés**.
8. Employer-only information block (employer contributions) — clearly marked "pour information", since it is not a deduction.

### 8.4 Retention

| Document | Duration | Basis | Conf. |
|---|---|---|---|
| Payroll records / payment records | Until end of **4th year** following the withholding year | CIDTA art. 75-2 | OFF |
| Payslip copy | **10 years** is the commonly stated practice; some sources say 5 | No single text located | **UNVERIFIED** |
| CNAS affiliation and DAS supporting documents | **10 years** commonly stated | No single text located | **UNVERIFIED** |
| Accounting documents (SCF) | 10 years | Commercial/accounting practice | PRAC |

> Implement a **10-year** retention default (superset), with the tax 5-year minimum documented.

### 8.5 Payslip prohibitions

The payslip must not mention **union membership, strike participation, or staff-representative functions**. These are confidential and their mention can expose the employer [S8, PRAC].

---

## 9. Declarations calendar

### 9.1 Recurring

| Frequency | Declaration | Body | Deadline | Data required | Src |
|---|---|---|---|---|---|
| On hire | Activity declaration (first employee) | CNAS | **10 days** | Employer identity, activity, first hire | S9, OFF |
| On hire | Employee affiliation | CNAS | **10 days** | Civil status, NSS, contract, salary | S9, OFF |
| On hire | Vacancy notification | ANEM / commune / approved agency | **Before recruiting** (offer must be deposited; direct recruitment only after the 5-working-day window, then immediate information) | Job profile, number of posts, contract type | S20, REP |
| Monthly | Recruitment reporting | ANEM (wilaya agency) | Within **10 days** after month end | Branch, socio-professional category, age, gender, posts filled, employer data | S20, OFF |
| Monthly (≥10 employees) | **DAC** + contribution payment | CNAS | Within **30 days** of month end | Headcount, per-employee base, contributions | S9, OFF |
| Quarterly (≤9 employees) | **DAC** + payment | CNAS | Within **30 days** of quarter end | Same | S9, OFF |
| Monthly | **G n°50** (IRG + VAT + other) | DGI | **1st–20th** of following month | IRG withheld per employee (total), taxable bases, VAT | S2, OFF |
| Quarterly | **G n°50 ter** (IRG only, IFU/simplified) | DGI | 1st–20th after quarter | IRG withheld | S26, OFF |
| Monthly/quarterly | TLS (pipelines/mining only) | DGI | With G50 | Turnover | S14, OFF |
| Semestrial | **TFPC + TAPP** | DGI | **20 July** (S1) / **20 January N+1** (S2) | Gross half-year payroll, training and apprenticeship spend, invoices | S6, OFF |
| Event | Work accident | CNAS | **48 h** | Accident report, victim data | S8, OFF |
| Event | Cessation / death of employer | DGI (G29) | 10 days / 6 months | Final salary state | S2, OFF |

### 9.2 Annual

| Declaration | Body | Deadline | Data required | Src |
|---|---|---|---|---|
| **DAS** (déclaration annuelle des salaires et salariés) | CNAS | **1–31 January** | Per employee: NSS, identity, entry/exit, time worked, **salary per quarter**, contributions | S9, S18, OFF |
| **DAS** BTPH | CACOBATPH | **31 July** (reference year 1 Jul–30 Jun) | Same, BTPH perimeter | S18, OFF |
| **G n°29** (état annuel des salaires) | DGI | **30 April** | Per beneficiary: name, **NIN**, job, address, family situation, gross, net, IRG withheld | S2, OFF |
| **G n°1** (personal global income) | DGI | **30 June** (since LF 2025) | Employee's other income; credit for withheld IRG | S2, OFF |
| CASNOS base declaration | CASNOS | **31 January** | Declared income / turnover | S23, REP |
| CASNOS contribution payment | CASNOS | **30 June** (1 Oct agriculture) | — | S23, REP |
| Employer's annual accounts / social balance sheet | CNRC / tax | 30 April – 30 June (varies) | Payroll totals | PRAC |

### 9.3 What each body actually needs (data contract)

| Body | Minimum data set |
|---|---|
| **CNAS** | Employer number, NIF, employee NSS, civil status, hire/exit dates, contract type, CNAS base per period, headcount, contribution split |
| **DGI (G50/G29)** | NIF, NIN, employee identity and address, family situation, gross and net paid, IRG base, IRG withheld, period |
| **CASNOS** | Activity code, registration number, declared income, base, contribution |
| **ANEM** | Branch, socio-professional category, age, gender, posts, contract type, recruitment date |
| **CACOBATPH (BTPH)** | Same as CNAS + site/chantier and bad-weather periods |

---

## 10. SIRH implications

### 10.1 Master data the module must hold

**Company**
- NIF, CNAS employer number, CASNOS number (if applicable), CACOBATPH number (if BTPH), DGI tax office, Jibaya'tic access, collective agreement reference, sector (BTPH flag), wilaya (for zone/south leave), payroll calendar, rounding policy.

**Employee**
- Identity: name (FR/AR), date of birth, place of birth, gender, nationality.
- **NIN** (mandatory since 2026), **NSS/CNAS number**, badge/matricule.
- Family situation and **number of dependants** (recorded even though it has no IRG effect).
- Address, bank/CCP details.
- Hire date, contract type (CDI/CDD/ANEM scheme/apprenticeship), trial period, classification/coefficient, job, establishment, wilaya.
- Exit date and reason.
- Flags: disabled worker, pensioner, expatriate, posted worker, part-time, multi-employer.

**Pay element (the key object)** — every element must carry:
- code, label FR/AR, type (fixed / variable / recurring / exceptional);
- **cotisable CNAS** Y/N and, if Y, its own base rule;
- **imposable IRG** Y/N and its own base rule;
- **counts toward SNMG** Y/N;
- proratisable Y/N, and the proration basis (30 days, 173,33 h, working days);
- order in the calculation cascade;
- CCN/contract source;
- effective-dated amount/rate;
- whether it is a **monthly recurring** bonus (barème) or **non-monthly** (10 % flat).

### 10.2 Rules engine

1. **Salary proration** — hire/exit mid-month, part-time, unpaid absence, sick leave suspension.
2. **SNMG control** — base + allowances (excluding expense reimbursements) ≥ 24 000 DA (full-time equivalent). Block payroll if breached.
3. **CNAS base** — apply inclusion/exclusion per element; floor at SNMG; no ceiling; BTPH overlay.
4. **IRG** — taxable base = gross taxable − CNAS 9 % − pension; exemption ≤ 30 000; barème; abattement 40 % clamp 1 000/1 500; smoothing band; disabled/pensioner variant; **10 % flat** on non-monthly bonuses.
5. **Overtime** — cap 8 h/week, 12 h/day amplitude, +50 % floor, CCN rate, rest-day compensation.
6. **Leave** — 2,5 days/month, 30 calendar days cap, 10 extra days in southern wilayas, reference period 1 July–30 June, indemnity = 1/12 of reference-year remuneration.
7. **Termination** — notice per CCN, leave balance, CCN indemnity, 3 months for economic dismissal, certificate of work.
8. **Costing** — employer load 25,5 % (or 38,085 % BTPH), TFPC/TAPP 0–2 %, leave provision, per-hour and per-productive-hour cost.
9. **Declarations** — generate DAC, DAS, G50, G29 extracts with the exact data contract; control totals; NIN completeness check.

### 10.3 Edge cases to handle explicitly

- **Month of hire/exit** — proration and the 15-working-day rule for leave (arts. 43–44).
- **Unpaid leave** — reduces CNAS base but the floor at SNMG may still apply.
- **Sick leave** — contract suspended; CNAS pays IJ; CCN top-up optional; no CNAS contribution on the IJ.
- **Maternity** — 98 days; CNAS pays; keep seniority and leave accrual.
- **Work accident** — 48 h declaration; 100 % IJ from day 1; employer pays the accident day.
- **Public holiday on a weekend** — no carry-over.
- **Ramadan** — panier not paid to Muslim staff on normal day shift (practice).
- **Southern wilayas** — +10 days leave minimum.
- **BTPH** — CACOBATPH instead of leave provision; different DAS year; 0,375 % employee chômage-intempéries.
- **Disabled employee / pensioner** — 42 500 DA smoothing threshold instead of 35 000.
- **Non-monthly bonus** — 10 % flat, not barème.
- **Benefits in kind** — food floor 400 DA/meal; housing/vehicle valued case by case.
- **Expatriate** — work permit is a labour-ministry matter, not ANEM; tax treaty may override; **no general expatriation allowance exemption** in the CIDTA (only residence/isolation ≤ 70 % of base). Flag each case.
- **Multiple employers** — each withholds; employee regularises via G1 by 30 June.
- **CASNOS + salary** — dual affiliation; do not assume CNAS covers the non-salary income.
- **Cessation of business** — G29 within 10 days; final pay and certificate.
- **Recalculations / arrears** — arrears on salary follow the barème if they relate to the current period; non-monthly arrears follow the 10 % rule. Define a policy and document it.
- **Rounding** — no legal rule; choose 2 decimals or nearest dinar and apply consistently. Document the choice.

### 10.4 Ambiguities where practice differs by company / CCN

| Topic | Why it differs | Recommendation |
|---|---|---|
| Transport and panier IRG treatment | Not expressly exempted by CIDTA art. 68 | Parameterise, require a written tax position, log the choice |
| Overtime hourly base | "Salaire horaire normal" not defined; base salary vs total reference salary | Parameterise per CCN |
| Notice duration | Law refers to CCN (arts. 68 and 73); no statutory number | Store per CCN/contract |
| Dismissal indemnity | Art. 72 repealed; no general statutory amount | Store per CCN/règlement intérieur |
| Daily absence divisor | 30 vs working days vs 173,33 h | Parameterise and keep consistent |
| Advance repayment cap | No statutory cap located | Company policy + written agreement |
| 13th month / bonuses | Not statutory | Per CCN/contract |
| Night / shift / astreinte premiums | Not statutory | Per CCN |
| Housing / vehicle benefits valuation | No national scale | Documented valuation method per company |
| Sick-leave top-up | Not statutory | Per CCN |
| CASNOS 2026 transitional base | Decree applies from 23 July 2026 | Confirm with CASNOS before computing |
| TFPC/TAPP treatment of non-cotisable allowances in the base | "Rémunérations brutes versées" is broad | Take the conservative (include) position, flag |

### 10.5 Controls the module should ship with

- SNMG breach alert (per employee, per month).
- CNAS base < SNMG alert.
- IRG recomputation against the official DGI table (oracle test).
- Overtime cap alert (8 h/week, 12 h/day).
- NIN / NSS completeness before G29/DAS generation.
- DAC vs payroll reconciliation (headcount, base, contributions).
- G50 IRG total vs payroll IRG total.
- Leave balance vs provision reconciliation.
- DAS vs 12 × DAC reconciliation.
- BTPH flag consistency (CACOBATPH vs leave provision).
- Effective-date control on every statutory parameter (SNMG, barème, rates, thresholds).

---

## Sources

All URLs retrieved **2026-11-07**.

| # | Source | Publisher / type | URL |
|---|---|---|---|
| S1 | Décret présidentiel n° 26-01 du 7 janvier 2026 fixant le SNMG (JO 2026 n° 1) | JORADP — **OFF** | https://www.joradp.dz/FTP/jo-francais/2026/F2026001.pdf |
| S2 | Impôt sur le revenu global — Traitements et salaires (updated 26 Mar 2024) | DGI — **OFF** | https://www.mfdgi.gov.dz/fr/particuliers/irg-traitements-et-salaires |
| S3 | Table IRG 2022 (barème mensuel) | DGI — **OFF** | https://mfdgi.gov.dz/images/bareme_irg/TABLE_IRG_2022.pdf |
| S4 | Loi n° 21-16 du 30 décembre 2021 portant loi de finances pour 2022 | Ministère des Finances / DGB — **OFF** | https://dgb.mf.gov.dz/wp-content/uploads/2022/01/LF_2022.pdf |
| S5 | Code des impôts directs et taxes assimilées — édition 2026 (consolidated) | Official text, non-government mirror — **OFF** | https://a-tla.org/sites/default/files/2026-05/Algeria%20-%20Code%20des%20Imp%C3%B4ts%20Directs%20et%20Taxes%20Assimil%C3%A9es%202026%20C.pdf |
| S6 | Loi n° 25-17 du 14 décembre 2025 portant loi de finances pour 2026 (FR) | Ministère des Finances — **OFF** | https://www.mf.gov.dz/images/pdf/loidefinance/Loi_de_Finances_2026_FR.pdf |
| S7 | Les cotisations en Algérie (2024 edition) | CLEISS — **REP** | https://www.cleiss.fr/docs/cotisations/algerie.html |
| S8 | La sécurité sociale des salariés en Algérie | CLEISS — **REP** | https://www.cleiss.fr/docs/regimes/regime_algerie_salaries.html |
| S9 | Guide de télédéclaration CNAS (DAC, DAS, délais) | CNAS — **OFF** | https://teledeclaration.cnas.dz/pdf/Guide%20TELE-DECLARATION.pdf |
| S10 | Le certificat médical d'arrêt de travail | CNAS — **OFF** | https://cnas.dz/fr/le-certificat-medical-darret-de-travail/ |
| S11 | Présentation de la CNAS (prestations, 98 jours maternité, IJ) | CNAS — **OFF** | https://cnas.dz/fr/presentation-de-la-cnas/ |
| S12 | Loi n° 90-11 du 21 avril 1990 relative aux relations de travail (consolidated, FR) | ILO NATLEX — **OFF** | https://natlex.ilo.org/dyn/natlex2/natlex2/files/download/9557/DZA-9557.pdf |
| S13 | Législation du travail (salaire, congés, fêtes légales, SNMG) | MTESS — **OFF** | https://www.mtess.gov.dz/fr/legislation-du-travail/ |
| S14 | Loi de finances 2024 — mesures phares (suppression TAP) | KPMG Algérie — **REP** | https://assets.kpmg.com/content/dam/kpmgsites/dz/pdf/newsletter/loi-de-finances-2024-fr.pdf.coredownload.inline.pdf |
| S15 | Les dispositions fiscales de la loi de finances pour 2024 | DGB / Ministère des Finances — **OFF** | https://dgpp.mf.gov.dz/wp-content/uploads/2024/01/Les-dispositions-fiscales-de-la-loi-de-finances-pour-2024-1.pdf |
| S16 | Guide des affaires Algérie 2025 (taxes de formation et d'apprentissage, TLS) | Business France — **REP** | https://event.businessfrance.fr/rencontres-algerie/wp-content/uploads/sites/1317/2025/03/Guide-des-affaires-Algerie-2025.pdf |
| S17 | Déclaration d'assiette des cotisations (CACOBATPH, taux 12,21 % / 0,75 %) | CACOBATPH — **OFF** | https://www.cacobatph.dz/dac/?lang=fr |
| S18 | DAS — Déclaration annuelle des salaires (CACOBATPH, année de référence, pénalités) | CACOBATPH — **OFF** | https://www.cacobatph.dz/das/?lang=fr |
| S19 | Ordonnance n° 95-01 du 21 janvier 1995 fixant l'assiette des cotisations | Official text mirror — **OFF** | https://kanonix.app/documents/ordonnance-95-01-fr |
| S20 | Décret exécutif n° 09-94 (informations ANEM : besoins trimestriels, recrutements mensuels) | Official text mirror — **OFF** | https://gms-dz.com/wp-content/uploads/2025/01/Decret-executif-n%C2%B0-09-94-AWEM.pdf |
| S21 | Loi n° 63-278 du 26 juillet 1963 fixant la liste des fêtes légales (consolidated) | Official text mirror — **OFF** | https://kanonix.app/documents/loi-63-278-fr |
| S22 | Loi n° 23-10 du 26 juin 2023 (Aïd porté à 3 jours) — JO n° 43/2023 | JORADP — **OFF** | https://www.joradp.dz/FTP/JO-FRANCAIS/2023/F2023043.pdf |
| S23 | Décret exécutif n° 26-257 du 15 juillet 2026 (CASNOS : 15 %, base 288 000–5 760 000) — analysis of JO 53/2026 | UpGrowth — **REP** | https://www.upgrowth.dz/journal-officiel/decret-26-257-cotisation-securite-sociale-non-salaries |
| S24 | Algeria — social security country profile (2026) | ISSA — **REP** | https://www.issa.int/sites/default/files/documents/2026-02/1-%20Alg%C3%A9rie.pdf |
| S25 | Taxe sur l'activité professionnelle (historic DGI page, pre-2024) | DGI — **OFF** | https://www.mfdgi.gov.dz/fr/professionnels/services-pro/regime-reel/taxe-sur-lactivite-professionnelle |
| S26 | Calendrier fiscal — paiement trimestriel des retenues à la source (IFU / simplifié) | DGI — **OFF** | https://www.mfdgi.gov.dz/fr/professionnels/calandrier-fiscal-pro/595-regime-reel-simplifie/531-paiement-trimestriel-des-retenues-a-la-source |
| S27 | Nouvelles modalités de souscription des déclarations fiscales (LF 2026, télédéclaration) | DGI — **OFF** | https://www.mfdgi.gov.dz/fr/a-propos/actu-fr/nouvelles-modalites-introduites-par-la-loi-de-finances-2026-en-matiere-de-souscription-des-declarations-fiscales |
| S28 | Algérie : principales mesures de la loi de finances pour 2026 | Deloitte — **REP** | https://blog.avocats.deloitte.fr/algerie-les-principales-mesures-de-la-loi-de-finances-pour-2026/ |
| S29 | Algeria — Finance Law 2026: key tax measures | EY — **REP** | https://taxnews.ey.com/news/2026-0245-algeria-finance-law-2026-key-tax-and-regulatory-measures-impacting-foreign-and-algerian-companies |
| S30 | CASNOS 2026 : cotisation, délais, assiette | Hsabet — **REP/PRAC** | https://hsabet.com/fr/guides/casnos-algerie |
| S31 | Assiette de cotisation CNAS (inclusions/exclusions, plancher SNMG) | Alzirc — **REP** | https://alzirc.com/social/assiette-cnas/ |
| S32 | Loi n° 83-14 du 2 juillet 1983 (JO n° 28/1983) — obligations des assujettis | JORADP — **OFF** | https://www.joradp.dz/FTP/jo-francais/1983/F1983028.pdf |
| S33 | La déclaration des salaires (G29) devient obligatoire en ligne | TSA / DGI circular of 22 Sep 2025 — **REP** | https://www.tsa-algerie.com/impots-en-algerie-la-declaration-des-salaires-devient-obligatoire-en-ligne/ |
| S34 | Barème IRG 2026 — table de contrôle et exemples chiffrés | Winalco — **PRAC** | https://winalco.dz/documents/bareme-irg-2026-algerie.pdf |
| S35 | Indemnité d'expérience professionnelle — décret 85-58 (textes réglementaires) | Portail juridique ESI — **OFF** | https://portailjuridique.esi.dz/fran%C3%A7ais/gestion-de-ressources-humaines/indemnit%C3%A9-dexp%C3%A9rience-professionnel |
| S36 | Permis de travail des salariés étrangers (loi 81-10, décret 82-510, ANEM vs ministère) | UpGrowth — **REP** | https://www.upgrowth.dz/permis-de-travail-etranger-algerie |
| S37 | IRG 2026 : exonération 30 000 DA, abattements, absence de réduction par enfant | Almawarid — **REP** | https://almawarid.app/blog/comment-calculer-lirg-en-algerie-en-2025-tranches-taux-et-exemples/ |

---

## Open questions / UNVERIFIED

Items below are **not** settled by a source of sufficient authority. They must be resolved before the SIRH rules are frozen.

1. **IRG 30 001–35 000 band at the 35 000 boundary.** The published smoothing formula and the ordinary barème do not meet at 35 000; the tax appears to jump. The DGI's official monthly table must be obtained and implemented as a lookup. Test 30 000 / 30 001 / 34 999 / 35 000 / 35 001. *Status: UNVERIFIED (boundary only; the rest of the barème is OFF).*

2. **IRG treatment of flat transport and panier allowances.** CIDTA art. 68 does not list them; practice exempts them. The 1,5 × hourly SNMG panier amount and the exemption of a flat transport allowance have **no explicit legal basis**. Risk of reclassification on audit. *Status: PRAC + UNVERIFIED.*

3. **CASNOS 2026 transitional base.** Décret 26-257 applies from **23 July 2026 without retroactivity**. Whether contributions for 1 Jan–22 Jul 2026 use the old fixed base (216 000 / 4 320 000) or the new SNMG-indexed base is not stated in the sources consulted. *Status: UNVERIFIED — confirm with CASNOS.*

4. **CNAS payment deadline: 15 days or 30 days?** Loi 83-14 art. 21 says 15 days after the month/quarter; the CNAS portal and guide enforce 30 days. Also, the DAS late penalty is quoted as **5 %/month** in the official texts and **2 %/month** in one press source. *Status: 5 % is retained; deadline conflict UNVERIFIED.*

5. **Advance (avance) repayment cap.** Guides cite "1/5 of net salary under art. 85 loi 90-11"; art. 85 actually concerns monetary payment. No statutory cap was located. Also no explicit prohibition of disciplinary fines in loi 90-11. *Status: UNVERIFIED — legal counsel required.*

6. **Payslip and CNAS document retention.** Tax law gives 4 years + current (CIDTA art. 75). The "10 years" for payslips and CNAS documents is practice, not a located text. *Status: UNVERIFIED.*

7. **Dismissal indemnity.** Art. 72 loi 90-11 (1 month/year, cap 15 months) was **repealed** by décret législatif 94-09 art. 35. Several widely-read sites still publish 15/20/30-day scales (French-style) that have no basis in Algerian law. The only statutory amount located is **3 months** for economic dismissal. *Status: no general statutory indemnity — OFF; amounts per CCN are UNVERIFIED.*

8. **Notice periods.** The law refers to collective agreements (arts. 68 and 73); no statutory duration. The 1/2/3-month grid is **practice**, not law. *Status: PRAC.*

9. **Housing and vehicle benefit valuation.** CIDTA art. 71 mandates "real value" but gives no scale for housing or vehicles. The 400 DA/meal floor is the only statutory number. *Status: UNVERIFIED for housing/vehicle.*

10. **CNAC employer reductions for 2026.** Schemes exist (hires ≥ 6 months, southern/high-plateau rates up to 2,5 % instead of 25 %), but the current eligibility and rates were not confirmed from a CNAC circular. *Status: UNVERIFIED — do not implement.*

11. **TFPC/TAPP base and non-cotisable allowances.** "Masse salariale brute" is defined as gross remuneration before contributions and IRG, but the treatment of panier/transport (excluded from CNAS) is not expressly settled. *Status: UNVERIFIED — take the conservative include-position.*

12. **"Participation CNAC".** No separate levy of that name was found. CNAC is financed by the 1,5 % unemployment contribution inside CNAS. If the product spec means something else (e.g. a sectoral fund), it needs a source. *Status: not found.*

13. **Rounding rule.** No legal text fixes payroll rounding. *Status: PRAC — document the chosen policy.*

14. **Public holiday count.** The MTESS page still lists Aïd at 2 days; loi 23-10 (2023) says 3. The law prevails, but some official pages are stale. *Status: resolved in favour of 3 days (OFF); the discrepancy is an operational risk for calendar imports.*
