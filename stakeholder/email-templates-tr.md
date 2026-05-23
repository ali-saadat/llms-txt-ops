# Turkish Business Email Templates

*Türkçe iş emaili şablonları. ExampleMart vakasından çıkarılan ve Türk iş kültürüne uygun yapılandırılmış şablonlar.*

## Türkçe iş emaili kuralları (kısa özet)

- **Hitap**: `Merhaba [İsim] Hanım/Bey,` (resmi) — `Hanım` kadınlar için, `Bey` erkekler için
- **Resmi "siz" formu**: tüm fiil çekimlerinde (`teşekkür ederim`, `inceledik`, `paylaştığınız`)
- **Kapanış**: `Saygılarımla,` (en yaygın resmi kapanış) — `İyi çalışmalar dilerim` ek nezaket ifadesi
- **Teknik terimler**: UTF-8, SHA-256, Jira gibi terimler İngilizce kalır
- **Birinci çoğul şahıs**: takım eylemleri için (`kontrol ettik`, `doğruladık`) — bireysel ifadeler için (`teşekkür ederim`)

## Şablon 1 — ExampleMart modeli: ilk öneri emaili

**Konu**: `[Proje] llms.txt — Düzenlenmiş Versiyon Ekte`

```
Merhaba [Alıcı],

Öncelikle — beni bu konuya dahil ettiğiniz için içtenlikle teşekkür ederim. 
[Site]'in halihazırda bir llms.txt yayında bulunduruyor olması bile sizi 
dünyadaki sitelerin yaklaşık %90'ının önüne koyuyor; "uzun olması daha mı 
iyi" sorusunu sormak ise tam da doğru sezgi. Çoğu ekip bu noktaya 
ulaşamıyor bile.

Mevcut dosyayı detaylı inceleyip 2026 yılındaki standardın geldiği yere 
göre yeniden yapılandırdım. Hızlı özet aşağıda, tam dosya ekte.

Mevcut uzun dosya — dürüst artı ve eksiler

[Artı-eksi tablosu]

Sezgi doğruydu; uygulama biçimi sadece standardın bugün geldiği noktayı 
biraz öncesinde kalmış.

Düzenlenmiş dosyanın neden daha iyi çalıştığı

[Karşılaştırma tablosu: dosya boyutu, link sayısı, gömülü direktifler, 
kapsam, gündeme getirilen araçlar]

Bunun [Site] için ne anlama geldiği

- Marka düzeyindeki sorular ("[Site] nedir?") doğru şekilde 
  cevaplandırılıyor
- Uzun kuyruk bölge sorguları URL kalıbıyla temiz çözülüyor — tüm 
  bölgeler listelenmeden tam kapsam
- Hukuki / regülasyon sorguları yüksek atıf potansiyelli rehberlere 
  yönlendiriliyor
- llms-full.txt ve MCP ile ileriye dönük uyumlu — agentic commerce 
  geldiğinde önde olacaksınız

Düzenlenmiş dosya ekte ve deploy için hazır. Mevcut olanı değiştirmek bir 
öğleden sonralık değişiklikle anlamlı bir iyileştirme sağlar.

Dilerseniz dosyayı birlikte inceleyebilir ya da [Site] ekibinin 
vurgulamak istediği başka noktalara göre üzerinde iterasyon yapabiliriz. 
Bana güvendiğiniz için tekrar teşekkürler — bu gerçekten keyifliydi.

Saygılarımla,
[İsim]
```

## Şablon 2 — Birden fazla geri bildirim setinden sonra kapsamlı yanıt

**Konu**: `Re: [Proje] llms.txt — vN Revizyonu Tüm Geri Bildirimleri Karşılıyor`

```
Merhaba [Alıcı 1], merhaba [Alıcı 2] Hanım/Bey,

Her ikinize de içtenlikle teşekkür ederim. [Alıcı 1], yapısal sorularınız 
tüm tartışmayı netleştirdi. [Alıcı 2], [konu] incelemenizin derinliği 
dosyayı "spec'e uyumlu"dan "iş için gerçekten faydalı"ya taşıyan tam da 
gereken katkı tipi. [N] noktanızın tamamı vN'de yansıtıldı; birkaç yerde 
uygulama önerinin bir adım ötesine geçti. Detaylar aşağıda.

İki dosya ektedir:

1. project-llms-vN.txt — deploy için hazır dosya ([boyut], [N] adet 
   küratörlü URL, [N] bölüm, UTF-8, BOM içermez, tam doğrulanmış)
2. project-llms-deployment-spec.md — Jira'ya hazır deployment 
   dokümantasyonu; yapısal gerekçe, CI doğrulama scripti, sunucu 
   konfigürasyonu ve dosyanın nasıl oluşturulup yönetildiğinin bölüm 
   bazlı açıklaması içerir

---

## [Alıcı 2]'nin [N] [konu] noktasına yanıtlar

Her birini sırasıyla ele alıyorum. Hepsi vN'de mevcut.

[Her nokta için: ismi, durumu, vN'nin nasıl karşıladığı, varsa öneri 
ötesi uygulama detayı]

---

## [Alıcı 1]'in [N] yapısal sorusuna yanıtlar

### S1 — [Soru 1]

[Tablolu veya madde imli kısa cevap]

### S2 — [Soru 2]

[Kısa cevap]

---

## vN'nin direkt talebin ötesinde sağladıkları

- **Bir dosya, iki hedef kitle.** Aynı dosya hem dış AI ajanlarına 
  hizmet ediyor hem de kendi gelecekteki RAG / chatbot / destek asistanı 
  çalışmalarımız için kaynak-doğruluk haritası işlevi görüyor. Çift iş 
  yapmaya gerek yok.
- **İleriye dönük uyumluluk.** [IETF AIPREF working group] (Ocak 2025'te 
  kurulan) gerçek standardizasyonun yapıldığı yer. Standart kabul 
  edilirse ve büyük LLM'ler taahhüt verirse, biz zaten doğru 
  konumdayız. Ucuz sigorta.
- **Planlanan llms-full.txt eki.** Mintlify'ın deseni — en yüksek atıf 
  potansiyelli ~30 makalenin tam markdown içeriğini birleştirme.

---

## Beklentilerin dürüstçe yönetimi

Başarının ne anlama geldiği konusunda hizalanmamız için bu konuda şeffaf 
olmak istiyorum.

llms.txt'in AI atıfları üzerindeki doğrudan etkisine ilişkin ampirik 
kayıt sade ve etkileyici değil. Üç bağımsız çalışma — SE Ranking 
(n=300,000 domain, Kasım 2025), OtterlyAI (90 günlük sunucu logları, 
Şubat 2026) ve Search Engine Land (10-site test, Ocak 2026) — dosyayı 
yayınlamanın AI atıflarında ölçülebilir bir artış sağlamadığını gösterdi. 
John Mueller, Google'ın bu dosyayı tüketmediğini açıkça söyledi.

Peki neden yine de yayınlıyoruz? Eleştirel incelemeye dayanan üç gerçek 
sebep:

1. Mevcut durum (şişirilmiş dosya) en kötü seçenek. vN ile değiştirmek, 
   sağlayıcıların adoption durumundan bağımsız olarak açık ve hemen 
   gerçekleşen bir iyileştirme — "bozuk"tan "doğru"ya geçiyoruz.
2. Dahili grounding ek değeri. Talimatlar bloğu kendi AI çalışmamız için 
   mükemmel grounding materyali — hiçbir dış AI dosyayı okumasa bile 
   değer üretmeye devam ediyor.
3. İleriye dönük uyumluluk hiçbir maliyeti yok. AIPREF kabul edilir ve 
   sağlayıcılar taahhüt verirse, biz zaten doğru konumdayız.

AI atıflarını gerçekten hareket ettiren kaldıraçlar bugün için içerik 
kalitesi, dış atıflar (Wikipedia, Reddit, YouTube), schema.org ve temiz 
semantik HTML — tam olarak SEO ekibinin halihazırda yatırım yaptığı 
alanlar. llms.txt çalışması bu daha geniş stratejiyi destekliyor; 
yerine geçmiyor.

vN'yi doğru beklentilerle yayına almayı, ileride aşırı söz vermenin 
sonucu olarak hayal kırıklığı yaşatmaktan yeğliyorum.

---

## Sonraki adımlar

- **Jira ticket** — deployment spec, mühendislik ekibinin açacağı ticket'a 
  doğrudan kopyalanabilecek formatta hazırlandı. Kabul kriterleri, 
  doğrulama scripti, sunucu konfigürasyonu ve deploy/rollback playbook 
  içerir.
- **CI doğrulama** — doğrulama scripti'ni build pipeline'a entegre 
  edelim ki gelecekteki refresh'ler bozuk gönderemesin.
- **Sunucu headerları** — spec'te Nginx konfig bloğu.
- **robots.txt tutarlılık kontrolü** — vN'deki her URL, önemsediğimiz AI 
  user-agent'ları için Allow: olmalı.
- **Üç aylık refresh** — dokümante edilmiş cadence; sonraki review 
  [tarih].
- **İzleme** — deploy sonrası /llms.txt'e gelen istekleri user-agent 
  bazlı loglayalım.

İsterseniz 30 dakikalık bir görüşme ile vN'yi bölüm bölüm gözden 
geçirelim.

Zamanınız ve titizliğiniz için her ikinize de tekrar teşekkür ederim.

Saygılarımla,
[İsim]
```

## Şablon 3 — Karakter kodlama / kalite konusu yanıtı (kaynak gerçekten temiz olduğunda)

**Konu**: `Re: [Proje] llms.txt — Karakter Kodlama Doğrulaması`

```
Merhaba [Alıcı] Hanım/Bey,

Dosya üzerindeki dikkatli incelemeniz ve paylaştığınız spesifik örnekler 
için içtenlikle teşekkür ederim. Bunlar sayesinde gerçek bir doğrulama 
çalışması yürütebildik.

Endişenizi ciddiyetle ele aldık ve kaynak dosya üzerinde [N] bağımsız 
kontrol gerçekleştirdik:

[Kontrol tablosu:]
- Karakter kodlaması: UTF-8 — file -bi ile teyit edildi
- BOM kontrolü: BOM yok
- Türkçe karakter envanteri: [ilgili karakterlerin sayıları] hepsi doğru 
  UTF-8 kodlaması ile bulunuyor
- Paylaştığınız bozuk örüntülerin kaynak dosyada aranması: sıfır 
  bulundu
- Cihaz #1: [araç] doğru görüntüledi
- Cihaz #2: [araç] doğru görüntüledi
- SHA-256 hash: [hash] — sonraki aşamalarda byte düzeyinde doğrulama 
  için referans

Sonuç: kaynak dosya temiz. Gördüğünüz şey muhtemelen görüntüleme katmanı 
veya transit katmanı kaynaklı — en olası nedenler: [yazı tipi fallback / 
e-posta gateway normalleştirmesi / kopyala-yapıştır ara işlem].

Bu endişenin yeniden gündeme gelmemesi için üç savunma katmanı 
ekliyoruz:

1. CI, her deploy öncesi UTF-8 geçerliliğini, BOM yokluğunu ve karakter 
   envanterini kontrol ediyor. Aksi halde build başarısız oluyor.
2. Deploy sonrası, yayınlanan dosyanın SHA-256 hash'i kaynak hash ile 
   karşılaştırılacak. CDN / proxy dönüşümlerini yakalar.
3. İleriki transferler e-posta eki yerine paylaşımlı sürücü veya Git PR 
   üzerinden yapılacak. Ara-araç riskini ortadan kaldırır.

İsterseniz birlikte doğrulayalım: kısa bir ekran paylaşımı ile dosyayı 
sizin cihazınızda [VS Code / önerdiğim viewer] üzerinde yan yana 
açabiliriz. Sadece sizin için uygun bir zaman dilimi bildirmeniz 
yeterli.

Bu konuyu yakaladığınız için tekrar teşekkür ederim — kaynak temiz çıksa 
bile sağlam bir diagnostic protokol yerinde olması başlı başına bir 
kazanım.

Saygılarımla,
[İsim]
```

## Şablon 4 — Birden fazla muhataba aynı emailde hitap etme deseni

Türk iş kültüründe yaygın: birincil muhataba detaylı yanıt verip, aynı 
emailde başka bir muhataba ayrı bir bölümle hitap etmek.

```
Merhaba [Birincil muhatap] Hanım/Bey,

[Detaylı içerik...]

---

[İkincil muhataplar — ad olarak]

[Konu hakkında ne yapmaları gerektiği — istek formunda]:
"Bu kapsamda [X] görevinin Jira üzerinde açılması için sürecin 
başlatılmasını rica ediyorum."

[Açıklama ve referanslar.]

[Herhangi bir aşamada destek için iletişim açıklaması.]

---

Tekrar [birincil muhataba teşekkür]. İyi çalışmalar dilerim.

Saygılarımla,
[İsim]
```

Bu desen anonimleştirilmiş vaka çalışmasında kullanıldı — SEO uzmanına 
kodlama yanıtı + mühendislik ekibine Jira açma talebi aynı emailde.

## Önemli üslup notları

### Sayın vs Merhaba

- **Sayın** — daha resmi, ilk temas için, dış paydaşlara yazarken
- **Merhaba** — devam eden ekip içi yazışmalar için, sıcak ve profesyonel

ExampleMart gibi aktif tartışma threadlerinde `Merhaba [İsim] Hanım/Bey` 
uygun.

### Hanım / Bey kullanımı

- Kadın muhatap → `[İsim] Hanım`
- Erkek muhatap → `[İsim] Bey`
- İsim bilinmiyorsa → `Sayın Yetkili`

Bilinen ekip içinde sadece isim kullanmak kabul edilebilir ama 
özellikle SEO uzmanı / kıdemli personel için `Hanım/Bey` koruyucu olur.

### Resmi "siz" formu

Tüm zamanlarda korunmalı:
- `incelemeniz` (değil `incelemen`)
- `paylaştığınız` (değil `paylaştığın`)
- `gözlemlediğiniz` (değil `gözlemlediğin`)
- `çekinmeden iletişime geçin` (değil `çekinmeden iletişime geç`)

### Kapanış varyasyonları

| Kapanış | Bağlam |
|---|---|
| `Saygılarımla,` | Standart resmi kapanış — her durumda uygun |
| `İyi çalışmalar dilerim` | Ek nezaket — yardımcı not olarak ekleyin |
| `Saygılarımla, iyi çalışmalar` | İkisinin birleşimi — orta düzey resmiyet |
| `Tekrar teşekkür ederim` | Bir önceki paragrafa bağlantılı — kapanış öncesi |

## Cross-references

- English versions → `email-templates-en.md`
- Framing language (English) → `expectations.md`
- Real example used in case → `../case-study/example-marketplace-case.md`
