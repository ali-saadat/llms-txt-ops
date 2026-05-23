# 中文 (zh) — Mandarin Chinese

Mandarin Chinese business communication conventions. Notable variations between Mainland China (simplified characters, 简体字), Taiwan (traditional characters, 繁體字), and Hong Kong (traditional + Cantonese influence). Most business communication uses simplified characters for Mainland, traditional for Taiwan and Hong Kong.

## Variant matters

Match the recipient's variant:
- **Mainland China** (大陆 / dàlù): Simplified characters, "你" (nǐ), business culture more Mainland-mainstream
- **Taiwan** (台湾 / táiwān): Traditional characters, slightly different vocabulary
- **Hong Kong** (香港 / xiānggǎng): Traditional characters, often English-heavy in business
- **Singapore** (新加坡 / xīnjiāpō): Simplified characters typically, often code-switches with English

When unsure, ask. Don't mix variants in the same document.

## Formality calibration

| Context | Formality |
|---|---|
| Close colleagues | Casual: "你好 [Name]" — informal `你` |
| Cross-functional thread | Professional: "您好 [Name]" — formal `您` (Mainland) / `您好` (Taiwan) |
| Senior / management | "尊敬的 [Name + Title]" or "[Title + Name]您好" |
| External / vendor | Fully formal opening + closing |
| Hong Kong | Often code-switches with English; English greetings common |

## Forms of address

- **您 (nín)** — formal "you", used for elders, superiors, customers
- **你 (nǐ)** — informal "you", peers, colleagues
- **先生 (xiānsheng)** — Mr.
- **女士 (nǚshì)** — Ms./Mrs.
- **小姐 (xiǎojiě)** — Miss (Mainland) — but in some Mainland contexts, has become inappropriate; "女士" is safer
- **博士 (bóshì)** — Dr.
- **教授 (jiàoshòu)** — Professor

Title precedes name in formal address: `张总` (Zhāng zǒng, "President Zhang"), `李博士` (Lǐ bóshì, "Dr. Li").

## Common business email phrases

| Purpose | Simplified (Mainland) | Traditional (Taiwan/HK) |
|---|---|---|
| Opening greeting | 您好 | 您好 |
| Self-introduction | 我是[公司]的[名字] | 我是[公司]的[名字] |
| Opening thanks | 感谢您仔细的审阅和反馈 | 感謝您仔細的審閱和反饋 |
| Acknowledging concern | 我想直接回应这个问题 | 我想直接回應這個問題 |
| Presenting findings | 以下是我们的验证结果 | 以下是我們的驗證結果 |
| Honest framing | 关于成功的标准我想保持透明 | 關於成功的標準我想保持透明 |
| Closing offer | 如有任何问题请随时联系 | 如有任何問題請隨時聯繫 |

## Closing patterns

| Formality | Mainland | Taiwan/HK |
|---|---|---|
| Standard formal | 此致 + 敬礼 (two lines) | 此致 + 敬禮 |
| Common formal | 谢谢! | 謝謝! |
| Tech business standard | 祝好 | 祝好 |
| Most formal | 敬上 (after name) | 敬上 |
| English-influenced | "Best regards," then Chinese name | "Best regards," then Chinese name |

## Honest-expectations opening (Mainland simplified)

> 在我们继续之前,我想就llms.txt的实际作用与无法做到的事情设定现实的预期 — 三项独立研究(SE Ranking n=30万域名、OtterlyAI 90天服务器日志、Search Engine Land 10站点测试)均未发现可量化的AI引用提升。

## Three-reasons framing (Mainland simplified)

> 经过仔细审视后,有三个站得住脚的理由:(1) 替换现有损坏的文件本身就是明确的改进,(2) 文件可同时作为我们自身AI工作的内部知识基础,(3) 前向兼容性的成本为零。论据是防御性的,而非进取性的。

## Date and number formats

- Date Mainland: `2026年5月15日` or `2026-05-15`
- Date Taiwan/HK: `2026年5月15日` or `15/5/2026`
- Number: `1,234.56` (US-style, both variants)
- Currency Mainland: `¥1,234` or `1,234元`
- Currency Taiwan: `NT$1,234`
- Currency HK: `HK$1,234`

## Cultural notes

- **Hierarchy is critical** — copy senior colleagues even on minor communications
- **Indirect language is preferred** for difficult topics; direct "no" is uncommon
- **Face (面子 / miànzi)** — avoid causing embarrassment to anyone in the conversation
- **Numerology** — 4 (sounds like "death") is unlucky; 8 is lucky. Less relevant in tech context but be aware.
- **Names**: Chinese names are usually written family-name-first (`张伟` = "Zhang Wei"). Don't reverse to Western order unless the person uses Western order in their own signature.
- **Holiday awareness** — Lunar New Year (春节), Mid-Autumn Festival (中秋节) etc. affect availability
- **WeChat is dominant** — many business communications happen on WeChat rather than email, especially in Mainland. Email may be secondary channel.
- **English mixing is common in tech** — phrases like "OK", "Reasonable", "Sure" often appear in Chinese business email from tech-industry Mandarin speakers

## Chinese-specific llms.txt concerns

- **Personal Information Protection Law (PIPL)** — China's GDPR equivalent (since Nov 2021)
- **Cybersecurity Law (网安法)** and **Data Security Law** — applicable to sites operating in China
- **Cross-border data transfer restrictions** — significantly more restrictive than GDPR
- **Mainland encoding**: GB18030 historical issue but modern stacks use UTF-8; ensure full UTF-8 handling for full character set
- **Great Firewall implications**: AI bot user-agents accessing sites hosted in China have unique constraints

## Cross-references

- `_router.md` — language router
- `../../stakeholder/expectations.md` — framing language
