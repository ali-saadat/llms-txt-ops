# Türkçe (tr) — Turkish

Türk iş dünyası iletişim kuralları. Tam şablonlar `../../stakeholder/email-templates-tr.md` dosyasındadır. Kapsamlı vaka çalışması: ExampleMart case (`../../case-study/example-marketplace-case.md`).

## Formality calibration

| Context | Formality |
|---|---|
| Close colleagues, same level | "Merhaba [İsim]," with first names; informal `sen` form |
| Cross-functional, ongoing thread | "Merhaba [İsim] Hanım/Bey," — formal `siz` form |
| Senior colleagues / managers | "Sayın [İsim] Hanım/Bey," — formal `siz` throughout |
| External / vendor | "Sayın [İsim Soyisim] Hanım/Bey," — fully formal |
| Public-facing | Formal third-person or "Sayın Yetkili," for general |

## Honorifics — the most important convention

- **Hanım** (kadın): after first name for women — e.g., `Ayşe Hanım`
- **Bey** (erkek): after first name for men — e.g., `Mehmet Bey`
- **Sayın**: "Esteemed/Honorable" — most formal opener, often combined with full name
- **Hocam**: "My teacher/mentor" — for senior colleagues, academic context (informal for tech work)

Rule: **when in doubt, use `Hanım`/`Bey`**. Dropping them with senior colleagues reads as disrespectful.

## Formal "siz" form vs informal "sen"

Default to `siz` (formal you) in all business communication. Mark every verb:

| Informal `sen` | Formal `siz` | Meaning |
|---|---|---|
| `inceledin mi` | `incelediniz mi` | did you review |
| `gönderdin` | `gönderdiniz` | you sent |
| `paylaştığın` | `paylaştığınız` | (which/that) you shared |
| `bekliyorum` | `bekliyorum` (no diff at "I" form) | I am waiting |
| `gözlemlediğin` | `gözlemlediğiniz` | (that) you observed |

Even casual workplace threads keep `siz` for cross-team and any cross-cultural communication.

## Common business email phrases

| Purpose | Türkçe |
|---|---|
| Açılış teşekkürü | "Öncelikle dikkatli incelemeniz için içtenlikle teşekkür ederim." |
| Genel teşekkür | "Geri bildirimleriniz için teşekkür ederim." |
| Bilgi verme | "Sizinle aşağıdaki bilgileri paylaşmak isterim." |
| Doğrulama sunma | "Yaptığımız kontroller sonucunda..." |
| Dürüst değerlendirme | "Açıkçası belirtmek isterim ki..." |
| Önemli not | "Önemli bir nokta:" |
| Sonuçta | "Sonuç olarak..." |
| Görüşme önerme | "Dilerseniz kısa bir görüşme yapabiliriz" |
| Soru kabul | "Herhangi bir sorunuz olursa lütfen iletişime geçin." |
| Yardım önerme | "Destek olmaktan memnuniyet duyarım." |

## Closing patterns

| Resmiyet seviyesi | Kapanış |
|---|---|
| Standart resmi | `Saygılarımla,` |
| Daha sıcak ek | `Saygılarımla,` + `İyi çalışmalar dilerim` |
| Tam resmi | `En içten saygılarımla,` |
| Yarı-resmi | `Sevgiler,` (yalnızca yakın takım için) |

## Specific patterns for llms.txt advisory in Turkish

### Honest-expectations opening (Turkish-language example)

> "Devam etmeden önce, llms.txt'in ne yapacağı ve yapmayacağı konusunda gerçekçi beklentiler belirlemek istiyorum — çünkü üç bağımsız çalışma (SE Ranking n=300k, OtterlyAI 90 günlük loglar, Search Engine Land 10-site testi) tamamı ölçülebilir AI-atıf artışı bulamadı."

### Three-reasons framing in Turkish

> "Eleştirel incelemeye dayanan üç gerçek sebep: (1) mevcut bozuk dosyayı değiştirmek tartışmasız iyileşme, (2) dosya kendi AI çalışmamız için dahili grounding'e dönüşüyor, (3) ileriye dönük uyumluluk hiçbir maliyet getirmiyor."

### Encoding-issue verification response

> "Yaptığımız tüm kontroller sonucunda kaynak dosyada herhangi bir karakter kodlama problemi tespit edemedik. Dosya, her iki cihazda da doğru şekilde açılıp Türkçe karakterler beklenen biçimde görüntülenmektedir."

### Polite disagreement opening

> "Bu konuyu farklı şekilde değerlendiriyorum çünkü..." veya "Bu noktada görüşüm biraz farklı..."

## Technical terms in Turkish business emails

Bu terimler İngilizce kalır:
- UTF-8, BOM, SHA-256, JSON, XML, MCP, API, HTTP, HTTPS
- llms.txt, robots.txt, sitemap.xml
- Schema.org, JSON-LD
- Jira, GitHub, Slack
- Nginx, Apache, CDN

Türkçeleştirilen terimler:
- "encoding" → "karakter kodlaması"
- "deployment" → "deploy" (genelde İngilizce kalır), "yayına alma"
- "validation" → "doğrulama"
- "monitoring" → "izleme"
- "stakeholder" → "paydaş" (formal) veya "ekip üyesi" (informal)

## Vaka çalışmasından alınan dersler

Anonimleştirilmiş ExampleMart vakasında öğrenilen önemli noktalar (`../../case-study/example-marketplace-case.md`):

1. **SEO uzmanına yapılan yanıt**: detaylı doğrulama + 6 SEO önerisinin tek tek ele alınması + nezaketin korunması
2. **Yöneticinin iki yapısal sorusuna cevap**: tablolu, somut, Jira-ready format
3. **Mühendislik ekibine** ayrı bir paragraf bölümü ile hitap etme — toplu mailde alt-bölüm tekniği
4. **Saygılarımla** + İyi çalışmalar dilerim kombinasyonu — sıcak ama profesyonel kapanış

## Cross-references

- `../../stakeholder/email-templates-tr.md` — tam Türkçe şablonlar
- `../../case-study/example-marketplace-case.md` — kapsamlı Türkiye vakası
- `_router.md` — language router
