# 日本語 (ja) — Japanese

Japanese business communication conventions. The most complex language for formality calibration due to the **keigo** (敬語) system. Getting tone wrong is more consequential than in Western languages.

## Formality is non-negotiable

Japanese has multiple speech levels — informal (casual), polite (`desu/masu`), formal (`-narimasu` / `gozaimasu`), and humble (`itadaku`, `mosu-ageru`). **Business communication uses polite-to-formal exclusively.**

Western "casual" doesn't translate. Even between close colleagues, written business email maintains polite forms.

## Honorifics

- **さん (-san)** — universal honorific, gender-neutral. Default for colleagues, clients, anyone you've introduced yourself to. Like "Mr./Ms." but more universal.
- **様 (-sama)** — very formal, for customers and high-status external parties. Used in formal letters and on envelopes.
- **先生 (-sensei)** — for teachers, doctors, lawyers, accountants — anyone with professional expertise.
- **氏 (-shi)** — formal in writing for third-person reference.
- **役職 (yakushoku)** — title-based: 部長 (Buchō, department head), 社長 (Shachō, president), 取締役 (Torishimariyaku, director) — used WITHOUT last name in direct address.

Critical: **Use the recipient's title + さん (-san) or -様 (-sama)**. Last name + さん is the safe default. Switching to first name is uncommon even after long working relationships.

## Common business email structure

Japanese business email has a strict template:

```
[Recipient title + name + 様/さん]

お世話になっております。
[Your name/company]の[your name]です。

[Body — concise, often with bullet-style points]

何卒よろしくお願いいたします。

[Your name]
[Company]
```

## Common business email phrases

| Purpose | 日本語 |
|---|---|
| Standard opening | お世話になっております (osewa ni natte orimasu) — "I'm always grateful for your support" |
| Self-introduction | [会社名]の[名前]と申します ([company name] no [name] to mōshimasu) — "I'm [name] from [company]" |
| Opening thanks | ご丁寧にご確認いただきありがとうございます (gotēnei ni gokakunin itadaki arigatō gozaimasu) — "Thank you for your careful review" |
| Apologetic acknowledgment | お手数をおかけしますが (otesū o okake shimasu ga) — "Sorry to trouble you, but..." |
| Presenting findings | 確認結果をご報告いたします (kakunin kekka o gohōkoku itashimasu) — "I'd like to report the verification results" |
| Polite request | お願いいたします (onegai itashimasu) — "Please" / standard request |
| Acknowledging mistake | 申し訳ございません (mōshiwake gozaimasen) — "I apologize" |
| Closing courtesy | 何卒よろしくお願いいたします (nanitozo yoroshiku onegai itashimasu) — Universal closing |

## Closing patterns

Japanese business email closes with set phrases, NOT signature-style:

| Context | Closing phrase |
|---|---|
| Standard | 何卒よろしくお願いいたします (nanitozo yoroshiku onegai itashimasu) |
| Formal | 引き続きどうぞよろしくお願い申し上げます (hikitsuzuki dōzo yoroshiku onegai mōshiagemasu) |
| Following a request | お忙しいところ恐れ入りますが、ご対応のほどよろしくお願いいたします |
| First contact | 今後とも、よろしくお願いいたします |

After the phrase, sign with name, company, position, contact.

## Honest-expectations opening (translated, formal)

> 続けて作業を進める前に、llms.txtに関する現実的な期待値を共有させていただきたく存じます。三つの独立した調査(SE Ranking n=30万ドメイン、OtterlyAI 90日間サーバーログ、Search Engine Land 10サイトテスト)はいずれも、AI引用への測定可能な向上を示しませんでした。

## Three-reasons framing (translated)

> 検討に耐える理由は三つです。(1) 既存の壊れたファイルの置き換えは明らかに改善である、(2) このファイルは社内の独自のAI業務における基盤資料としても機能する、(3) 将来的な互換性確保にはコストがかからない。守備的な根拠であり、攻撃的なものではありません。

## Date and number formats

- Date: `2026年5月15日` (year/month/day) — formal
- Date: `2026/05/15` — common in business systems
- Number: `1,234.56` (US format common; some industries use 万-based: `12.3456万` for 123,456)
- Currency: `¥1,234` or `1,234円` — yen
- Time: 24-hour clock common (`14時30分` or `14:30`)

## Cultural notes

- **Indirect communication is preferred** — direct refusal is rare; "難しい" (difficult) often means "no"
- **Building consensus (根回し / nemawashi)** — important decisions usually pre-discussed informally before formal email
- **Hierarchical sensitivity** — copy senior colleagues even when communication is between juniors
- **Time-sensitivity** — replying quickly (same-day if possible) is appreciated
- **Group-orientation** — say "we" / "our team" more than "I"
- **Apologetic framing** — explicitly apologize for small inconveniences ("Sorry for the slight delay" etc.) even when not really late
- **Avoid emoji and exclamation marks** — read as unprofessional in most contexts

## Japan-specific llms.txt concerns

- **Personal Information Protection Law (APPI)** — Japan's GDPR equivalent
- **Industry-specific regulations** — finance has stringent rules (JFSA), pharma has separate regime
- **Half-width vs full-width characters** — encoding gotcha; ensure UTF-8 handles full-width Japanese correctly (most modern stacks do, but worth verifying)
- **Vertical writing** — irrelevant for llms.txt (which is markdown horizontal), but a consideration for printed deliverables

## Cross-references

- `_router.md` — language router
- `../../stakeholder/expectations.md` — framing language
