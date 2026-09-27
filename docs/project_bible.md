# Proje Kitabı (Project Bible)

## Amaç
3–8 yaş arası çocuklar için, Türk çocuk edebiyatının sıcaklığından, mizahından, doğa sevgisinden ve arkadaşlık temalarından ilham alan; ancak tamamen özgün karakterler, hikâyeler ve dünyalar üreten bir YouTube animasyon kanalı.

## Hedef Kitle
Ana hedef: 3–8 yaş. Not: bazı bölümler farklı yaş aralıklarını (ör. 8–10) hedefleyebilir; her bölümün target_age alanı ayrı belirlenir.

## İçerik Felsefesi
- Tek problem, tek çözüm, pozitif son yapısı.
- Mizah, merak, keşif, arkadaşlık, aile ilişkileri, doğa sevgisi ana temalardır.
- Öğretici ama "vaaz verir gibi" olmayan bir ton.

## Görsel Stil
- Renk paleti: toprak tonları + pastel yeşil/mavi, aşırı parlak/neon renk yok.
- Işık: altın saat (gün doğumu/batımı) hissi baskın.
- Çizim tarzı: 2.5D, düz renkli, "resimli kitap" hissi; Pixar kadar foto-gerçekçi DEĞİL. Bu bilinçli bir tercih: hem üretim maliyetini düşürür hem de YouTube'un "gerçekçi sentetik içerik" ifşa politikasına takılma riskini azaltır.
- Hafif kağıt/suluboya doku overlay; jenerik (markasız) Anadolu motif detayları.

## Anlatım Kuralları
- Her bölüm 3–5 dakika.
- Başlık / Karakterler / Olay / Mesaj / Komik sahne şablonu her bölümde zorunlu.
- Sabit dünya (Fındıkdere Mahallesi) — bkz. docs/world_bible.md — tekrar kullanılabilir varlık (asset) tutarlılığı için sabit tutulur.

## Karakter Kuralları
- Sabit bir "ana karakter evreni" var (10 karakter, bkz. config/characters.yaml).
- Her bölüm bu evrenden 1-3 karakter kullanır; hepsi aynı anda her bölümde olmak zorunda değil.
- Yaş aralığı ve hangi karakter(ler)in öne çıkacağı bölümden bölüme değişebilir.

## Özgünlük ve Telif Kuralları (ZORUNLU — atlanamaz)
- Türk çocuk yazarlarının (dahili referans listesi: docs/style_influences_internal.md) SADECE genel üslup/tema özelliklerinden ilham alınır: mizah, doğa sevgisi, arkadaşlık, merak, aile ilişkileri.
- HİÇBİR mevcut kitabın olay örgüsü, karakteri veya özel/ayırt edici unsuru kopyalanmaz veya uyarlanmaz.
- Yazar isimleri veya "şu yazardan ilham alındı" ifadeleri hiçbir zaman başlıkta, açıklamada, etikette veya herhangi bir halka açık YouTube alanında kullanılmaz — bu içerik çıkarımı sadece iç tasarım referansıdır.
- Halk masalı/folklor (Nasreddin Hoca, Keloğlan, Dede Korkut vb.) kullanılacaksa: SADECE genel motif/olay iskeleti referans alınır; hiçbir spesifik modern kitap baskısının metni, diyaloğu veya illüstrasyonu kopyalanmaz. Senaryo, diyalog ve görsel promptlar sıfırdan yazılır.
- Her bölüm için üç soruluk "kaynak kontrolü" doldurulmadan bölüm onaya gönderilmez: (1) esin kaynağı tamamen özgün mü yoksa folklor mu, (2) sadece iskelet/tema mı alındı yoksa spesifik bir esere ait sahne/diyalog/görsel mi kullanıldı, (3) şüpheli ise bölüm rafa kaldırılır.

## Üretim Kuralları
- Sıfır ek maliyet hedefi: mevcut Google AI abonelikleri + ücretsiz/açık kaynak araçlar (Piper TTS, FFmpeg, DaVinci Resolve free).
- Video üretimi (Veo) tek gerçek maliyet kalemi; her kullanım öncesi maliyet raporlanır ve onay istenir.

## Kalite Standartları
- Karakter tutarlılığı: referans görsel + video-uzatma yöntemiyle sağlanır (bkz. docs/pipeline.md).
- Her bölüm insan onayından geçmeden yayınlanmaz.

## Otomasyon Felsefesi
- Level 2/3 (script-driven / pipeline automation) hedeflenir; Level 5 (tam otonom) şimdilik hedeflenmiyor.

## Maliyet Sınırları
- Aylık hedef: mümkün olduğunca 0 €; onaylanmış bütçe olmadan hiçbir ücretli API/servis devreye alınmaz.

## İnsan Onay Noktaları
- Checkpoint A: kanal konsepti (bu belge) — ONAYLANDI (2026-09-27)
- Checkpoint B: her bölümün hikâyesi
- Checkpoint C: görsel stil (bu belge) — ONAYLANDI (2026-09-27)
- Checkpoint D: üretilen varlıklar (görseller/videolar)
- Checkpoint E: final video
- Checkpoint F: YouTube yükleme
