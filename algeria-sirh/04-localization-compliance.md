# 04 — Localization and compliance operations (Algeria)

**Status:** research complete for product design; legal points marked `UNVERIFIED` need Algerian counsel before go-live.
**Retrieval date for all sources:** 7 November 2026.
**Scope:** what an Algerian SIRH must render, store, sign, declare and integrate so that a private-sector employer can run HR and payroll without breaking local expectations. It is not a substitute for the payroll rules in `01-payroll-costisation.md` or the labour-law rules in `02-legal-declarations.md`; it covers the *localization layer* around them.

## Legend

| Tag | Meaning |
|---|---|
| **LAW** | Binding legal or regulatory text, with the reference given. |
| **PRACTICE** | Observed market/administrative practice, not a legal obligation. |
| **UNVERIFIED** | No reliable source found, sources conflict, or the text is silent. Do not code as a hard rule. |
| **A CONFIRMER** | 2026 religious date not yet confirmed by an official Algerian communiqué at retrieval time. |
| **CONFIRMÉ** | Date confirmed by an official Algerian communiqué or by a fixed legal date. |

Two conventions from the index apply throughout: law and common practice are kept separate, and every rate/threshold/duration must carry a source and an effective date.

---

## 1. Languages and UI

### 1.1 Legal status

| Language | Status | Consequence for the SIRH |
|---|---|---|
| Arabic (ar) | National and official language of the State (Constitution 2020, art. 3). | Default language for official documents, administration-facing output and legal acts. |
| Tamazight (ber) | Also national and official (Constitution 2020, art. 4), with an academy and organic-law implementation. | Not required for payroll, but should be supported as a display language where the employer chooses; do not assume Tifinagh vs Latin script. |
| French (fr) | No official status. De facto working language of business, banks, many employers and much of higher education. | Must be supported as a first-class UI and document language. Most Algerian HR users will expect French payroll vocabulary. |

The 1991 Arabisation law (loi n° 91-05) requires Arabic for official documents, reports, minutes and acts, and even penalises signing a document in another language in an official capacity. Its general application was deferred/suspended from 1992 and it is unevenly enforced; the practical result is **Arabic for administration, bilingual Arabic/French for employees and business** ([loi 91-05, JO 1991](https://www.joradp.dz/JO8499/1991/003/Fp38.pdf); [décret 92-303](https://www.axl.cefan.ulaval.ca/afrique/algerie_decret-92-303-1992.htm)).

Court filings and exhibits must be in Arabic or accompanied by an official translation (loi 08-09, art. 8), which matters for any employment dispute export ([loi 08-09](https://droit.mjustice.gov.dz/sites/default/files/loi_fr_08-09.pdf)).

**Product rule:** ship `ar` and `fr` as equal UI locales; treat `ar-DZ` as the default for official output and `fr-DZ` as the default for internal/HR output, per company. Do not treat French as a fallback only.

### 1.2 RTL and mixed-direction layout

- Mirror the whole application shell for Arabic: navigation on the right, progress direction right-to-left, icons with direction (arrows, chevrons) flipped.
- Do **not** mirror: RIB/account numbers, amounts, dates, ISO codes, phone numbers, e-mail addresses, file names, chart axes when the axis is numerical. Wrap them in `dir="ltr"` / bidi isolates.
- Forms with mixed content are the hard part: an Arabic label followed by a French name, or an Arabic name inside a French sentence. Use Unicode bidi isolation (`<bdi>`, `dir="auto"`, or `\u2068…\u2069`) around user data, never around the whole field.
- Tables: keep column order logical in the data model; mirror only at render time. Numeric columns right-align in LTR and left-align in RTL.
- PDF generation must embed an Arabic font with proper shaping (harfbuzz) and must not rely on the browser's bidi for the whole page; generate per-cell runs.
- Arabic resets: use `lang="ar"` on the html element and per-fragment `lang` attributes so screen readers and hyphenation behave.

### 1.3 Fonts and typography

| Use | Recommended | Notes |
|---|---|---|
| Arabic UI/body | Noto Naskh Arabic, IBM Plex Sans Arabic, Cairo | Naskh is more legible for long text and legal documents; Cairo/Plex are better for dense UI. |
| Arabic headings | IBM Plex Sans Arabic SemiBold, Cairo Bold | Avoid display fonts for payroll tables. |
| French/Latin UI | Inter, Source Sans 3, IBM Plex Sans | Match x-height with the Arabic face. |
| Monospace (RIB, amounts) | IBM Plex Mono, JetBrains Mono | Keep digits LTR. |

Do not use Arabic-Indic digits by default. CLDR `ar-DZ` uses the Latin numbering system (`latn`) with `,` decimal and `.` grouping ([CLDR ar-DZ numbers](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/ar-DZ/numbers.json)). Algerian payroll documents overwhelmingly use Latin digits; offer Arabic-Indic only as an explicit per-company option, and never mix systems inside one amount.

### 1.4 Bilingual terminology glossary (FR ↔ AR)

Terms below are aligned with CNAS/DGI bilingual usage; this is a product glossary, not a sworn translation. Where CNAS uses a different form, prefer the CNAS form on declarations.

| French | Arabic | Notes |
|---|---|---|
| salaire | أجر / راتب | “أجر” is the labour-law term; “راتب” is common in payroll UI. |
| salaire de base | الأجر الأساسي | |
| salaire brut | الأجر الخام | |
| salaire net | الأجر الصافي | |
| net à payer | الصافي للدفع | |
| retenue | خصم / اقتطاع | “اقتطاع” for statutory withholding; “خصم” for deductions. |
| cotisation | اشتراك | |
| cotisation sociale | اشتراك الضمان الاجتماعي | |
| cotisation salariale | الاشتراك العمالي | Employee share. |
| cotisation patronale | الاشتراك المستخدم | Employer share. |
| bulletin de paie | كشف الراتب / بطاقة الأجر | Use “كشف الراتب” in UI; CNAS/DGI forms may say “كشف الأجر”. |
| fiche de paie | بطاقة الأجر | Same document; keep one term per locale. |
| contrat de travail | عقد العمل | |
| contrat à durée indéterminée (CDI) | عقد عمل غير محدد المدة | |
| contrat à durée déterminée (CDD) | عقد عمل محدد المدة | |
| période d'essai | فترة الاختبار | |
| employeur | المستخدم / رب العمل | “المستخدم” is the statutory term in social-security texts. |
| salarié / travailleur | عامل / أجير | “عامل” is the labour-law term. |
| congé | عطلة | |
| congé annuel | العطلة السنوية | |
| congé maladie | العطلة المرضية | |
| congé maternité | عطلة الأمومة | |
| absence | غياب | |
| heure supplémentaire | ساعة إضافية | |
| prime | علاوة | |
| indemnité | تعويض | |
| avantage en nature | مزية عينية | |
| ancienneté | الأقدمية | |
| promotion | ترقية | |
| licenciement | التسريح | |
| démission | الاستقالة | |
| fin de contrat | نهاية علاقة العمل | |
| certificat de travail | شهادة نهاية العمل | Distinguish from attestation de travail. |
| attestation de travail | شهادة عمل | |
| attestation de salaire | شهادة الأجر / شهادة راتب | |
| attestation de travail et de salaire (ATS) | شهادة العمل والأجر | CNAS form. |
| ordre de virement | أمر تحويل | |
| virement bancaire | تحويل بنكي | |
| relevé d'identité bancaire (RIB) | معرف بنكي | Keep “RIB” in UI; the 20-digit number is universally called RIB. |
| compte courant postal (CCP) | الحساب البريدي الجاري | Algérie Poste. |
| déclaration annuelle des salaires (DAS) | التصريح السنوي بالأجور والعمال | |
| déclaration des assiettes de cotisation (DAC) | تصريح وعاء الاشتراكات | |
| IRG (impôt sur le revenu global) | الضريبة على الدخل الإجمالي | |
| CNAS | الصندوق الوطني للتأمينات الاجتماعية للعمال الأجراء | Keep the acronym. |
| CASNOS | الصندوق الوطني للضمان الاجتماعي لغير الأجراء | Non-salaried; not payroll. |
| CNAC | الصندوق الوطني للتأمين على البطالة | Unemployment insurance. |
| sécurité sociale | الضمان الاجتماعي | |
| retraite | التقاعد | |
| pointage | تسجيل الحضور | |
| jour férié | يوم عطلة رسمية / عيد | “عيد” for religious feasts; “عطلة رسمية” for statutory days. |
| exercice fiscal | السنة المالية | |
| devise | العملة | |
| taux de change | سعر الصرف | |

Sources for terminology in context: [CNAS employer portal FR/AR](https://teledeclaration.cnas.dz/), [CNAS digital services](https://cnas.dz/fr/nos-services-numeriques), [DGI G50 form](https://www.mfdgi.gov.dz/fr/espace-telechargements/formulaires-declaration).

---

## 2. Numbers, dates, currency, time

### 2.1 Numbers and currency

| Item | Rule | Source / note |
|---|---|---|
| Currency | Algerian dinar, ISO `DZD`, local symbol `DA` (French) / `د.ج` (Arabic). 1 dinar = 100 centimes. | ISO 4217; CLDR `fr-DZ` symbol `DA`, `ar-DZ` symbol `د.ج`. |
| Decimal separator | Comma `,` in both French and Arabic (Algeria). | CLDR ar-DZ and fr-DZ both `decimal: ","`. |
| Thousands separator | Space in French typography (CLDR uses narrow no-break space U+202F); dot is also common in Algerian documents and in `ar-DZ` CLDR. | CLDR fr-DZ `group: "\u202f"`, ar-DZ `group: "."`. Pick **one** per company and render consistently. |
| Recommended display | `1 234 567,89 DA` (French) / `1.234.567,89 د.ج` (Arabic) | Space/dot are both accepted; never use comma for thousands. |
| Decimals | Store money as integer centimes or `DECIMAL(15,2)`. Display 2 decimals for amounts, 0 decimals is common on summaries but is a presentation choice, not a rule. | Prevents rounding drift in CNAS/IRG. |
| Negative amounts | Minus sign before the number: `-12 500,00 DA`. Accounting exports may use parentheses `(12 500,00)`. | Choose one per output type; never mix. |
| Percentages | `9 %` (French space before %), `9%` in compact UI. | Cosmetic; keep the value numeric. |
| Machine formats | CSV/API: UTF-8, `.` decimal, no thousands separator, no currency symbol, ISO date. | Required for bank and CNAS files. |

CLDR references: [ar-DZ numbers](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/ar-DZ/numbers.json), [fr-DZ numbers](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/fr-DZ/numbers.json), [ar-DZ currencies](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/ar-DZ/currencies.json).

### 2.2 Dates and calendar

| Item | Rule |
|---|---|
| Human date | `dd/mm/yyyy` (e.g. `07/11/2026`). CLDR `fr-DZ` short is `dd/MM/y`; `ar-DZ` short is `d/M/y`, medium `dd/MM/y`. |
| Long date | `7 novembre 2026` / `7 نوفمبر 2026`. |
| API / storage | ISO 8601 `YYYY-MM-DD`; timestamps in UTC with explicit offset, displayed in `Africa/Algiers`. |
| Week start | Sunday in practice for business calendars (most private employers work Sunday–Thursday with Friday–Saturday off). CLDR does not set a first day for DZ; do not rely on it. |
| Hijri | Display-only, never the calculation basis for pay, leave or deadlines. Show the Hijri equivalent next to the Gregorian date where the document is religious (holiday notices, Ramadan). |
| Fiscal year | Civil year, 1 January–31 December, by default under the SCF; an entity may use another closing date only if its activity cycle justifies it. |
| Time zone | `Africa/Algiers`, UTC+01:00 all year. No daylight saving since 1981. |

Hijri implementation: do **not** use a calculated Umm al-Qura table to decide whether tomorrow is a holiday. Algerian religious dates are proclaimed after lunar observation (see §3). Store the official Gregorian date as the source of truth and optionally display the Hijri date that the communiqué states.

### 2.3 Time zone and DST history

Algeria has used UTC+01:00 permanently since 1981 and has not observed DST since the night of 31 October 1980. IANA zone: `Africa/Algiers`. The legal time is GMT+1 under the arrêté of 6 April 1981 ([timeanddate DST history](https://www.timeanddate.com/time/change/algeria?year=1980); [Time.is Algeria](https://time.is/fr/Algeria)). SIRH consequence: no DST transition jobs, no ambiguous local times; still store UTC and convert on display.

---

## 3. Calendar, holidays and working time

### 3.1 Weekend

- **Private sector:** the Labour Code (loi 90-11, art. 33) fixes the normal weekly rest day as **Friday**, one full day; it does not itself mandate Saturday. In practice most private employers, banks and insurers are closed Friday–Saturday, but retail, health, security, hospitality and continuous-process plants use other patterns.
- **Product rule:** weekend is **per establishment**, default `Fri-Sat`, configurable to `Fri` only or a rolling roster. Do not hard-code Saturday as non-working for overtime.

### 3.2 Statutory public holidays

The list is fixed by loi 63-278 of 26 July 1963, as modified by ordonnance 68-419, loi 05-06, loi 18-12 (added Yennayer and Gregorian New Year) and loi 23-10 of 26 June 2023 (three days for each Eid) ([loi 63-278](https://www.joradp.dz/FTP/jo-francais/1963/F1963053.pdf); [loi 23-10, JO n°43/2023](https://www.joradp.dz/FTP/jo-francais/2023/F2023043.pdf); [compilation of texts](https://portailjuridique.esi.dz/fran%C3%A7ais/f%C3%AAtes-et-cong%C3%A9s-l%C3%A9gales)).

**Fixed (Gregorian) days, every year:**

| Date | Holiday | Days |
|---|---|---|
| 1 January | New Year's Day (Jour de l'An) | 1 |
| 12 January | Yennayer, Amazigh New Year | 1 |
| 1 May | Labour Day | 1 |
| 5 July | Independence Day | 1 |
| 1 November | Anniversary of the Revolution | 1 |

**Religious days (Hijri, proclaimed):**

| Holiday | Legal duration |
|---|---|
| Eid al-Fitr (Aïd el-Fitr / Aïd Esseghir) | 3 days |
| Eid al-Adha (Aïd el-Adha / Aïd el-Kébir) | 3 days |
| 1 Muharram (Islamic New Year) | 1 day |
| Achoura (10 Muharram) | 1 day |
| Mawlid al-Nabi (El Mawlid Ennabaoui) | 1 day |

That is 14 legal days. The Ministry of Labour page still shows the pre-2023 two-day Eid; loi 23-10 is later and prevails. The same page adds employee-specific legal holidays: for Christian staff, Easter Monday, Ascension, 15 August (Assumption) and 25 December (Christmas); for Jewish staff, Roch Achana, Yom Kippur and Pesach. These are statutory for the employees concerned, not general closures, and they must be modelled as optional per-employee holiday entitlements ([MTESS, Législation du travail](https://www.mtess.gov.dz/fr/legislation-du-travail)).

**2026 table — do not treat computed dates as legal:**

| Date 2026 | Holiday | Status |
|---|---|---|
| Thu 1 Jan | New Year's Day | CONFIRMÉ (fixed by law) |
| Mon 12 Jan | Yennayer | CONFIRMÉ (fixed by law) |
| Fri 1 May | Labour Day | CONFIRMÉ (fixed by law) |
| Sun 5 Jul | Independence Day | CONFIRMÉ (fixed by law) |
| Sun 1 Nov | Anniversary of the Revolution | CONFIRMÉ (fixed by law) |
| Date not fixed (3 days) | Eid al-Fitr | **A CONFIRMER** — official communiqué not retrieved; non-official sources point to 19, 20 or 24 March, so no date is asserted here. |
| Wed 27 – Fri 29 May | Eid al-Adha | **CONFIRMÉ** — joint Ministry of Labour / DGFP communiqué reported by APS on 24 May 2026: 10–12 Dhou el Hidja 1447 = 27–29 May 2026. |
| Around 16–17 Jun | 1 Muharram | **A CONFIRMER** — sources conflict (16 vs 17 June). |
| Around 25–26 Jun | Achoura | **A CONFIRMER** — sources conflict. |
| Around 25–26 Aug | Mawlid al-Nabi | **A CONFIRMER** — sources conflict. |

Sources for the 2026 confirmations/uncertainties: [APS, 24 May 2026](https://www.aps.dz/fr/algerie/societe/mpjo2nai-les-journees-du-mercredi-jeudi-et-vendredi-prochains-chomees-et-payees); [Austrian embassy 2026 list](https://www.bmeia.gv.at/fileadmin/user_upload/Vertretungen/Algier/Dokumente/2026_Jours_feries.pdf); [public holidays compilation](https://publicholidays.info/country/algeria/2026). The non-official lists disagree; the SIRH must not pick one silently.

### 3.3 How movable dates are announced

1. The National Commission for Lunar Observation, under the Ministry of Religious Affairs and Wakfs, meets on the "night of doubt" and observes the crescent.
2. The Ministry of Labour, Employment and Social Security and the Directorate-General of the Civil Service (DGFP) issue a **joint communiqué** declaring which days are "chômés et payés", usually a few days before, and state both the Hijri and Gregorian dates.
3. APS and the written press publish the communiqué; employers apply it, including to hourly and daily workers, with continuity-of-service arrangements for shift work.

**SIRH design:** holidays are a *versioned data set*, not a computed calendar. Provide an admin screen to enter/confirm the official dates and an audit trail of the communiqué reference. Allow a correction to be applied retroactively to already-processed payroll (recompute, don't silently overwrite). Never auto-approve a calculated date. For Ramadan, the start and end also depend on the same observation.

### 3.4 Ramadan working hours

- **Private sector:** no general legal reduction. The employer sets the timetable by internal rules or collective agreement; a 1–2 hour reduction is common but not a statutory right. `UNVERIFIED` if a client claims a legal entitlement to reduced hours.
- **Pay:** the monthly salary is not reduced because of Ramadan hours. Hours actually worked beyond the Ramadan timetable are overtime under the normal rules.
- **Product rule:** a `ramadan_timetable` per establishment, with start/end dates driven by the same official announcement as the holidays.

### 3.5 School year, leave season and payroll cut-off

- The school year runs September–June, with the long summer break in July–August. Annual leave demand peaks in July–August, and many employers close part of August.
- Annual leave is **2.5 working days per month of work, capped at 30 calendar days per working year**; the reference period runs **1 July to 30 June** (loi 90-11, arts. 40–41). New hires start from their recruitment date. Southern wilayas get at least 10 extra days (art. 42). The leave schedule is set by the employer after consulting the participation committee (art. 51), and the leave indemnity is 1/12 of the reference-year remuneration (art. 52) ([loi 90-11, consolidated](https://www.mtess.gov.dz/fr/loi-n-90-11-du-21-avril-1990-relative-aux-relations-de-travail-page-488-rectificatif)).
- **Do not accrue leave on a calendar year.** Accrual, carry-over and the leave indemnity must follow the July–June reference year. This is one of the most common localization bugs.
- **Payroll cut-off:** the law requires pay at term (art. 88) and does not fix a monthly cut-off. Practice is a monthly cycle with the bank file sent 2–4 business days before value date. Statutory deadlines then drive the calendar: CNAS DAC within 30 days of the month/quarter end, DAS within 30 days of 31 December (30 January; often quoted as 31 January), DGI G50 by the 20th of the following month. See §9.

---

## 4. HR documents: content, signature, stamp, retention

The table is the minimum product template. "Stamp" means the employer's `cachet`; a qualified electronic seal can replace it (see §5), but the business expectation is still a visible stamp on PDFs.

| Document | When issued | Minimum content | Signed / stamped by | Language | Retention |
|---|---|---|---|---|---|
| **Bulletin de paie** (pay slip) | Monthly, with pay | Employer name, address, NIF, CNAS employer number, APE code; employee name, NAS/social-security number, position, classification; pay period; days/hours worked; base salary; every prime/indemnity itemised by nature and amount; overtime hours and rate; CNAS employee share (9%) and employer share (25% + 0.5% works fund, informative); IRG base and amount; other deductions (advances, assignments, mutual); net to pay; payment method/date. | Employer signature and stamp (practice); employee acknowledgment recommended but not a legal condition. | Arabic or French; bilingual recommended. | Keep at least 10 years to align with accounting books; payroll-specific legal retention is `UNVERIFIED` (see §5.3). |
| **Contrat de travail** (employment contract) | At hire; written for CDD, part-time, and any clause needing proof | Parties; position and classification; place of work; start date; duration and motive for CDD; trial period; remuneration and components; working time; leave; collective agreement reference; termination conditions. | Both parties; employer stamp. | Arabic or French; bilingual if the employee is Arabic-only. | Life of contract + at least 5 years after end (practice); accounting/legal retention may require longer. |
| **Avenant** (amendment) | Any change to a material term | Reference to the initial contract; changed clause; effective date; unchanged clauses. | Both parties. | Same as contract. | Attached to the contract. |
| **Attestation de travail** | On employee request (bank, visa, housing, administration) | Employer identity and address; employee identity; position; start date; still employed or end date; sometimes salary. | Employer signature + stamp. | French or Arabic; the requesting body dictates. | Copy in personnel file; 5 years minimum (practice). |
| **Attestation de salaire** | On request (credit, visa, CNAS, retirement) | Employer and employee identity; period; gross/net salary; components; CNAS number. | Employer signature + stamp. | French or Arabic. | Copy in personnel file. |
| **Attestation de travail et de salaire (ATS)** | For CNAS files; now declared/verified through the CNAS employer portal | CNAS employer number; employee NAS; employment dates; months; days worked; absences; contribution salary; signature block. | Employer signature + stamp; CNAS may require portal declaration. | French/Arabic CNAS template. | Copy 10 years (CNAS/accounting). |
| **Certificat de travail** | Mandatory at end of the employment relationship | Hire date; end date; positions held and corresponding periods. It does not replace the employer's other obligations (loi 90-11, art. 67). | Employer signature + stamp. | French or Arabic. | At least 5 years after issue; keep with personnel file. |
| **Ordre de virement** (payment order) | Each payroll run | Employer account and RIB; value date; total amount and number of beneficiaries; listing of beneficiary name, RIB, amount, motif; signatory name and capacity. | Authorised signatories per bank mandate; dual signature is common. | French (banking convention). | 10 years with accounting; bank statements 10 years. |
| **Reçu de solde de tout compte** | At termination | Components of the final settlement; leave indemnity; notice; amounts paid; acknowledgment. | Employer and employee. | French/Arabic. | 10 years. |
| **Déclaration CNAS — DAC** | Monthly if ≥10 employees, quarterly if <10; within 30 days of period end | Employer identification; period; employee list; contribution base; contributions; movement of employees. | Employer via portal (electronic), with responsible person. | French/Arabic portal. | 10 years. |
| **Déclaration CNAS — DAS** | Annually, within 30 days of 31 December (normally 30 January; often quoted as 31 January) | Nominative list; NAS; dates in/out; days/hours per quarter; salary per quarter; annual total. | Employer via portal; header + detail files. | French/Arabic portal. | 10 years. |
| **DGI G50** | Monthly by the 20th | VAT, IRG on salaries, instalments, withholding, stamp duty; period; employer identification. | Employer/representative via Jibayatic or paper at the tax office. | French/Arabic. | 10 years. |
| **DGI G29** | Annually with the tax package | State of salaries and wages paid; employee NIN; amounts. | Employer. | French/Arabic. | 10 years. |

Key legal anchors: bulletin de paie content at loi 90-11, art. 86; certificate at art. 67; pay at term at art. 88; salary paid in money at art. 85. Sanctions for not issuing a pay slip were increased to DZD 10,000–20,000 per worker (art. 148 as amended) ([loi 90-11](https://www.mtess.gov.dz/fr/loi-n-90-11-du-21-avril-1990-relative-aux-relations-de-travail-page-488-rectificatif); [Legal Doctrine on the pay slip](https://legal-doctrine.com/en/edition/la-fiche-de-paie-en-droit-algerien)).

**Product rule:** one document engine, two templates (`fr`, `ar`), one data contract. The PDF must embed the exact figures used in the bank file and the declarations; any post-validation correction creates a new version, never an in-place edit.

---

## 5. E-signature and e-archiving

### 5.1 Legal framework (as of 2026)

Algeria replaced the 2015 e-signature law with **loi n° 26-02 of 17 February 2026** on trust services for electronic transactions and electronic identification, published in JO n°14 of 18 February 2026 and in force from that date. The 2015 law (loi 15-04) is the previous framework; it is cited below only where loi 26-02 reproduces the same principle or where its transitional provisions still apply. Confirm the exact abrogation/transitional scope with counsel before relying on a 15-04 article ([loi 26-02, MPT](https://www.mpt.gov.dz/wp-content/uploads/2026/02/Loi-n%C2%B0-26-02.Services-de-Confiance.Identification-electronique.FR_.pdf); [JO n°14/2026](https://www.joradp.dz/FTP/jo-francais/2026/F2026014.pdf)).

| Point | Rule |
|---|---|
| Qualified e-signature | Only the **qualified** electronic signature is legally equivalent to a handwritten signature (loi 26-02, art. 7). |
| Other e-signatures | A signature cannot be refused as evidence solely because it is electronic, or because it is not qualified (loi 15-04, art. 9; the same principle is carried into loi 26-02). It may still be challenged on reliability. |
| E-seal | A qualified electronic seal benefits from a presumption of integrity and origin for legal persons (loi 26-02, art. 8) — the right tool for employer stamps on bulk documents. |
| Qualified certificate | Issued by an authorised trust-service provider; the national authority publishes a trusted list. |
| Timestamp | Qualified electronic timestamp is regulated as a trust service; it proves existence at a date/time and integrity. |
| E-registered mail | Qualified electronic registered delivery is regulated and gives proof of sending/receipt. |
| Trust-service providers | All data collected by trust-service providers must be hosted on Algerian territory (loi 26-02, art. 27), with transfer abroad only under the conditions of the law. |
| Consent/coercion | A person cannot be forced to perform a legal act by electronic signature only (loi 15-04, art. 3); offer a paper alternative. |

### 5.2 What a SIRH may accept

| Use case | Recommended acceptance | Legal confidence |
|---|---|---|
| Employment contract / amendment | Qualified e-signature of both parties, or wet signature + scan. Use a qualified provider on the ANCE trusted list. | High for qualified; `UNVERIFIED` for simple click-to-sign as equivalent to handwritten. |
| Bulletin de paie | Publish in the employee portal with a qualified timestamp and an audit trail; offer PDF download. Delivery by e-mail is common. | The obligation is to issue a pay slip; electronic delivery is not expressly addressed by the Labour Code. `UNVERIFIED`. |
| Employer stamp on bulk documents | Qualified electronic seal + timestamp. | High under loi 26-02. |
| Acknowledgment of receipt / policies | Simple electronic acceptance with authenticated login, timestamp, IP and document hash is good evidence. | Good evidence, not equivalent to a handwritten signature. |
| Statutory declarations (CNAS, DGI) | Use the official portal; the portal's authentication is the signature. Do not re-sign manually. | High (official channel). |
| Termination documents | Qualified signature is strongly recommended; labour disputes often turn on proof of date and content. | High for qualified; wet signature remains safest. |

**Hard product rule:** do not label a simple click or an image of a signature as "signature électronique qualifiée". Store the certificate chain, the signer's identity, the timestamp token, the document hash and the audit log. If a qualified provider is not integrated, fall back to wet signature.

### 5.3 E-archiving and legal value

No dedicated Algerian "electronic archiving" statute was identified. The relevant rules are:

- The signed electronic document must be **kept in its original electronic form**. Under the former loi 15-04 (art. 4), the modalities of conservation were set by regulation; loi 26-02 now regulates electronic documents and trust services, but the exact conservation article and implementing decree are `UNVERIFIED`. The safe design is to preserve the original bitstream, hash, signature chain and timestamp for the full retention period.
- Accounting books and supporting documents must be kept **10 years** (Code de commerce, art. 12; SCF). This covers the payroll journal, the general ledger and the documents supporting them ([Code de commerce](http://www.invest.caci.dz/fileadmin/template/recueil/pdf/Ord_75-59.pdf)).
- A scanned paper copy has no automatic statutory equivalence to the original; case law and the administration may accept it, but this is `UNVERIFIED`. Keep the paper original for documents where the law requires an original (e.g. notarised acts, some registrations).
- A qualified e-archive should preserve: original bitstream, format, hash, signature/certificate chain, timestamp, audit trail, access log, and the ability to render it for the full retention period.

**Retention recommendation:** 10 years for payroll, declarations and accounting; life of contract + 10 years for contracts; 10 years after termination for personnel files. The often-quoted "5 years" for payroll documents is not clearly grounded in an Algerian text — treat it as a minimum and keep 10 years.

---

## 6. Data protection and hosting

### 6.1 Framework

- **Loi n° 18-07 of 10 June 2018**, amended and supplemented by **loi n° 25-11 of 24 July 2025**, is the general personal-data law. It applies to public and private controllers established in Algeria or using automated means located in Algeria ([loi 18-07, ANPDP](https://anpdp.dz/wp-content/uploads/2023/01/2.1-Loi-N%C2%B018-07-2.pdf); [loi 25-11, JO n°48/2025](https://www.douane.gov.dz/IMG/pdf/loi_18-07_du_24_07_2025_fr_dz.pdf)).
- The regulator is the **ANPDP** (Autorité nationale de protection des données à caractère personnel), operational since August 2023, with an online portal and regional inspection units ([ANPDP](https://anpdp.dz/); [Gide overview, 1 July 2026](https://www.gide.com/en/news-insights/protection-of-personal-data-focus-on-algerian-regulations/)).

### 6.2 Registration and authorisation

| Processing | Regime |
|---|---|
| Ordinary HR/payroll processing | **Prior declaration** to the ANPDP (loi 18-07, art. 12), receipt issued immediately or within 48 hours. |
| Processing presenting manifest risks | ANPDP may convert the declaration into an **authorisation** (art. 17); decision within 10 days. |
| Sensitive data (health, biometrics, political, religious, etc.) | **Prior authorisation** (art. 18); the ANPDP publishes a specific form. |
| Interconnection of files | **Prior authorisation** (arts. 14 and 19). |
| Transfer abroad | **Prior authorisation** (art. 44), plus adequacy in the destination country or an art. 45 derogation. |
| Biometric attendance | **Prior authorisation** required; no employee consent needed for HR management; retention limited to the employment relationship (ANPDP Decision n°03 of 6 May 2026, summarised by Gide). |
| Video surveillance at work | Prior declaration, purpose limited to security of persons and property, transparency and security obligations (ANPDP Decision n°02 of 4 March 2026). |
| Pre-employment drug test results | Health data; declaration regime; retention limited to 3 months (ANPDP Decision n°01 of 25 February 2026). |

Every controller must designate a **DPO** and communicate their contact to the ANPDP (loi 25-11, inserting arts. 41 bis et seq.; ANPDP Decision n°01 of 24 December 2025). It must also keep a **register of processing activities** and an automated log of operations.

### 6.3 Employee rights and retention

- Rights: information, access, rectification, objection; erasure is limited to unlawful/unnecessary data. Requests are free; the controller must respond within the statutory delay (10 days for rectification under art. 35).
- Retention: data must not be kept beyond the stated purpose. For HR, the employment relationship plus the legal retention period (10 years for payroll/accounting) is the defensible rule. Biometric attendance is limited to the duration of the employment relationship (Decision 03/2026).
- Consent: not the right basis for payroll (legal obligation/contract). Consent is required for optional processing (e.g. marketing, photos, some wellness data). Do not bundle consent into the employment contract.

### 6.4 Breach handling

- The controller must notify the ANPDP **within 5 days** of becoming aware of a personal-data breach (loi 25-11, new art. 45 bis 8), with the nature, consequences and measures taken; late notification must explain the delay.
- Individuals must be notified where the breach is likely to create a high risk to their rights and freedoms (art. 45 bis 10).
- Service providers on public electronic communications networks must notify "without delay" under art. 43.
- Keep an inventory of breaches and remedial measures (art. 43).

### 6.5 Hosting and transfer abroad

| Question | Answer |
|---|---|
| Must a private employer host HR data in Algeria? | **No general local-hosting mandate** in loi 18-07. The law controls *transfer abroad*, not the location as such. Transfer requires ANPDP authorisation and an adequate protection level, or an art. 45 derogation. |
| Can a SIRH use a foreign SaaS? | Yes, but the transfer must be authorised; the contract must include the art. 39 processor clauses; the ANPDP must be able to inspect; breach notification and DPO apply. Criminal penalties for unlawful transfer: 1–5 years and DZD 500,000–1,000,000 (art. 67). |
| Trust-service providers | Must host collected data in Algeria (loi 26-02, art. 27). If the SIRH uses a qualified signature/timestamp provider, that provider must be locally hosted/authorised. |
| Sector-specific | Banking, health, insurance and defence have additional localisation/security rules. `UNVERIFIED` in detail; check the sector regulator. |

**Design implication:** make hosting region a per-tenant configuration, with a hard block on cross-border transfer unless an ANPDP authorisation reference is recorded. Log every export that contains personal data.

---

## 7. Accessibility and language of legal documents

### 7.1 Accessibility

- Loi n° 02-09 of 8 May 2002 protects and promotes persons with disabilities and includes accessibility to **information and communication** (art. 30), alongside the built environment and transport ([loi 02-09, JO n°34/2002](https://www.joradp.dz/FTP/jo-francais/2002/F2002034.PDF)).
- No Algerian decree was found that mandates WCAG for private web applications. Digital accessibility is therefore a **policy/quality requirement**, not a directly enforceable SIRH rule. `UNVERIFIED` for public procurement, where accessibility clauses may be imposed.
- Recommended baseline: WCAG 2.2 AA, keyboard navigation, visible focus, 4.5:1 contrast, 200% zoom, screen-reader labels in Arabic and French, no colour-only status, accessible PDFs (tagged, reading order, language attributes) and an HTML alternative for legal documents.
- Arabic accessibility specifics: correct `lang="ar"`, logical reading order in RTL, accessible names for icon buttons, and no images of text.

### 7.2 Which documents must be in Arabic

| Document | Language rule | Confidence |
|---|---|---|
| Court filings, exhibits, judgments | Arabic, or Arabic + official translation; otherwise inadmissible (loi 08-09, art. 8). | LAW |
| Official administrative documents, reports, minutes of public administrations, institutions, enterprises and associations | Arabic under loi 91-05, art. 5; application suspended/deferred since 1992, so bilingual practice dominates. | LAW but unevenly enforced |
| Acts (actes) | Arabic exclusively under loi 91-05, art. 6; registration/publicity refused if not in Arabic. | LAW but unevenly enforced |
| Employment contract | No language requirement in loi 90-11. Arabic or French both valid; bilingual recommended. An Arabic-only employee must be able to understand it. | LAW silent / PRACTICE |
| Bulletin de paie | No language requirement; must itemise every element (art. 86). Arabic or French; bilingual recommended. | LAW silent / PRACTICE |
| CNAS / DGI / labour-inspection forms | Official templates are Arabic/French; use the official bilingual form where provided. | PRACTICE |
| Internal policies, HR portal | Employer's choice; bilingual is the safe default. | PRACTICE |

**Translation obligations:** for court, an official translation by a sworn translator is required. For administration, an Arabic version may be demanded; French is usually accepted in practice. Do not promise that a French-only document is legally sufficient for every administration. `UNVERIFIED` whether an Arabic translation prevails over the French text in a private contract; state the prevailing language explicitly in the contract.

**Product rule:** every generated document carries a `language` and a `prevailing_language` field when bilingual. The PDF footer states which version prevails. The employee can choose the portal language independently of the document language.

---

## 8. Payments and banking

### 8.1 Payment methods and legality

| Method | Status | Notes |
|---|---|---|
| Bank transfer (virement) | Standard for salaries, especially larger employers. | Requires a RIB per employee; bank file or portal. |
| CCP / Algérie Poste (Baridi) | Legal and widely used, especially for smaller employers and employees without a bank account. | `RIP`/CCP number; 20-digit structure with bank code `007`, agency `99999`. |
| Cheque | Legal, but impractical for mass payroll. | Traceable; not used for monthly salary runs at scale. |
| Cash | Not prohibited by the Labour Code; salary must be paid in money (art. 85). | Discouraged; no proof of payment, CNAS/IRG risk. Cash restrictions apply to specific transactions (real estate, vehicles, boats, compulsory insurance) and B2B payments above DZD 1,000,000 (LF 2024, art. 116). Salary is not one of the listed banned categories, but a cash salary above the B2B threshold could be requalified. `UNVERIFIED` for salary specifically. |
| Payment card / e-wallet | Possible for advances or expenses, not a standard salary method. | Edahabia/CIB cards are widespread. |

**Product rule:** support bank and CCP as first-class methods; keep "cash" as a legacy method with a mandatory receipt/acknowledgment and a warning. Never generate a bank file without validating the RIB key.

### 8.2 RIB / CCP structure

Bank of Algeria Instruction n°06-2004 standardises the bank account number and the RIB:

```
BBB AAAAA CCCCCCCCCC XX
 3    5        10      2   = 20 digits
```

- `BBB` = bank code (001 BNA, 002 BEA, 003 BADR, 004 CPA, 005 BDL, 006 Al Baraka, 007 CCP, 008 Trésor, 011 CNEP, 021 Société Générale, 027 BNP Paribas, 032 AGB, etc.).
- `AAAAA` = agency code, assigned by the bank.
- `CCCCCCCCCC` = individual account number.
- `XX` = control key, computed by **modulo 97**: concatenate the first 18 digits, multiply by 100, divide by 97, key = 97 − remainder.
- For CCP: bank code `007`, agency `99999`, then the 10-digit CCP account.

Sources: [Bank of Algeria Instruction 06-2004](https://www.bank-of-algeria.dz/stoodroa/2021/03/instruction062004.pdf); [RIB validator/structure](https://www.babalweb.net/fr/finance/verificateur-rib-algerie.php).

### 8.3 Payroll transfer files

- The de facto interbank standard is **VIR.EDI**: a fixed-width text file with a `VIRM` header (ordering bank, operation type `010`, currency `0` for dinars, ordering RIB, ordering name), one line per beneficiary (sequence number, RIB, amount on 15 characters with implied 2 decimals, 70-character label), and an `FVIR` trailer. Example: `000000000500065` = 5,000.65 DA ([VIR.EDI structure](https://dlg-net.com/docs/pcpaiew/help/VIREMENT_BANCAIRE_SUR_SUPPORT_INFORMATIQUE_STD_STRUCTURE.htm)).
- Many banks also accept CSV/XLSX through their corporate portals (BNA Corporate, BEA e-bea Corporate, CPA, BDL, CNEP, AGB, Société Générale `Vir-Express`). The column set is usually `RIB;Bénéficiaire;Montant;Motif`, UTF-8, semicolon-separated. Treat this as a per-bank adapter, not a single standard.
- The **ordre de virement** is the signed instruction; the file is its attachment. Both must carry the same total and beneficiary count. Dual control (maker/checker) is standard.

### 8.4 Bank domiciliation

- Employers may require a RIB for transfer, but cannot unilaterally open an account for an employee. The employee provides the RIB and can change it; keep a signed mandate/consent for the salary domiciliation.
- Private employers pay through commercial banks; some employees are paid through CCP. Support both.
- Salary assignment/cessation (cessions sur salaire) must be handled as a deduction with a legal basis and a cap; see `01-payroll-costisation.md`.

---

## 9. Integrations

### 9.1 CNAS — tele-declaration

| Flow | Frequency / deadline | Format / channel |
|---|---|---|
| Affiliation/immatriculation of a new employee | Within **10 days** of recruitment (loi 83-14 of 2 July 1983, art. 10) | CNAS employer portal; employee identity, NAS, date of recruitment, position, wilaya/commune of birth. |
| DAC — declaration of contribution base | Monthly if ≥10 employees, quarterly if <10; within **30 days** after the period (art. 21) | Portal; contribution base, employee list, movement. |
| DAS — annual declaration of salaries and employees | Within **30 days of 31 December** (normally 30 January; often quoted as 31 January) — art. 14 | Portal; two fixed-width files: `Entête` (employer) and `Détail` (employees). Fields include employer number, reference year, line number, NAS + key, name, birth date, quarterly duration + unit (M/J/H), quarterly salary, annual salary, entry/exit dates, observation. |
| ATS — attestation de travail et de salaire | On need | Portal declaration; CNAS template AS8. |
| Work accident | Within **48 hours** of knowledge | CNAS portal. |
| Payment of contributions | With the DAC | E-payment / e-banking on the portal. |

Sources: [CNAS tele-declaration portal](https://teledeclaration.cnas.dz/); [official guide](https://teledeclaration.cnas.dz/pdf/Guide%20TELE-DECLARATION.pdf); [CNAS digital services](https://cnas.dz/fr/nos-services-numeriques); [CNAS employer page](https://cnas.dz/fr/employeur).

Portal authentication now uses **2FA by SMS/e-mail**, so the SIRH cannot fully automate the submission without a human or a secure credential vault. Design a "prepare → export → upload → reconcile receipt" workflow, not a silent API.

### 9.2 DGI — G50 and G29

| Flow | Frequency / deadline | Channel |
|---|---|---|
| G50 — monthly declaration of VAT, IRG on salaries, instalments, withholding, stamp duty | From the 1st to the **20th** of the following month (or quarter, depending on regime) | Jibayatic (`jibayatic.mf.gov.dz`) or paper at the tax office. E-payment available since 25 July 2026 via CIB/Edahabia card or bank transfer. |
| G29 — annual state of salaries | With the annual tax package (usually by 30 April) | DGI portal / paper. |
| G12 / G12 bis — IFU | Annual, 20 January / 30 June depending on regime | Jibayatic. |

Sources: [DGI declaration forms](https://www.mfdgi.gov.dz/fr/espace-telechargements/formulaires-declaration); [Jibayatic documentation](https://mfdgi.gov.dz/portailpublic/documentation.html); [DGI communiqué on G50](https://mfdgi.gov.dz/fr/a-propos/actu-fr/souscription-g12bis-g50ter-g50-fr).

**Product rule:** the G50 line "IRG salaires" must reconcile exactly with the payroll journal for the month. Keep the Jibayatic receipt (timestamped) with the payroll run. Do not compute the G50 from a different base than the one used for the pay slips.

### 9.3 CACOBATPH (BTPH sector)

Employers in construction, public works and hydraulics also declare a **DAS** to CACOBATPH, with a reference year running **1 July–30 June**, due by **31 July**. It can be filed via `tasrihatcom.dz` or the CACOBATPH DAS software. The DAS is the basis for paid-leave contributions and bad-weather unemployment. Penalties for late filing: 15% of contributions plus 5% per month ([CACOBATPH DAS](https://www.cacobatph.dz/das?lang=fr)). This is a separate integration from CNAS and must not be forgotten for BTPH clients.

### 9.4 Biometric devices

- Common in Algeria: ZKTeco, Suprema, Hikvision and generic fingerprint/face terminals, often standalone with a USB/TCP export of attendance logs. This is field observation, not an official list. `UNVERIFIED` as a market-share claim.
- Legal constraint: biometric attendance requires **prior ANPDP authorisation** (Decision n°03 of 6 May 2026), information of employees, security measures, and retention limited to the employment relationship. Employee consent is not the legal basis.
- Product rule: support CSV import from the major terminals, but keep the biometric template out of the SIRH database where possible; store only the attendance event and the device ID. If the SIRH stores templates, it becomes a biometric processor and needs its own authorisation.
- Provide a non-biometric fallback (badge, PIN, mobile geolocation with consent) because some employees will refuse fingerprint/face.

### 9.5 ERP / accounting exports

- The accounting framework is the **SCF** (Système Comptable Financier, loi 07-11), mandatory since 1 January 2010. Payroll accounts: `42` personnel, `421` salaries payable, `431` social security, `442` IRG, etc. The payroll journal must reconcile to the general ledger.
- Export formats: SCF-compliant journal entries (CSV/XLSX), `journal de paie`, `livre de paie`, and the CNAS/DGI files. Keep the payroll journal immutable after closing; corrections go through a new entry.
- Retention: 10 years for books and supporting documents (Code de commerce, art. 12).

---

## 10. SIRH implications

### 10.1 i18n architecture

- **Locale is a first-class entity per company and per establishment**, not a global setting. A group may have an Arabic-first subsidiary and a French-first one.
- Separate four things that are often conflated:
  1. `ui_locale` (ar/fr, plus optional ber) — the language of menus, labels, validation messages.
  2. `document_locale` (ar/fr, bilingual) — the language of generated PDFs.
  3. `format_locale` (`ar-DZ` / `fr-DZ`) — number, date, currency formatting.
  4. `legal_jurisdiction` — Algeria, with per-sector variations (BTPH).
- Translation keys must be stable and versioned; payroll terms need a review by an Algerian payroll expert, not machine translation. Keep a glossary table in the database and use it for both UI and document templates.
- RTL is a layout mode, not a translation. Test every screen with Arabic data and French data, including mixed names and RIBs.
- Do not translate statutory codes (CNAS, IRG, DAS, G50, RIB, NIF, NAS); keep the acronym and add a local-language gloss.

### 10.2 Seed data

| Data set | What to seed | Update mechanism |
|---|---|---|
| Public holidays | 14 legal days per year; fixed dates; religious dates as `A CONFIRMER` until the official communiqué; employee-specific Christian days (Easter Monday, Ascension, 15 Aug, 25 Dec) and Jewish days (Roch Achana, Yom Kippur, Pesach) as opt-in entitlements. | Admin confirmation screen with communiqué reference; audit trail; retroactive correction. |
| Ramadan timetable | Per establishment; start/end from the official announcement; hours. | Admin screen; effective-dated. |
| Weekend pattern | Per establishment; default Fri–Sat. | Company/establishment setting. |
| CNAS parameters | Rates (employee 9%; employer 25% + 0.5% works fund = 25.5%; total 34.5%), ceiling/base rules, contribution categories. | Versioned by effective date; source URL. |
| IRG brackets | Annual/monthly brackets, 40% abatement, smoothing; effective date. | Versioned; source = Finance Law. |
| SNMG | Monthly amount; effective date. | Versioned. |
| Leave rules | 2.5 days/month, 30-day cap, 1 July–30 June reference year, +10 days South. | Configurable per collective agreement. |
| Overtime | +50% minimum; 20% cap; night 21:00–05:00. | Configurable by agreement. |
| Bank codes | 3-digit bank codes and names; RIB key algorithm. | Reference table; source Bank of Algeria. |
| Document templates | Bulletin, contract, attestations, certificate, ATS, payment order. | Per locale; versioned. |
| Glossary | FR ↔ AR HR/payroll terms. | Reviewed by payroll expert. |

### 10.3 Per-company locale and formatting rules

- Store `currency = DZD` at company level; never allow a payroll run in another currency without an explicit expatriate exception.
- Store `decimal_separator`, `thousands_separator`, `date_format`, `time_format` as company settings, defaulting to `,` / space / `dd/MM/yyyy` / 24h.
- Store `weekend_days`, `working_days`, `ramadan_hours`, `holiday_calendar_id`.
- Store `document_language` and `prevailing_language`; print both on bilingual documents.
- Store `data_region` and `transfer_authorisation_ref`; block cross-border export without a reference.
- Store `signature_policy` (qualified / simple / wet) per document type; default to qualified for contracts and termination, wet fallback.

### 10.4 Checklist before go-live

**Legal and data**

- [ ] ANPDP declaration filed for HR/payroll processing; receipt stored.
- [ ] Specific authorisation filed for biometric attendance (if used), video surveillance (if used), and any transfer abroad.
- [ ] DPO designated and communicated to the ANPDP.
- [ ] Register of processing activities and automated log in place.
- [ ] Processor contract with the art. 39 clauses for any SaaS/subprocessor.
- [ ] Breach procedure with a 5-day notification clock and a named owner.
- [ ] Retention schedule: payroll/accounting 10 years; biometric data deleted at end of employment; recruitment data deleted after the statutory period.
- [ ] Hosting region and transfer-authorisation reference recorded.

**Localization**

- [ ] Arabic and French UI complete; RTL tested on every screen; mixed-direction forms tested with real names and RIBs.
- [ ] Arabic font embedded in PDFs; no missing glyphs; no Arabic-Indic digits by default.
- [ ] Numbers, dates, currency and negatives consistent across UI, PDF and exports.
- [ ] `Africa/Algiers` used everywhere; no DST jobs.
- [ ] Glossary reviewed by an Algerian payroll expert; statutory acronyms untranslated.
- [ ] Document templates approved by an Algerian labour-law adviser; bilingual versions state the prevailing language.

**Calendar and payroll**

- [ ] 2026 holidays loaded with `A CONFIRMER` flags; Eid al-Adha 27–29 May confirmed; official communiqué reference stored.
- [ ] Leave accrual on 1 July–30 June, not calendar year; 30-day cap; South +10 days.
- [ ] Ramadan timetable per establishment; no pay reduction.
- [ ] Weekend per establishment; overtime rules applied to Friday/Saturday correctly.
- [ ] Payroll cut-off aligned with bank value date; CNAS DAC, DGI G50, DAS and CACOBATPH deadlines in the calendar.

**Documents and signature**

- [ ] Bulletin de paie contains every art. 86 element and reconciles to the bank file and declarations.
- [ ] Contract, attestation, certificate, ATS and payment order templates complete.
- [ ] Qualified e-signature/e-seal provider on the ANCE trusted list; certificate chain and timestamp stored.
- [ ] Wet-signature fallback for employees who cannot or will not sign electronically.
- [ ] Document versioning: no in-place edits after validation; corrections create a new version.

**Integrations**

- [ ] CNAS portal workflow (prepare → upload → receipt → reconcile) with 2FA handling.
- [ ] DGI Jibayatic G50/G29 workflow and receipt storage.
- [ ] CACOBATPH DAS for BTPH clients.
- [ ] Bank adapters for VIR.EDI and the client's bank portal; RIB modulo-97 validation.
- [ ] Biometric import with device mapping and no template storage unless authorised.
- [ ] SCF payroll journal export and reconciliation to the general ledger.

---

## Sources

All URLs retrieved **7 November 2026**. Where a PDF is cited, the citation is to the official Journal Officiel or the issuing ministry's copy.

1. Constitution of Algeria 2020 (JO n°82, 30 Dec 2020) — https://www.joradp.dz/FTP/JO-FRANCAIS/2020/F2020082.pdf ; https://cour-constitutionnelle.dz/2023/05/06/constitution
2. Loi n° 91-05 of 16 Jan 1991 on the generalisation of Arabic — https://www.joradp.dz/JO8499/1991/003/Fp38.pdf
3. Décret présidentiel n° 92-303 of 4 July 1992 (implementation of loi 91-05) — https://www.axl.cefan.ulaval.ca/afrique/algerie_decret-92-303-1992.htm
4. Loi n° 08-09 of 25 Feb 2008, code de procédure civile et administrative — https://droit.mjustice.gov.dz/sites/default/files/loi_fr_08-09.pdf
5. Loi n° 90-11 of 21 Apr 1990 on labour relations (consolidated) — https://www.mtess.gov.dz/fr/loi-n-90-11-du-21-avril-1990-relative-aux-relations-de-travail-page-488-rectificatif
6. Loi n° 63-278 of 26 July 1963 fixing the list of legal holidays — https://www.joradp.dz/FTP/jo-francais/1963/F1963053.pdf
7. Loi n° 23-10 of 26 June 2023 amending loi 63-278 (three-day Eids) — https://www.joradp.dz/FTP/jo-francais/2023/F2023043.pdf
8. Compilation of holiday texts (loi 18-12, loi 05-06, ordonnance 68-419) — https://portailjuridique.esi.dz/fran%C3%A7ais/f%C3%AAtes-et-cong%C3%A9s-l%C3%A9gales
9. Ministry of Labour, Employment and Social Security — labour legislation and legal holidays — https://www.mtess.gov.dz/fr/legislation-du-travail
10. APS, 24 May 2026 — Eid al-Adha 2026 (27–29 May) joint communiqué — https://www.aps.dz/fr/algerie/societe/mpjo2nai-les-journees-du-mercredi-jeudi-et-vendredi-prochains-chomees-et-payees
11. *(public sector — out of scope)* APS, 17 Feb 2026 — Ramadan 2026 school/public-sector hours — https://www.aps.dz/fr/algerie/education-et-technologie/mlqg3zg0-le-ministere-de-l-education-annonce-les-horaires-de-travail-dans-les-etablissements-educatifs
12. L'Expression, 17 July 2026 — Ramadan timetable note n°2 of 16 Feb 2026 — https://www.lexpressiondz.com/nationale/des-horaires-amenages-durant-le-mois-sacre-402997
13. Loi n° 15-04 of 1 Feb 2015 on electronic signature and certification — https://www.mpt.gov.dz/wp-content/uploads/2023/11/Loi-n%C2%B015-04.pdf ; https://www.douane.gov.dz/IMG/pdf/loi_no_15-04_du_1er_fevrier_2015_fixant_les_regles_generales_relatives_a_la_signature_et_a_la_certification_electroniques.pdf
14. Loi n° 26-02 of 17 Feb 2026 on trust services and electronic identification (JO n°14, 18 Feb 2026) — https://www.mpt.gov.dz/wp-content/uploads/2026/02/Loi-n%C2%B0-26-02.Services-de-Confiance.Identification-electronique.FR_.pdf ; https://www.joradp.dz/FTP/jo-francais/2026/F2026014.pdf
15. Loi n° 18-07 of 10 June 2018 on personal data protection — https://anpdp.dz/wp-content/uploads/2023/01/2.1-Loi-N%C2%B018-07-2.pdf ; https://www.joradp.dz/FTP/jo-francais/2018/F2018034.pdf
16. Loi n° 25-11 of 24 July 2025 amending loi 18-07 — https://www.douane.gov.dz/IMG/pdf/loi_18-07_du_24_07_2025_fr_dz.pdf
17. ANPDP — official site and declaration guides — https://anpdp.dz/ ; https://anpdp.dz/wp-content/uploads/2023/08/guide_declaration_traitement_V1.0.pdf
18. Gide, "Personal Data Protection: An Overview of Algerian Regulations", 1 July 2026 (ANPDP decisions on DPO, health data, video surveillance, biometric attendance) — https://www.gide.com/en/news-insights/protection-of-personal-data-focus-on-algerian-regulations/
19. CNAS — tele-declaration employer portal — https://teledeclaration.cnas.dz/
20. CNAS — official tele-declaration guide (DAC/DAS file formats, ATS) — https://teledeclaration.cnas.dz/pdf/Guide%20TELE-DECLARATION.pdf
21. CNAS — digital services — https://cnas.dz/fr/nos-services-numeriques
22. CNAS — employer obligations (affiliation, DAS, contributions) — https://cnas.dz/fr/employeur
23. DGI — declaration forms (G50, G50 TER, G29) — https://www.mfdgi.gov.dz/fr/espace-telechargements/formulaires-declaration
24. DGI — Jibayatic documentation — https://mfdgi.gov.dz/portailpublic/documentation.html
25. DGI — communiqué on G50/G50 TER/G12 bis — https://mfdgi.gov.dz/fr/a-propos/actu-fr/souscription-g12bis-g50ter-g50-fr
26. CACOBATPH — DAS (BTPH) — https://www.cacobatph.dz/das?lang=fr
27. Bank of Algeria — Instruction n°06-2004 on the bank account number and RIB — https://www.bank-of-algeria.dz/stoodroa/2021/03/instruction062004.pdf
28. VIR.EDI — payroll transfer file structure — https://dlg-net.com/docs/pcpaiew/help/VIREMENT_BANCAIRE_SUR_SUPPORT_INFORMATIQUE_STD_STRUCTURE.htm
29. CLDR — `ar-DZ` numbers — https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/ar-DZ/numbers.json
30. CLDR — `fr-DZ` numbers — https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/fr-DZ/numbers.json
31. CLDR — `ar-DZ` currencies and dates — https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-numbers-full/main/ar-DZ/currencies.json
32. Time.is — Algeria time zone (Africa/Algiers, no DST since 1981) — https://time.is/fr/Algeria
33. Timeanddate — Algeria DST history — https://www.timeanddate.com/time/change/algeria?year=1980
34. Code de commerce (ordonnance 75-59), art. 12 — 10-year retention — http://www.invest.caci.dz/fileadmin/template/recueil/pdf/Ord_75-59.pdf
35. Loi n° 02-09 of 8 May 2002 on persons with disabilities — https://www.joradp.dz/FTP/jo-francais/2002/F2002034.PDF
36. *(public sector — out of scope)* Décret exécutif n° 09-244 of 22 July 2009 (Friday–Saturday weekend, public sector) — https://www.joradp.dz/FTP/jo-francais/2009/F2009044.pdf
37. Loi n° 07-11 of 25 Nov 2007 (SCF) and Treasury presentation — https://tresor.mf.gov.dz/systeme-comptable-financier
38. Décret présidentiel n° 25-320 of 30 Dec 2025 (national data governance) — secondary report: https://lechodalgerie.dz/gouvernance-des-donnees-un-cadre-national-officiellement-instaure-un-decret-presidentiel-pour-renforcer-la-souverainete-numerique
39. Legal Doctrine — the pay slip in Algerian law — https://legal-doctrine.com/en/edition/la-fiche-de-paie-en-droit-algerien
40. Loi n° 83-14 of 2 July 1983 on social-security obligations (JO n°28/1983) — https://www.joradp.dz/FTP/jo-francais/1983/F1983028.pdf

---

## Open questions / UNVERIFIED

1. **Electronic pay slip.** Does delivery of the bulletin de paie by e-mail/portal satisfy loi 90-11 art. 86 without a wet or qualified signature? No express text found. Default to a qualified timestamp + employee portal acceptance, and offer a printable PDF; confirm with counsel.
2. **Electronic employment contract.** Loi 90-11 requires writing for CDD but is silent on electronic form. Loi 26-02 makes a qualified e-signature equivalent to handwritten, but no labour-specific text confirms acceptance by the labour inspectorate. Default to qualified signature + wet fallback.
3. **Scanned paper value.** No Algerian text found that gives a scanned copy the same probative value as the original. Keep originals for documents where the law requires an original; treat scans as evidence, not as the legal original.
4. **Payroll-specific retention.** The 10-year accounting retention is clear; a specific payroll-document retention (often quoted as 5 years) is not clearly grounded. Use 10 years.
6. **French/Arabic prevailing language in private contracts.** Loi 91-05 says Arabic for official acts, but its application is suspended and bilingual practice is widespread. No clear rule on which version prevails in a private employment contract; state it expressly.
7. **2026 religious dates.** Only Eid al-Adha (27–29 May) was confirmed by a retrieved official communiqué. Eid al-Fitr, 1 Muharram, Achoura and Mawlid remain `A CONFIRMER`; sources disagree by 1–5 days. Do not hard-code.
8. **Ramadan private-sector hours.** No general legal reduction; employer practice varies. Confirm with the client's collective agreement.
9. **Cash salary.** The Labour Code does not ban it, but LF 2024 art. 116 (B2B > DZD 1,000,000) and LF 2025 art. 207 (specific transactions) create traceability pressure. Whether a cash salary above the threshold is lawful is `UNVERIFIED`; recommend bank/CCP.
10. **VIR.EDI official status.** The format is the de facto interbank standard described by banking-software vendors; no Bank of Algeria instruction retrieved that mandates it. Validate with the client's bank.
11. **Biometric vendor market share.** ZKTeco/Suprema/Hikvision are commonly seen in the field, but no official statistics were found. Treat as observation, not market data.
12. **Digital accessibility standard.** Loi 02-09 covers accessibility to information and communication, but no WCAG-equivalent decree for private web apps was found. Use WCAG 2.2 AA as a quality baseline.
13. **Hijri display.** Algerian official communiqués give both Hijri and Gregorian dates; there is no single national Hijri calendar library. Do not compute; store the official date.
14. **ANPDP fees and processing times.** The law sets 2 months (extendable to 4) for authorisation and 48 hours for a declaration receipt; actual practice and any fees should be checked on the ANPDP portal before committing to a go-live date.
