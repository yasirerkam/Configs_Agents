---

# VS Code Çoklu Satır (Multiline) Arama ve Regex Notları

## 1. Arama Kutusunda "Çoklu Satır" (Multiline) Kısayolunu Kullanmak

Arama kutusunu (`Ctrl + F`) çoklu satır moduna geçirmek ve standart regex aramalarının takılmasını önlemek için:

* Arama kutusuna tıklayın.
* Klavyeden **`Alt + Enter`** (macOS'ta `Option + Enter`) tuşlarına basın.
* Bu işlem arama kutusunu dikey olarak genişletir ve VS Code'un regex motorunun `\n` (satır sonu) karakterlerini otomatik olarak daha esnek okumasını sağlar.

## 2. Regex ile Çözüm (Ripgrep Satır Atlama Darboğazını Aşmak)

VS Code arama motoru (Ripgrep) çoklu satır eşleşmelerinde standart joker karakterleri (`.*` veya `[\s\S]`) genellikle yoksayar. Satır atlamak için açıkça `\n` karakterini (newline literal) bir karakter sınıfı `[...]` içinde tanımlamak zorunludur.

VS Code'un satır sonlarında takılmasını engellemek için, belirsiz joker karakterler kullanmak yerine sadece bloğun içindeki karakterleri ve `\n` literalini içeren spesifik bir regex kullanılmalıdır.

**Örnek Regex Deseni:**

```regex
"fallback_models":[\n\s]*\[[\n\s\w"/:{},.\-]*\]

```

**Bu Desenin Çalışma Mantığı:**

* `"fallback_models":` Başlangıç noktasını yakalar.
* `[\n\s]*\[` Köşeli paranteze kadar olan tüm boşlukları ve satır atlamalarını (`\n`) açıkça ve zorla okutur.
* `[\n\s\w"/:{},.\-]*` **Kilit nokta:** Motoru "her şeyi seç" (`.*`) diyerek kilitlenmesine sebep olmak yerine, motorun sadece şunları aramasını sağlar:
* Satır atlamaları (`\n`) ve boşluklar (`\s`)
* Harfler ve rakamlar (`\w`)
* Tırnak (`"`), iki nokta (`:`), virgül (`,`), süslü parantez (`{}`), bölü (`/`), tire (`-`), nokta (`.`)


* `\]` Karakter setinin içinde `]` olmadığı için, motor diğer satırları tek tek `\n` yardımıyla geçer ve ilk kapalı köşeli parantezi gördüğünde güvenle durur.