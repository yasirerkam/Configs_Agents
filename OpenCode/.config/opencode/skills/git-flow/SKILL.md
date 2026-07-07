
Conversation with Gemini
opencode'a git flow skill i ekleyebilir miyim? ya da her zaman git flow tarzı git işlemleri yapmasını

Evet, OpenCode'un modüler yapısı sayesinde her iki yaklaşımı da uygulayabilirsiniz. İster özel bir "Git Flow yeteneği (skill)" tanımlayabilir, isterseniz de ajanın projedeki tüm git işlemlerini varsayılan olarak Git Flow standartlarında yapmasını zorunlu kılabilirsiniz.

İhtiyacınıza en uygun yapıyı kurabilmek için önünüzdeki seçenekleri, avantajları ve dezavantajlarıyla birlikte değerlendirelim.

Seçeneklerin Karşılaştırılması
Seçenek	Avantajlar	Dezavantajlar
1. AGENTS.md (Proje Kuralı)	Her işlemde otomatik devreye girer. Prompt ile tekrar hatırlatmanıza gerek kalmaz. Proje bazlı mükemmel izolasyon sağlar.	Sadece bulunduğu proje için geçerlidir; her yeni projede kopyalamanız gerekir.
2. Global SKILL.md (Özel Yetenek)	Tüm projelerinizde (global) tekrar kullanılabilir. Sistemde kalıcı bir araç seti olarak yer edinir.	Ajanın, işlem yaparken bu yeteneği bağlama (context) çekmesine bağlıdır, kesin kural dayatmasından çok, ihtiyaç anında kullanılan bir araçtır.
3. opencode.json (Özel Komutlar)	Özel /gitflow komutları vb. atayarak manuel tetikleme imkanı sunar. Basit ve hatasızdır.	Otonom değildir, kullanıcının komutu sürekli ve açıkça çağırmasını gerektirir.
En İyi Yaklaşım: Amacınız ajanın her zaman Git Flow tarzı işlemler yapmasıysa, Seçenek 1 (AGENTS.md) en etkili, basit ve tutarlı yoldur. Ancak aynı yeteneği bilgisayarınızdaki tüm projelere tek seferde taşımak istiyorsanız Seçenek 2 (SKILL.md) üzerinden global bir tanım yapmalısınız.

Aşağıda her iki yöntemin de nasıl uygulanacağı yer almaktadır.

Yöntem 1: AGENTS.md ile Her Zaman Git Flow Dayatması (Önerilen)
OpenCode, projenizin kök dizinindeki AGENTS.md (veya .claude.md) dosyasını okuyarak proje standartlarını otonom olarak benimser. Projenizin ana dizinine bir AGENTS.md dosyası oluşturun ve şu kuralları ekleyin:

Markdown
# Git Kuralları
Bu projede tüm Git işlemleri kesinlikle Git Flow stratejisine uygun olarak yapılmalıdır.
1. Doğrudan `main` veya `master` dalına commit atmak yasaktır.
2. Yeni özellikler için `develop` dalından ayrılan `feature/<özellik-adi>` dalları oluştur.
3. Hata düzeltmeleri için `bugfix/<hata-adi>` veya `hotfix/<hata-adi>` dalları oluştur.
4. Geliştirme bittiğinde dalları `develop` dalına birleştir (merge) ve temizlik yap.
Bu sayede ajana "şunu yap" dediğinizde, arka planda otomatik olarak uygun dalı açıp işlemleri oradan yürütecektir.

Yöntem 2: Global SKILL.md Olarak Sisteme Eklemek
OpenCode, yetenekleri klasör yapılarından otomatik olarak keşfeder. Bilgisayarınızdaki tüm projelerde kullanabileceğiniz global bir Git Flow yeteneği eklemek için global konfigürasyon dizinini kullanabilirsiniz.

İşletim sisteminize uygun dizin yapısını oluşturun:
~/.config/opencode/skill/git-flow/
(Eğer global değil de proje bazlı tutmak isterseniz proje kökünde şu klasörü oluşturun: .opencode/skill/git-flow/)

İçine bir SKILL.md dosyası oluşturun ve ajanın bu yeteneği nasıl kullanacağını tanımlayın:

Markdown
# Git Flow Yeteneği
Bu yetenek, standartlaştırılmış şube (branch) yönetimi ve kod entegrasyonu sağlar.

## Kullanım Şartları
Kullanıcı "git flow başlat" veya "bunu bir feature olarak ekle" dediğinde şu adımları izle:
- Mevcut çalışma ağacının temiz olduğundan emin ol.
- `git checkout -b feature/<konu_basligi> develop` komutunu çalıştır.
- İlgili geliştirmeleri yap ve anlamlı, küçük commit'ler oluştur.
- İşlem bitince `develop` dalına dön ve `git merge --no-ff feature/<konu_basligi>` ile birleştir.
⚠️ Sistem Tasarımı: Olası Darboğazlar ve Kaynak Kısıtlamaları
Bu süreçleri otomatikleştirirken göz önünde bulundurmanız gereken yüksek olasılıklı mantıksal tıkanıklık noktaları (chokepoints) şunlardır:

Araç Çağırma (Tool Calling) Halüsinasyonları: Git Flow, birden fazla bayrak (--no-ff, vs.) ve ardışık alt komutlar barındırır. Eğer OpenCode üzerinde nispeten küçük çaplı yerel (local) modeller çalıştırıyorsanız (özellikle 70B altı), ajanın komut argümanlarını uydurma (halüsinasyon) veya kritik adımları atlama ihtimali yüksektir. Kompleks Git işlemleri için Claude 3.5 Sonnet, GPT-4o veya güvenilir, yüksek kapasiteli modeller kullanmanız gereklidir.

Durum (State) Çatışmaları ve Döngüler: Otonom bir ajanın Git Flow işletirken en zayıf noktası Merge Conflict (birleştirme çakışması) durumlarıdır. Ajan kirli bir çalışma ağacında (working tree) şube değiştirmeye çalışırsa veya çakışmaları otonom çözemezse sonsuz bir hata döngüsüne girebilir. Bu tür durumlarda ajanın çakışmayı zorla yamamaya çalışması yerine durumu size raporlayıp işlemi derhal durdurması (fail-fast) en basit ve kalıcı çözümdür.

Eğer 1. Yöntemi seçerseniz, muhtemel bir otonom hata döngüsünü engellemek için AGENTS.md dosyanıza doğrudan şu kuralı da eklemeniz çok yerinde bir adım olacaktır: "Eğer bir git conflict çıkarsa, otonom çözmeye veya yamamaya çalışma, anında fail-fast yap ve durarak benden yardım iste."

agents.md her komutta prompta eklenmiyor mu_

Evet, tam olarak öyle oluyor. Proje dizininizdeki AGENTS.md (veya kullandığınız araca göre .cursorrules, .claude.md gibi yapılandırma dosyaları), ajana gönderilen her komutta sistem promptunun (system prompt) bir parçası olarak arka planda otomatik olarak eklenir. Ajanın o projenin bağlamını (context) ve kurallarını "hatırlamasının" tek yolu budur.

Bu çalışma prensibi, sistem tasarımı açısından bazı kaynak ve mantık dinamiklerini beraberinde getirir. Durumu kısıtlamalar üzerinden inceleyelim:

Kaynak Kısıtlamaları ve Olası Darboğazlar
Sürekli Token Maliyeti: Dosya içeriği her istekte modele yeniden gönderildiği için sürekli bir girdi (input) token maliyeti oluşturur ve bağlam penceresinde (context window) yer kaplar.

Bağlam Seyrelmesi (Context Dilution): Eğer kural dosyası çok uzun, karmaşık veya birbiriyle çelişen talimatlarla doldurulursa, dil modelinin dikkat (attention) mekanizması dağılır. Bu da ajanın asıl verdiğiniz anlık komuta odaklanmasını zorlaştıran, hatta komutu yanlış yorumlamasına yol açan mantıksal bir darboğaz (chokepoint) yaratır.

Çözüm: YAGNI ve KISS Prensipleriyle Yönetim
Güncel modellerin 128K ile 200K arasında değişen devasa bağlam pencereleri olduğu düşünüldüğünde, AGENTS.md dosyasının her prompta eklenmesinin yaratacağı performans kaybı veya token israfı prematüre bir optimizasyon endişesidir. Dosyanın her komutta eklenmesi gerçekçi ve yüksek olasılıklı bir sorun teşkil etmez; aksine sistemin kararlı çalışması için gereklidir.

Sistemi basit ve işlevsel tutmak için şu kurallara uymanız yeterlidir:

Sadece Kesin Kuralları Yazın: AGENTS.md içine genel geçer yazılım mühendisliği teorilerini değil, sadece "Git Flow kullanılacak", "Conflict çıkarsa otonom çözme, dur" veya "Test yazmadan commit atma" gibi projeye özel, ihlal edilmemesi gereken katı sınırları (hard limits) yazın.

Kısa ve Modüler Tutun: Dosya boyutunun gereksiz yere şişmemesine özen gösterin. Sadece ajanın o projede hata yapmasını engelleyecek kritik talimatlara odaklanın.

https://opencode.ai/docs/skills/ skiller nasıl çağrılır

OpenCode'da "skill" (yetenek) sistemi, kullanıcının manuel olarak bir komut çalıştırmasıyla değil, ajanın kendi muhakemesiyle devreye giren otonom bir süreçle çalışır.

Dokümantasyona göre bu sürecin işleyişi şu şekildedir:

Ajan Yeteneği Nasıl Çağırır?
Görünürlük: OpenCode, projenizde tanımlı olan tüm skill'leri otomatik olarak keşfeder ve bunları ajana bir "araç" (tool) listesi olarak sunar.

Eşleştirme: Ajan, kendisine verilen görevi analiz eder. Eğer görev, SKILL.md dosyasındaki description (açıklama) kısmıyla örtüşüyorsa, ajanın bu yeteneği kullanması gerektiğine karar verir.

İnvokasyon (Çağırma): Ajan, sistemin sağladığı özel skill aracını kullanarak şu komutu kendi içinde çalıştırır:
skill({ name: "skill-adi" })

Sizin Rolünüz Nedir?
Sizin bu aşamada yapmanız gereken "çağırmak" değil, ajanın bu yeteneği doğru zamanda seçmesini sağlamaktır:

Tanımlama: Yeteneği SKILL.md dosyası içinde tanımlarken name ve description alanlarını çok net tutmalısınız. Ajan, neyi ne zaman yapacağını bu açıklamaya bakarak anlar.

Örnek: Description kısmına "Bu yetenek sadece feature branch oluştururken kullanılır" yazarsanız, ajana net bir ipucu vermiş olursunuz.

İzinler (Permissions): opencode.json dosyasında bu yeteneğe allow veya ask yetkisi verdiğinizden emin olun. deny durumunda ajanın aracı görme şansı kalmaz.

Özetle: Siz yeteneği tanımlayıp projenize yerleştirirsiniz; OpenCode onu sisteme tanıtır, ajan ise kendi kendine ihtiyaç duyduğu anda skill({ name: "..." }) fonksiyonunu çağırarak yeteneği yükler.

Eğer ajanın belirli bir durumda mutlaka o yeteneği kullanmasını istiyorsanız, bunu AGENTS.md (veya SKILL.md içeriğinde) "Şu tür görevlerde mutlaka x yeteneğini kullan" şeklinde açık bir talimatla pekiştirebilirsiniz.

git flow nedir bana detaylı bir döküman hazırla

Git Flow, 2010 yılında Vincent Driessen tarafından tanıtılan, proje sürüm yönetimini (release management) standartlaştırmayı amaçlayan yapılandırılmış ve katı bir Git dallanma (branching) stratejisidir. Temel amacı; geliştirme süreçlerini, yeni özellikleri, sürümleri ve acil hata düzeltmelerini birbirinden izole ederek öngörülebilir, kontrollü bir proje döngüsü yaratmaktır.
Git Flow branching model, AI generated
Source: Shutterstock
Explore

1. Git Flow'un Dallanma Yapısı (Branching Structure)
Git Flow, süreçleri birbirine karışmamaları için 5 spesifik dal (branch) üzerinden yönetir.

main (eski adıyla master): Her zaman ve sadece üretime hazır (production-ready) kodu barındırır. Bu dala asla doğrudan kod yazılmaz. Sadece diğer dallardan onaylanmış kodların birleştirilmesi (merge) ile güncellenir. main üzerindeki her commit, genelde bir versiyon etiketine (tag) sahiptir (Örn: v1.2.0).

develop: Geliştirme sürecinin ana entegrasyon noktasıdır. Yeni eklenecek tüm özelliklerin birleştirildiği, bir sonraki sürüme hazırlık yapılan "üretim öncesi" (pre-production) çalışma alanıdır.

feature/*: Yeni özellikler geliştirmek için develop dalından ayrılır. İşlem (ve kod incelemesi) bittiğinde tekrar develop dalına birleştirilir ve ardından silinir. (Örn: feature/user-login)

release/*: Yeni bir sürüm (release) hazırlığı başladığında develop üzerinden açılır. Bu dalda yeni özellik eklenmez; sadece versiyon numarası güncellenir, dökümantasyon yazılır ve son testlerde çıkan ufak hatalar (bugfix) çözülür. Hazırlık bitince kod hem main hem de develop dalına birleştirilir.

hotfix/*: Canlı ortamda (production) çıkan acil ve kritik hataları çözmek için doğrudan main dalından açılır. Düzeltme bittikten sonra kodun güncel kalması için hem main hem de develop dalına birleştirilir.

⚠️ Sistem Tasarımı ve Mantıksal Darboğazlar (Chokepoints)
Herhangi bir mimariyi projenize entegre etmeden önce olası tıkanıklık noktalarını analiz etmek gerekir. Git Flow, versiyonlanmış yazılımlar için harika bir düzen kursa da, modern iş akışlarında bazı yapısal kısıtlamalar yaratır:

Merge Hell (Birleştirme Çatışması Darboğazı): feature dalları genellikle günlerce veya haftalarca açık kalır. Kodun ana entegrasyon dalına geç girmesi, çakışma (conflict) ihtimalini eksponansiyel olarak artırır. Bu mimari, Fail-Fast (hızlı başarısız olma) mantığını desteklemez; mantıksal veya yapısal çatışmalar işin en başında değil, haftalar sonraki "birleştirme gününde" ortaya çıkar.

YAGNI ve KISS İhlali: Eğer bir SaaS ürünü veya sürekli dağıtım (Continuous Deployment) yapılan bir web uygulaması geliştiriyorsanız, 5 farklı dal tipi ile çalışmak ciddi bir "You Aren't Gonna Need It" (Buna ihtiyacın olmayacak) ihlalidir. Ekibi gereksiz bürokrasiye boğarak, sistemin basitlik ve anlaşılırlık (KISS) ilkesini zedeler.

Senkronizasyon Riski: release veya hotfix dallarının iş bitiminde hem main hem de develop dallarına aynı anda birleştirilmesi zorunluluğu, manuel hatalara açıktır. develop dalının güncellenmesinin unutulması, projenin iki farklı gerçekliğe bölünmesine (drift) neden olur.

Önemli Not: Git Flow'un yaratıcısı Vincent Driessen, 2020 yılında orijinal makalesine bir not düşerek durumu güncellemiştir: "Eğer ekibiniz sürekli teslimat (Continuous Delivery) yapıyorsa, Git Flow'u projenize zorla giydirmeye (shoehorn) çalışmayın. GitHub Flow gibi çok daha basit iş akışlarını benimseyin."

Strateji Karşılaştırması: En İyi Seçeneği Belirleme
Farklı stratejilerin artıları ve eksileri üzerinden projenize en uygun modeli seçmek için aşağıdaki tabloyu değerlendirebilirsiniz:

Özellik	Git Flow	GitHub Flow	Trunk-Based Development (TBD)
Karmaşıklık / Öğrenme Eğrisi	Yüksek (5 dal tipi, katı kurallar)	Düşük (Sadece main ve feature)	En Düşük (Tek ana dal, kısa ömürlü mikro geliştirmeler)
Teslimat Hızı ve CI/CD	Yavaş (Uzun sürüm döngülerine bağlı)	Hızlı (Sürekli dağıtıma uygun)	En Hızlı (Günde çoklu canlıya çıkış, anlık geri bildirim)
Hata Tespiti (Fail-Fast)	Kötü (Çatışmalar çok geç fark edilir)	Orta (Pull Request sürecinde çözülür)	Mükemmel (Sürekli entegrasyon ile anında tespit)
En Uygun Kullanım Senaryosu	Masaüstü/Mobil uygulamalar, donanım yazılımları, paketli sürümler (v1, v2)	Web uygulamaları, SaaS ürünler, orta ölçekli çevik ekipler	Yüksek performanslı elit CI/CD ekipleri, devasa projeler
En Büyük Risk/Dezavantaj	Süreçleri yavaşlatan gereksiz iş yükü	Production'a hatalı kod çıkma riski nispeten daha fazladır	Kusursuz ve çok hızlı çalışan bir test otomasyonu (CI) gerektirir
Özetle: Ürününüz fiziksel bir cihaza yüklenen, belirli tarihlerde paketlenip dağıtılan veya geriye dönük versiyon desteği (örn: v1.5 kullanan müşteriler ile v2.0 kullanan müşterilerin aynı anda desteklenmesi) gerektiren bir sistemse Git Flow kullanmak son derece mantıklıdır.

Ekibinizin mevcut sürüm (release) sıklığı ve test otomasyonu olgunluğu ne seviyede? (Buna göre projeniz için yapısal bir Git Flow'un mu yoksa daha çevik bir Trunk-Based yaklaşımın mı uygun olduğuna kesin karar verebiliriz.)

git flow için opencode a bir skill oluşturmak için ne yapmak lazım

OpenCode üzerinde ajanın Git Flow standartlarını otonom olarak benimsemesini sağlayacak bir "skill" (yetenek) oluşturmak için belirli bir dizin yapısı kurmalı, doğru YAML frontmatter formatını kullanmalı ve ajana net sınırlar çizmelisiniz.

Sistemi YAGNI ve KISS prensiplerine uygun, karmaşadan uzak bir şekilde yapılandırmak için aşağıdaki adımları izleyebilirsiniz:

1. Dizin ve Dosya Yapısını Oluşturma
Yeteneği sadece mevcut projede kullanacaksanız proje dizininde, tüm projelerinizde kullanacaksanız global konfigürasyon dizininde ilgili klasörü ve dosyayı oluşturun:

Proje Bazlı (Tavsiye edilen başlangıç): Projenizin kök dizininde .opencode/skills/git-flow/ klasörünü oluşturun.

Global Kullanım: İşletim sisteminize göre ~/.config/opencode/skills/git-flow/ (veya ~/.claude/skills/git-flow/) klasörünü oluşturun.

Oluşturduğunuz klasörün içine SKILL.md adında bir dosya açın.

2. SKILL.md İçeriğini Hazırlama
Bu dosya, hem ajanın bu yeteneği ne zaman çağıracağını anlaması (description üzerinden) hem de çağırdığında hangi adımları izleyeceğini bilmesi için gereklidir.

Aşağıdaki şablonu kopyalayıp SKILL.md dosyanızın içine yapıştırın:

Markdown
---
name: git-flow
description: Proje sürüm yönetimi için Git Flow dallanma (branching) stratejisini uygular. Yeni özellik, sürüm veya hata düzeltme ekleneceği zaman bu yeteneği kullan.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: git
---

# Neler Yapıyorum
Bu yetenek, projedeki Git işlemlerinin katı Git Flow kurallarına (main, develop, feature/, release/, hotfix/) uygun olarak yapılmasını sağlar.

## Kullanım Şartları ve Katı Kurallar
Kullanıcı yeni bir özellik eklemeni, bir hata çözmeni veya yeni sürüm hazırlamanı istediğinde şu adımları izle:

1. **İzolasyon Prensibi:** `main` veya `develop` dalına doğrudan commit atmak KESİNLİKLE YASAKTIR.
2. **Feature (Yeni Özellik):** Yeni bir özellik geliştirilecekse, daima en güncel `develop` dalından ayrılan `feature/<kısa-tanım>` isimli bir dal oluştur (`git checkout -b feature/<isim> develop`).
3. **Hotfix (Acil Hata):** Canlı sistemde (production) acil bir düzeltme yapılacaksa `main` dalından `hotfix/<kısa-tanım>` oluştur. İşlem bitince hem `main` hem de `develop` dalına birleştir.
4. **Merge (Birleştirme):** İşlemler tamamlandığında dalları `--no-ff` (no fast-forward) bayrağı ile birleştir.
5. **DRY ve Temizlik:** Birleştirilen feature veya hotfix dallarını yerelde bırakma, silerek temiz bir çalışma alanı sağla.

## 🛑 Otonom Davranış Kısıtlamaları (Fail-Fast Durumları)
- **Merge Conflict (Çakışma):** Git birleştirme (merge) sırasında herhangi bir çakışma (conflict) meydana gelirse, çakışmayı otonom olarak çözmeye veya yamamaya ÇALIŞMA. İşlemi derhal durdur (fail-fast), durumu kullanıcıya raporla ve manuel müdahale bekle.
- **Kirli Çalışma Ağacı:** Dal değiştirmeden önce `git status` kontrolü yap. Kaydedilmemiş değişiklikler (uncommitted changes) varsa, işlemi durdur ve kullanıcıya "Değişiklikleri stash etmek ister misin?" diye sor.
3. Yeteneğe İzin (Permission) Verme
OpenCode'un güvenlik modeli gereği, yeni oluşturulan yeteneklerin ajan tarafından kullanılabilmesi için onaylanması gerekir. Projenizin kök dizinindeki opencode.json (veya ilgili konfigürasyon dosyanız) içerisine şu izin bloğunu ekleyin:

JSON
{
  "permission": {
    "skill": {
      "git-flow": "allow"
    }
  }
}
Sistem Tasarımı: Beklenen Darboğazlar ve Çözümleri
Bu yeteneği devreye alırken karşılaşabileceğiniz donanımsal veya mantıksal darboğazlar şunlardır:

Bağlam (Context) Kaybı ve Halüsinasyon: Kompleks komut zincirlerinde (özellikle hotfix sonrası kodu hem main hem de develop'a birleştirme aşamasında), ajan mevcut dalı unutup yanlış yere birleştirme yapabilir. Bu yapısal bir chokepoint'tir. Bunu önlemek için SKILL.md içindeki adımları son derece basit ve sıralı tuttuk (KISS).

State (Durum) Kilitlenmeleri: Ajan otonom çalışırken bir git merge işlemi conflict nedeniyle yarıda kesilirse, terminal "MERGING" durumunda kalır. Ajan bu durumu fark etmez ve yeni komutlar çalıştırmaya devam ederse sistem kilitlenir (loop). Bu kronik sorunu aşmak için SKILL.md içerisine "Conflict çıkarsa otonom çözmeye çalışma, anında fail-fast yap ve dur" kuralı eklenmiştir. Bu sayede sonsuz hata döngüsü ihtimali kırılmıştır.

skill.md detaylandır. ayrıca commit message kuralları da ekle

():

[isteğe bağlı detaylı gövde]

[isteğe bağlı alt bilgi / breaking change uyarısı]


### İzin Verilen Commit Tipleri (`<tip>`)
- **`feat`:** Projeye yeni bir özelliğin eklenmesi (YAGNI kuralına dikkat edilerek, sadece talep edilen).
- **`fix`:** Bir hatanın düzeltilmesi.
- **`docs`:** Sadece dökümantasyonda yapılan değişiklikler (README, API dökümanı vb.).
- **`style`:** Kodun çalışmasını etkilemeyen görsel/biçimsel değişiklikler (kod formatlama, noktalı virgül eksikleri, white-space düzeltmeleri).
- **`refactor`:** Ne bir hatayı düzelten ne de yeni bir özellik ekleyen kod değişiklikleri (kod kalitesini artırma, DRY uygulama).
- **`test`:** Eksik testlerin eklenmesi veya mevcut testlerin düzeltilmesi.
- **`chore`:** Derleme (build) süreçleri, paket yönetimi veya yardımcı araçlardaki değişiklikler (Örn: `.gitignore` güncellemesi, npm paket yüklemesi).

### Commit Mesajı Kuralları
1. **Küçük Harf Kullanımı:** `<tip>` ve `<kisa-ve-net-aciklama>` tamamen küçük harflerle yazılmalıdır.
2. **Emir Kipi:** Açıklama kısmı şimdiki zaman veya emir kipiyle yazılmalıdır (Örn: `add user login validation`, `user login validation eklendi` DEĞİL).
3. **Noktalama İşareti:** Özet başlığın sonuna nokta (.) konulmamalıdır.
4. **Kapsam (`<kapsam>`):** Değişikliğin etkilediği modül parantez içinde belirtilmelidir (Örn: `feat(auth): add google oauth2 support`).
5. **Kritik Değişiklikler (Breaking Change):** Eğer yapılan değişiklik geriye dönük uyumluluğu bozuyorsa, tipin sonuna ünlem işareti konulmalı ve gövdede detaylandırılmalıdır (Örn: `feat(api)!: remove v1 deprecated endpoints`).

---

## 3. 🛑 Güvenlik Duvarları ve Fail-Fast (Hızlı Başarısız Olma) Kuralları

Ajan, işlem sırasında aşağıdaki durumlardan biriyle karşılaşırsa **asla işleme devam etmemeli, kodu yamamaya çalışmamalı ve anında yürütmeyi durdurarak (fail-fast)** kullanıcıya rapor vermelidir:

1. **Merge Conflict (Birleştirme Çakışması):** Otomatik birleştirme başarısız olur ve çakışma çıkarsa, ajan kod bloklarını kendi kararıyla düzenlemeye çalışmamalıdır. Süreci durdurup çakışan dosyaları listelemelidir.
2. **Pre-commit / Linter Hataları:** Commit tetiklendiğinde projede tanımlı pre-commit hook'lar (Husky, ESLint, vb.) hata verir ve commit işlemini iptal ederse, ajan `--no-verify` bayrağı kullanarak bu korumayı bypass etmeye ÇALIŞMAMALIDIR. Hatayı okumalı, kodu düzeltmeli veya durup bildirmelidir.
3. **Kirli Çalışma Alanı (Dirty Working Tree):** Dal değiştirme komutundan önce kaydedilmemiş (untracked/staged) kritik kodlar varsa ve Git dal değişimini engelliyorsa, zorla (force) dal değiştirmemeli, kullanıcıya bildirmelidir.
"""

with open("SKILL.md", "w", encoding="utf-8") as f:
    f.write(skill_content.strip())

print("SKILL.md başarıyla oluşturuldu.")


Senin için Git Flow süreçlerini ve Conventional Commits standartlarını tek bir çatı altında birleştiren detaylı SKILL.md dosyasını hazırladım.
MD icon
SKILL
 MD 
Open

Sistem Tasarımında Dikkat Edilmesi Gereken Noktalar
Bu yeteneği otonom ajana (OpenCode) devrettiğinizde, sistemin doğası gereği ortaya çıkabilecek bazı mantıksal darboğazlar (chokepoints) vardır. Mimarinin güvenliğini artırmak için bu risklerin farkında olmanız önemlidir:

Commit Tipinde Anlam Karmaşası: Ajanın yaptığı kod değişikliği bazen hem feat (yeni özellik) hem de refactor (mevcut kodun yeniden yazılması) içerebilir. Ajan, bu tür gri alanlarda doğru kararı veremeyip chore gibi genel bir tipe başvurabilir. Bunun önüne geçmek için her büyük görevi parçalara bölerek (atomik commit) ajana iletmeniz faydalı olacaktır.

Linter ve Pre-commit Engelleri: Projenizde Husky, ESLint, Prettier gibi commit öncesi (pre-commit hook) denetleyiciler varsa ve ajan kodda ufak bir boşluk hatası (white-space) bile bırakırsa, Git işlemi başarısız olacaktır. Ajanın otonom olarak terminal hatalarını okuyup tekrar commit atmaya çalışması beklenmedik kilitlenmelere yol açabilir. Yetenek dosyasının Fail-Fast bölümüne, hook başarısız olduğunda ajanın zorla (bypass ederek) commit atmasını kesin bir dille yasaklayan güvenlik önlemi eklenmiştir.

İnteraktif Süreçlerde Tıkanma: Eğer Git konfigürasyonunuz bir merge işlemi sırasında Vim, Nano veya benzeri bir terminal metin düzenleyicisi açmaya çalışırsa (örneğin merge commit mesajı onayı için), CLI arayüzü kilitlenir. Ajan bu arayüzleri kapatamayacağı için işlem sonsuz döngüde asılı kalır. Bu yüzden tüm birleştirme komutlarına --no-ff ve gerektiğinde --no-edit (otomatik commit mesajı kabulü) yapılandırmalarının eşlik etmesi operasyonel bir gerekliliktir.

Yukarıdaki SKILL.md dosyasını proje kök dizininizdeki .opencode/skills/git-flow/ klasörüne kopyalayarak ajanın yetenek setine doğrudan entegre edebilirsiniz. Ajan artık her Git komutunda belirttiğimiz bu sıkı protokollere uyacaktır.




Gemini is AI and can make mistakes.

---
name: git-flow
description: Standart Git Flow dallanma modelini ve Conventional Commits (Anlamsal Commit) mesaj kurallarını projedeki tüm Git işlemlerine otonom olarak uygular.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: git-flow-conventional
---

# Git Flow ve Anlamsal Commit Yeteneği

Bu yetenek, projenin sürüm yönetimini (Git Flow) ve commit geçmişinin okunabilirliğini (Conventional Commits) disipline etmek amacıyla tasarlanmıştır. Ajan, proje içindeki tüm Git operasyonlarında aşağıda belirtilen katı kurallara ve yürütme adımlarına uymak zorundadır.

---

## 1. Dallanma Yönetimi (Git Flow Kuralları)

Ajan, yapacağı işin niteliğine göre yalnızca ilgili dalları (branch) kullanabilir. `main` veya `develop` dallarına doğrudan `commit` atmak veya doğrudan `push` yapmak kesinlikle yasaktır.

### A. Feature (Yeni Özellik) Geliştirme
- **Tetikleyici:** Yeni bir işlevsellik, kod ekleme veya yetenek geliştirme talebi.
- **Kaynak Dal:** `develop`
- **İsimlendirme:** `feature/<kisa-ozellik-adi>` (Örn: `feature/user-authentication`)
- **İş Akışı:**
  1. `git checkout develop && git pull` ile kaynak dalı güncelle.
  2. `git checkout -b feature/<isim>` ile yeni dal aç.
  3. Geliştirmeyi tamamla ve commit kurallarına uygun küçük commit'ler at.
  4. İş bittiğinde `develop` dalına geri dön, güncel kodları çek ve `git merge --no-ff feature/<isim>` ile birleştir.
  5. Yerel ve uzak `feature` dalını silerek temizlik yap.

### B. Bugfix (Hata Düzeltme)
- **Tetikleyici:** `develop` veya test aşamasında fark edilen fonksiyonel hataların çözümü.
- **Kaynak Dal:** `develop`
- **İsimlendirme:** `bugfix/<hata-tanimi>` (Örn: `bugfix/fix-token-expiration`)
- **İş Akışı:** `feature` iş akışı ile aynıdır; ancak dal ismi `bugfix/` öneki ile başlamalıdır.

### C. Hotfix (Acil Canlı Müdahale)
- **Tetikleyici:** Üretim ortamında (`main`/canlı sistem) ortaya çıkan ve anında çözülmesi gereken kritik hatalar.
- **Kaynak Dal:** `main`
- **İsimlendirme:** `hotfix/<kritik-hata-tanimi>` (Örn: `hotfix/payment-gateway-crash`)
- **İş Akışı:**
  1. `git checkout main && git pull` ile canlı ortam kodunu çek.
  2. `git checkout -b hotfix/<isim>` ile dalı oluştur.
  3. Hatayı en sade ve hızlı şekilde çöz (KISS).
  4. İşlem bitince dalı **hem `main` hem de `develop`** dallarına ayrı ayrı `--no-ff` ile birleştir.
  5. `main` dalında yeni bir versiyon etiketi (tag) oluştur (Örn: `git tag -a v1.0.1 -m "Hotfix: Payment crash fixed"`).

### D. Release (Yeni Sürüm Hazırlığı)
- **Tetikleyici:** Planlanan özelliklerin tamamlanması ve kodun canlıya çıkışa hazır hale getirilmesi.
- **Kaynak Dal:** `develop`
- **İsimlendirme:** `release/v<versiyon-numarasi>` (Örn: `release/v1.1.0`)
- **İş Akışı:** Sadece versiyon güncelleme, dökümantasyon ve son kabul test hataları bu dalda çözülür. İşlem bitince `main` ve `develop` dalları ile birleştirilir, `main` üzerinde versiyon etiketlenir.

---

## 2. Commit Mesajı Kuralları (Conventional Commits)

Ajan, üreteceği her commit mesajında **Conventional Commits 1.0.0** standartlarını uygulamak zorundadır. Mesajlar şu yapısal şablona uymalıdır:

```
<tip>(<kapsam>): <kisa-ve-net-aciklama>

[isteğe bağlı detaylı gövde]

[isteğe bağlı alt bilgi / breaking change uyarısı]
```

### İzin Verilen Commit Tipleri (`<tip>`)
- **`feat`:** Projeye yeni bir özelliğin eklenmesi (YAGNI kuralına dikkat edilerek, sadece talep edilen).
- **`fix`:** Bir hatanın düzeltilmesi.
- **`docs`:** Sadece dökümantasyonda yapılan değişiklikler (README, API dökümanı vb.).
- **`style`:** Kodun çalışmasını etkilemeyen görsel/biçimsel değişiklikler (kod formatlama, noktalı virgül eksikleri, white-space düzeltmeleri).
- **`refactor`:** Ne bir hatayı düzelten ne de yeni bir özellik ekleyen kod değişiklikleri (kod kalitesini artırma, DRY uygulama).
- **`test`:** Eksik testlerin eklenmesi veya mevcut testlerin düzeltilmesi.
- **`chore`:** Derleme (build) süreçleri, paket yönetimi veya yardımcı araçlardaki değişiklikler (Örn: `.gitignore` güncellemesi, npm paket yüklemesi).

### Commit Mesajı Kuralları
1. **Küçük Harf Kullanımı:** `<tip>` ve `<kisa-ve-net-aciklama>` tamamen küçük harflerle yazılmalıdır.
2. **Emir Kipi:** Açıklama kısmı şimdiki zaman veya emir kipiyle yazılmalıdır (Örn: `add user login validation`, `user login validation eklendi` DEĞİL).
3. **Noktalama İşareti:** Özet başlığın sonuna nokta (.) konulmamalıdır.
4. **Kapsam (`<kapsam>`):** Değişikliğin etkilediği modül parantez içinde belirtilmelidir (Örn: `feat(auth): add google oauth2 support`).
5. **Kritik Değişiklikler (Breaking Change):** Eğer yapılan değişiklik geriye dönük uyumluluğu bozuyorsa, tipin sonuna ünlem işareti konulmalı ve gövdede detaylandırılmalıdır (Örn: `feat(api)!: remove v1 deprecated endpoints`).

---

## 3. 🛑 Güvenlik Duvarları ve Fail-Fast (Hızlı Başarısız Olma) Kuralları

Ajan, işlem sırasında aşağıdaki durumlardan biriyle karşılaşırsa **asla işleme devam etmemeli, kodu yamamaya çalışmamalı ve anında yürütmeyi durdurarak (fail-fast)** kullanıcıya rapor vermelidir:

1. **Merge Conflict (Birleştirme Çakışması):** Otomatik birleştirme başarısız olur ve çakışma çıkarsa, ajan kod bloklarını kendi kararıyla düzenlemeye çalışmamalıdır. Süreci durdurup çakışan dosyaları listelemelidir.
2. **Pre-commit / Linter Hataları:** Commit tetiklendiğinde projede tanımlı pre-commit hook'lar (Husky, ESLint, vb.) hata verir ve commit işlemini iptal ederse, ajan `--no-verify` bayrağı kullanarak bu korumayı bypass etmeye ÇALIŞMAMALIDIR. Hatayı okumalı, kodu düzeltmeli veya durup bildirmelidir.
3. **Kirli Çalışma Alanı (Dirty Working Tree):** Dal değiştirme komutundan önce kaydedilmemiş (untracked/staged) kritik kodlar varsa ve Git dal değişimini engelliyorsa, zorla (force) dal değiştirmemeli, kullanıcıya bildirmelidir.
SKILL.md
Displaying SKILL.md.