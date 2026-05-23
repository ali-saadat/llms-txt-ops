# العربية (ar) — Arabic

Arabic business communication conventions. Arabic is right-to-left (RTL) and has significant variation between Modern Standard Arabic (MSA) used in formal/written business, and dialects (Egyptian, Levantine, Gulf, Maghreb) used informally. Business email defaults to MSA.

## Variant matters

- **MSA (Modern Standard Arabic / الفصحى)** — universal for written business, news, formal contexts. Use this for emails.
- **Dialects** — Egyptian (Cairo), Levantine (Lebanon/Syria/Jordan/Palestine), Gulf (UAE/Saudi/Kuwait/Qatar), Maghrebi (Morocco/Algeria/Tunisia). Spoken; rarely written formally.
- **Many business emails in Arab tech contexts code-switch with English**, especially in Gulf states (UAE, Saudi, Qatar).

## RTL formatting

Arabic text reads right-to-left. When mixing with English (URLs, technical terms), most modern email clients handle bidirectional rendering correctly. But:

- llms.txt content stays LTR (it's markdown, technically-flavored)
- Stakeholder emails in Arabic flow RTL
- Tables in Arabic-language docs need careful formatting

## Formality calibration

| Context | Formality |
|---|---|
| Close colleagues | "السلام عليكم" (greeting) + first name |
| Cross-functional thread | "السلام عليكم" + "السيد/السيدة [Name]" |
| Senior / management | "سيدي الفاضل" / "سيدتي الفاضلة" + Name |
| External / vendor | Full formal with title and family name |
| Gulf business | Often more formal; mix English freely |
| Egyptian business | Generally more conversational |

## Honorifics and titles

- **السيد (al-sayyid)** — Mr.
- **السيدة (al-sayyida)** — Mrs./Ms.
- **الأستاذ (al-ustāz)** — Sir / Professor / form of respect for educated/professional people (very common)
- **الدكتور (al-doctor)** — Dr. (always use if applicable)
- **المهندس (al-muhandis)** — Engineer (used as a title in Arab business culture)
- **الشيخ (al-shaykh)** — religious or tribal title; not used in normal business

Critical: **professional titles are very important in Arab business culture**. Engineer (المهندس) and Doctor (الدكتور) are titles used in everyday business address, not just in formal contexts.

## Greeting conventions

The opening greeting differs by religious/secular preference:

- **السلام عليكم** (as-salām ʿalaykum, "peace be upon you") — Islamic but used broadly in Arab business; standard
- **تحياتي** (taḥiyyātī, "my greetings") — secular alternative
- **مرحبا** (marḥabā, "hello") — more informal
- **صباح الخير** (ṣabāḥ al-khayr, "good morning") — time-specific

After the greeting, customary to wish health: "أتمنى لكم يوماً سعيداً" or "آمل أن تكونوا بخير".

## Common business email phrases

| Purpose | العربية |
|---|---|
| Opening thanks | "أشكركم على المراجعة الدقيقة والتعليقات القيمة" |
| Acknowledging concern | "أود معالجة هذه النقطة مباشرة" |
| Presenting findings | "فيما يلي نتائج التحقق الذي أجريناه" |
| Honest framing | "أود أن أكون شفافاً بشأن ما يعنيه النجاح في هذا السياق" |
| Citing evidence | "وفقاً لدراسة SE Ranking (300 ألف نطاق، نوفمبر 2025)..." |
| Closing offer | "أبقى رهن إشارتكم لأي استفسار" |
| Polite disagreement | "أرى الأمر بشكل مختلف قليلاً، حيث..." |

## Closing patterns

| Formality | Arabic | Transliteration |
|---|---|---|
| Standard formal | مع أطيب التحيات | maʿa aṭyab at-taḥiyyāt — "with the best regards" |
| Formal | تفضلوا بقبول فائق الاحترام | tafaḍḍalū bi-qabūl fāʾiq al-iḥtirām — "please accept the highest respect" |
| Common | شكراً جزيلاً | shukran jazīlan — "many thanks" |
| Religious-friendly | جزاكم الله خيراً | jazākum allāh khayran — "may God reward you with good" |
| Standard sign-off | مع تحياتي | maʿa taḥiyyātī — "with my regards" |

## Honest-expectations opening (translated)

> "قبل الاستمرار، أود تحديد توقعات واقعية حول ما سيفعله ملف llms.txt وما لن يفعله — لأن ثلاث دراسات مستقلة (SE Ranking بـ 300 ألف نطاق، OtterlyAI بـ 90 يوماً من سجلات الخادم، Search Engine Land باختبار 10 مواقع) لم تجد أي زيادة قابلة للقياس في الاستشهادات بالذكاء الاصطناعي."

## Three-reasons framing (translated)

> "ثلاثة أسباب تصمد أمام التدقيق: (1) استبدال ملف موجود معطل هو تحسين واضح، (2) الملف يخدم أيضاً كأساس داخلي لعملنا الخاص في الذكاء الاصطناعي، (3) التوافق المستقبلي لا يكلفنا شيئاً. الحالة دفاعية، وليست هجومية."

## Date and number formats

- Date: `15/05/2026` (DD/MM/YYYY) common
- Date Arabic: `٢٠٢٦/٠٥/١٥` (using Arabic-Indic digits) — formal context
- Numbers: Western digits (1234) common in business; Arabic-Indic (١٢٣٤) in formal Arabic-only documents
- Currency: varies by country — AED, SAR, EGP, KWD, etc.

## Cultural notes

- **Greetings are extended** — Arab business culture spends more time on personal acknowledgment ("How are you?", "How is your family?") before getting to the point
- **Religious-secular calibration** — assess whether to include religious phrases. Many businesspeople prefer secular forms; some appreciate religious framings. Default to secular unless you know the recipient's preference.
- **Family/tribe references** — particularly in Gulf, asking about family is normal small talk
- **Time-zone and prayer awareness** — meetings around prayer times (5 daily) are scheduled to avoid conflicts; Ramadan affects business hours
- **Friday is the weekend day** in most Arab countries (Saturday + Sunday for most Gulf states now, except Saudi Arabia which moved to Saturday-only weekend)
- **Code-switching with English** is common in tech contexts, particularly Gulf cities (Dubai, Riyadh, Abu Dhabi, Doha)
- **Names**: Arab names follow father-first patterns ("Ahmed bin Mohammed" = "Ahmed son of Mohammed"). Family/tribal names matter.
- **Formality level varies by country** — Lebanon and Egypt more conversational; Saudi and Gulf more formal

## Arab-specific llms.txt concerns

- **Data residency requirements** in Saudi Arabia, UAE, others — important for hosting decisions
- **PDPL (Saudi Arabia)** — personal data protection law analog to GDPR
- **UAE DPL** — UAE federal personal data law
- **Multi-script SEO** — sites serving Arab markets often need both Arabic and English versions; per-locale llms.txt files
- **Bidirectional text in HTML** — `dir="rtl"` attribute and CSS implications for the indexed pages

## Cross-references

- `_router.md` — language router
- `../../stakeholder/expectations.md` — framing language
