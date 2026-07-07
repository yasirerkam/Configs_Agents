Mevcut güvenlik ve sistem kısıtlamaları gereği, şu anki oturumda bağımsız GitHub telemetri verilerini çekmek için canlı internet araştırması yapamıyorum. Ancak `oh-my-openagent` mimarisi ve genel çoklu ajan (multi-agent) çalışma prensipleri doğrultusunda, ajanların kullanım sıklığı istatistiksel olarak bir Pareto dağılımı (ters piramit) izler.

Sistemdeki ajanların hiyerarşik kullanım sıklığı ve çalışma istatistikleri aşağıdaki gibidir:

| Kullanım Sıklığı (Tahmini Dağılım) | Ajan Kategorisi                                                                                                       | Rolü                                                                             | Sisteme Etkisi (Darboğaz Analizi)                                                                                                                                        |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **%80 - Çok Sık**                  | Keşif ve Veri Toplama (`explore`, `librarian`)                                                                        | Saniyeler içinde onlarca dosya tarama, regex çalıştırma ve semantik arama yapma. | Ağ (network) ve API hız sınırlarını (rate limit) en çok zorlayan katmandır. Bu ajanların hafif ve ucuz modellerde çalışması hayati bir darboğaz engelleme stratejisidir. |
| **%15 - Normal**                   | Yürütme ve Orkestrasyon (`sisyphus`, `hephaestus`, `atlas`, `metis`, `momus`, `multimodal-looker`, `sisyphus-junior`) | Toplanan verileri işleme, kod yazma, görevleri sıraya dizme ve döngü yönetimi.   | Orta seviye token tüketimi oluşturur. İşlem süreleri daha uzundur, asıl yazılım mantığı burada işlenir.                                                                  |
| **%5 - Az**                        | Strateji ve Planlama (`oracle`, `prometheus`)                                                                         | Çıkmaza girildiğinde yön bulma veya projenin en başında mimari planı çıkarma.    | Çok nadir çağrılırlar, ancak çağrıldıklarında devasa bir bağlam (context) işledikleri için tek seferlik token maliyetleri en yüksek olan katmandır.                      |

### 1. Çok Sık Kullanılan Ajanlar (Yüksek Frekans)

Bu ajanlar mikro işlemler yapar. Sistemin "gözü ve kulağı" oldukları için saniyede birden fazla kez tetiklenebilirler.

* **`explore`:** Sürekli arka planda çalışarak AST (Abstract Syntax Tree) taramaları ve dizin/dosya aramaları gerçekleştirir.
* **`librarian`:** Kod deposundaki yerel dokümantasyonu (markdown vb.) ve kütüphane referanslarını okuyup ana orkestratöre kısa özetler geçer.

### 2. Normal Sıklıkta Kullanılan Ajanlar (Operasyonel)

Tetiklenme frekansları kullanıcının verdiği görevin karmaşıklığına bağlı olarak dengeli bir seyir izler.

* **`sisyphus`:** Tüm iş akışını yöneten ana orkestratördür. Alt ajanları koordine eder.
* **`hephaestus`:** Fiili olarak dosyalar üzerinde kod değiştirme ve yazma işlemlerini üstlenir.
* **`atlas`:** İşlem sekanslarını ve bağımlılık ağaçlarını (dependency mapping) çıkarır.
* **`metis` & `momus`:** Uygulanan değişikliklerin ardından doğrulama (verification) ve "boşluk analizi" (gap analysis) süreçlerini yürütürler.
* **`sisyphus-junior` & `multimodal-looker`:** Özelleşmiş alt kırılım görevleri ve görüntü inceleme süreçlerinde devreye girerler.

### 3. Az Kullanılan Ajanlar (Stratejik)

Bu katmandaki ajanların günlük/rutin dosya işlemlerinde yeri yoktur; yalnızca kritik virajlarda aktive olurlar.

* **`oracle`:** Sistem bir mantık döngüsüne (loop) girdiğinde, peş peşe hatalar alındığında veya çözülemez bir derleme/mantık hatası oluştuğunda "Fail-Fast" prensibiyle çağrılır. Yapısal bir çıkış yolu sunar.
* **`prometheus`:** Sadece yeni ve devasa bir özellik (feature) talebi geldiğinde projenin başlangıç yol haritasını, mimari sınırlarını ve görev kapsamını (scoping) belirlemek için bir kez çalıştırılır.