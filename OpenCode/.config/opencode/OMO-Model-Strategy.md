# Oh-My-OpenAgent Model Eşleme Stratejisi

> OpenCode Go Aboneliği + OpenCode Zen Free Fallback
> Son Güncelleme: 2026-06-27

---

## Tier Sistemi

| Tier       | Zeka       | Kullanım Sıklığı | Modeller                                                                                                            |
| ---------- | ---------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Tier 1** | Çok Yüksek | Çok Az           | **Qwen3.7 Max**                                                                                                     |
| **Tier 2** | Yüksek     | Az / Az-Orta     | **DeepSeek V4 Pro**, **Qwen3.7 Plus**, **Kimi K2.7 Code**, **MiMo-V2.5-Pro**, **Kimi K2.6**                         |
| **Tier 3** | Orta       | Çok Sık          | **MiniMax M3**                                                                                                      |
| **Tier 4** | Az         | Çok Sık          | **MiMo-V2.5**, **DeepSeek V4 Flash**                                                                                |
| **Tier 5** | -          | -                | **MiMo-V2.5 Free**, **DeepSeek V4 Flash Free**, **Nemotron 3 Ultra Free**, **North Mini Code Free**, **Big Pickle** |

---

## Agent Eşleme Tablosu

| Agent                 | Kullanım | Zeka       | Primary             | Fallback Zinciri                                                                                                                |
| --------------------- | -------- | ---------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Momus**             | Çok Az   | Çok Yüksek | **Qwen3.7 Max**     | DeepSeek V4 Pro → Qwen3.7 Plus → Kimi K2.7 Code → MiMo-V2.5-Pro → Kimi K2.6 → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free |
| **Metis**             | Çok Az   | Çok Yüksek | **Qwen3.7 Max**     | DeepSeek V4 Pro → Qwen3.7 Plus → Kimi K2.7 Code → MiMo-V2.5-Pro → Kimi K2.6 → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free |
| **Prometheus**        | Az       | Çok Yüksek | **DeepSeek V4 Pro** | Qwen3.7 Plus → Kimi K2.7 Code → MiMo-V2.5-Pro → Kimi K2.6 → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free                   |
| **Oracle**            | Az       | Yüksek     | **Qwen3.7 Plus**    | Kimi K2.7 Code → MiMo-V2.5-Pro → Kimi K2.6 → DeepSeek V4 Pro → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free                |
| **Hephaestus**        | Az-Orta  | Yüksek     | **Kimi K2.7 Code**  | MiMo-V2.5-Pro → Kimi K2.6 → Qwen3.7 Plus → DeepSeek V4 Pro → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free                  |
| **Atlas**             | Orta     | Yüksek     | **MiMo-V2.5-Pro**   | Kimi K2.6 → Qwen3.7 Plus → DeepSeek V4 Pro → Kimi K2.7 Code → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free                 |
| **Sisyphus**          | Çok Sık  | Yüksek     | **Kimi K2.6**       | Qwen3.7 Plus → DeepSeek V4 Pro → Kimi K2.7 Code → MiMo-V2.5-Pro → MiniMax M3 → MiMo-V2.5 → DeepSeek V4 Flash → Free             |
| **Multimodal-Looker** | Çok Az   | Yüksek     | **Kimi K2.6**       | Qwen3.7 Plus → DeepSeek V4 Pro → MiMo-V2.5-Pro → MiniMax M3 → Free                                                              |
| **Sisyphus-Junior**   | Çok Sık  | Orta       | **MiniMax M3**      | Kimi K2.6 → MiMo-V2.5 → DeepSeek V4 Flash → Free                                                                                |
| **Librarian**         | Sık      | Orta       | **MiniMax M3**      | Kimi K2.6 → MiMo-V2.5 → DeepSeek V4 Flash → Free                                                                                |
| **Explore**           | Çok Sık  | Az         | **MiMo-V2.5**       | DeepSeek V4 Flash → MiniMax M3 → Free                                                                                           |

---

## Kategori Eşleme Tablosu

| Kategori               | Kullanım | Zeka       | Primary               | Fallback Zinciri                                                          |
| ---------------------- | -------- | ---------- | --------------------- | ------------------------------------------------------------------------- |
| **ultrabrain**         | Çok Az   | Çok Yüksek | **Qwen3.7 Max**       | DeepSeek V4 Pro → Qwen3.7 Plus → Kimi K2.7 Code → Kimi K2.6 → MiniMax M3  |
| **unspecified-high**   | Az       | Çok Yüksek | **DeepSeek V4 Pro**   | Qwen3.7 Plus → Kimi K2.7 Code → MiMo-V2.5-Pro → Kimi K2.6 → MiniMax M3    |
| **deep**               | Az-Orta  | Yüksek     | **Qwen3.7 Plus**      | Kimi K2.7 Code → MiMo-V2.5-Pro → Kimi K2.6 → DeepSeek V4 Pro → MiniMax M3 |
| **artistry**           | Az       | Yüksek     | **Kimi K2.7 Code**    | MiMo-V2.5-Pro → Kimi K2.6 → Qwen3.7 Plus → DeepSeek V4 Pro → MiniMax M3   |
| **visual-engineering** | Orta     | Yüksek     | **MiMo-V2.5-Pro**     | Kimi K2.6 → Qwen3.7 Plus → DeepSeek V4 Pro → MiniMax M3 → MiMo-V2.5       |
| **writing**            | Sık      | Orta       | **MiniMax M3**        | Kimi K2.6 → MiMo-V2.5 → DeepSeek V4 Flash                                 |
| **quick**              | Çok Sık  | Az         | **MiMo-V2.5**         | DeepSeek V4 Flash → MiniMax M3 → Free                                     |
| **unspecified-low**    | Çok Sık  | Az         | **DeepSeek V4 Flash** | MiMo-V2.5 → MiniMax M3 → Free                                             |

---

## Dağıtım Mantığı

- **Tier 1 (Qwen3.7 Max)**: Sadece çok az kullanılan ve çok yüksek zeka gerektiren Momus ve Metis'e. Her promptta değil, plan onayı gibi kritik anlarda devreye girer.
- **Tier 2 (DeepSeek V4 Pro / Qwen3.7 Plus / Kimi K2.7 Code / MiMo-V2.5-Pro / Kimi K2.6)**: Yüksek zeka gerektiren ama maliyetli agent'lara. Kullanım sıklığına göre Tier 2 içinde dağıtıldı:
  - Az kullanılanlar (Prometheus, Oracle) → Daha pahalı/güçlü modeller.
  - Çok sık kullanılan (Sisyphus) → Tier 2'nin en maliyet-etkin güçlü modeli (Kimi K2.6).
- **Tier 3 (MiniMax M3)**: Çok sık çağrılan orta-zeka agent'ları (Sisyphus-Junior, Librarian). Orta maliyet, yüksek kullanım.
- **Tier 4 (MiMo-V2.5 / DeepSeek V4 Flash)**: Çok sık çağrılan basit işler (Explore, quick, unspecified-low). Düşük maliyet.
- **Tier 5 (Zen Free)**: Tüm zincirlerin son güvenlik ağı. Ücretli modeller patlarsa veya limit dolarsa free modellere düşer.

---

## Önemli Notlar

- `runtime_fallback` API hatalarında otomatik model değişimi için aktiftir.
- `hashline_edit` ve `new_task_system_enabled` aktiftir.
