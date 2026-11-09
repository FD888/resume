# Резюме — Буйдалин Денис

Актуальная версия: [Buydalin_Denis_Resume.pdf](Buydalin_Denis_Resume.pdf)

## Сборка

PDF генерируется скриптом `build_resume.py` (ReportLab, шрифт DejaVu Sans).
Весь текст резюме лежит в словаре `RESUME` в начале скрипта.

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build_resume.py
```

Скрипт проверяет, что всё помещается на одну страницу A4 и заголовки не наезжают на даты.
Если шрифт DejaVu не найден в системе — положите `DejaVuSans.ttf` и `DejaVuSans-Bold.ttf` в `./fonts/`.
