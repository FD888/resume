#!/usr/bin/env python3
"""Сборка резюме Буйдалина Дениса в PDF (A4, одна страница).

Весь контент лежит в словаре RESUME ниже — чтобы обновить резюме,
правим данные и запускаем:  python build_resume.py
"""
from pathlib import Path
import sys

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Buydalin_Denis_Resume.pdf"
PHOTO = ROOT / "photo.jpg"

# ---------------------------------------------------------------- контент
RESUME = {
    "last_name": "БУЙДАЛИН",
    "first_name": "ДЕНИС СТЕПАНОВИЧ",
    "title": "Product Manager",
    "about": (
        "Продакт-менеджер и предприниматель на стыке экономики и искусственного "
        "интеллекта. Специализируюсь на агентно-ориентированном подходе к работе "
        "с информацией: проектирую AI-агентов и инструменты, которые собирают, "
        "структурируют и анализируют данные вместо людей. Разрабатываю AI-first — "
        "сам довожу продукт от идеи до работающего решения. Интересуюсь "
        "австрийской экономической школой. "
        "Студент 4 курса экономического факультета СПбГУ."
    ),
    "contacts": [
        "Санкт-Петербург",
        "+7 (918) 608-72-07",
        "buydalin.buy@mail.ru",
        "TG: @excentresitet",
        "GitHub: FD888",
    ],
    "skills": [
        "Продуктовая стратегия",
        "Customer Development",
        "Customer Journey (CJM)",
        "Юнит-экономика",
        "Продуктовые метрики",
        "MVP-разработка",
        "AI-агенты / агентные системы",
        "AI-first разработка",
        "Claude Code",
        "BI-инструменты / дашборды",
        "Автоматизация процессов",
        "Мобильные приложения",
        "Telegram Mini Apps",
        "1С (внедрение)",
        "Фин. моделирование",
        "DCF-анализ",
        "Excel / Google Sheets",
        "Adobe Photoshop",
        "Git / GitHub",
    ],
    "languages": ["Русский — родной", "Английский — B1"],
    "work_format": ["Удалённая работа / Офис"],
    "experience": [
        {
            "role": "Customer Journey Expert",
            "org": "ВТБ",
            "date": "Июл 2026 — н.в.",
            "bullets": [
                "Команда и продукт «Тематические каналы» в ВТБ Онлайн",
                "Создал внутренний BI-инструмент для статистики каналов — замену DataLens, "
                "недоступного внутри контура",
                "Генератор постов и микроавтоматизации рутины команды (AI-first)",
            ],
        },
        {
            "role": "Сооснователь, продакт-менеджер",
            "org": "notvik",
            "date": "2026 — н.в.",
            "bullets": [
                "Мобильное приложение для заметок с ИИ: голос, текст и скриншоты "
                "превращаются в структурированные заметки, задачи и напоминания",
                "Один из 4 сооснователей; отвечаю за концепцию и продукт в целом",
                "~80 DAU, цель — 1 000 DAU к концу ноября 2026",
            ],
        },
        {
            "role": "Основатель и разработчик",
            "org": "ТГДОМ",
            "date": "2025",
            "bullets": [
                "SaaS для риелторов: каталоги недвижимости в Telegram Mini Apps; "
                "MVP в одиночку (AI-first), первые пользователи",
            ],
        },
        {
            "role": "Специалист отдела внедрения",
            "org": 'ООО "Альфа-Софт"',
            "date": "Июл — Сен 2025",
            "bullets": [
                "Внедрение продуктов 1С в компаниях-клиентах: настройка, адаптация, "
                "обучение и сопровождение пользователей",
            ],
        },
        {
            "role": "Основатель",
            "org": "ТолькаПринтер",
            "date": "2024",
            "bullets": [
                "Сервис печати документов через Telegram-бота; команда из 3 человек; "
                "заявка на грант «Студенческий стартап»",
            ],
        },
        {
            "role": "Финансовый консультант",
            "org": "СКС Банк",
            "date": "Июн — Авг 2022",
            "bullets": [
                "Продажа банковских продуктов в розничном отделении: кредитные "
                "и дебетовые карты, ОСАГО",
            ],
        },
    ],
    "achievements": [
        {
            "role": "Топ-50 команд — Sber500 x Disrupt",
            "org": "Сбер",
            "date": "2026",
            "bullets": [
                "AI-программа Сбера (фонд 30 млн ₽): notvik во 2 этапе, боремся за победу",
            ],
        },
        {
            "role": "Топ-50 — Youth Liberty Prize 2026",
            "org": "Fundación Jesús Huerta de Soto",
            "date": "2026",
            "bullets": [
                "Международный конкурс эссе по австрийской школе (фонд €170 000): "
                "«The Invisible Hand of Knowledge» — топ-50 из 1 142 работ",
            ],
        },
        {
            "role": "BI-инструмент, принятый соседними командами",
            "org": "ВТБ",
            "date": "2026",
            "bullets": [
                "Сделал в одиночку — пользуются моя и соседние команды",
            ],
        },
        {
            "role": "3 место — Конкурс студенческих инициатив",
            "org": "Минэкономразвития РФ",
            "date": "",
            "bullets": [
                "Проект солнечно-дождевых панелей в СПб и ЛО; защита перед Министром "
                "экономического развития М.Г. Решетниковым",
            ],
        },
        {
            "role": "Финалист AI Boost Camp",
            "org": "K2 Нейротех",
            "date": "",
            "bullets": [
                "AI-фильтр false-positive срабатываний для разработчиков; отвечал "
                "за продуктовую и бизнес-часть: юнит-экономика, метрики, окупаемость",
            ],
        },
        {
            "role": "Основатель сообщества VibeFounders",
            "org": "",
            "date": "",
            "bullets": [
                "Мастермайнд-группа AI-first предпринимателей (6 участников): "
                "еженедельные встречи, трекинг проектов, обмен опытом",
            ],
        },
        {
            "role": "Резидент Фонда «Лидеры будущего»",
            "org": "набор 2022",
            "date": "",
            "bullets": [],
        },
    ],
    "education": [
        {
            "role": "СПбГУ — Экономический факультет",
            "org": "Бакалавриат",
            "date": "2023 — 2027",
            "bullets": ["Специальность: экономика. 4 курс"],
        },
    ],
}

# ---------------------------------------------------------------- оформление
BLUE = HexColor("#2b5797")
LIGHT_BLUE = HexColor("#a8c6e8")
TEXT = HexColor("#333333")
GREY = HexColor("#666666")

PAGE_W, PAGE_H = A4
SIDEBAR_W = 204.09
SIDE_X, SIDE_R = 22.68, 181.42
MAIN_X, MAIN_R = 232.44, 561.26
BOTTOM = 28

FONT_DIRS = [
    ROOT / "fonts",
    Path("/usr/share/fonts/truetype"),
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/dejavu"),
    Path("/Library/Fonts"),
    Path.home() / "Library/Fonts",
]


def register_fonts():
    for name, file in (("Sans", "DejaVuSans.ttf"), ("Sans-Bold", "DejaVuSans-Bold.ttf")):
        for d in FONT_DIRS:
            if (d / file).exists():
                pdfmetrics.registerFont(TTFont(name, str(d / file)))
                break
        else:
            sys.exit(f"Не найден шрифт {file}: положите его в ./fonts/")


def wrap(text, font, size, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Resume:
    def __init__(self, c):
        self.c = c

    # -- sidebar ---------------------------------------------------------
    def sidebar(self, data):
        c = self.c
        c.setFillColor(BLUE)
        c.rect(0, 0, SIDEBAR_W, PAGE_H, stroke=0, fill=1)

        # фото в белой рамке со скруглёнными углами
        fx, fy, fs = 31.18, PAGE_H - 184.25, 141.73
        c.setFillColor(white)
        c.setStrokeColor(white)
        c.setLineWidth(2)
        c.roundRect(fx, fy, fs, fs, 10, stroke=1, fill=0)
        if PHOTO.exists():
            img = ImageReader(str(PHOTO))
            iw, ih = img.getSize()
            h = fs - 4
            w = h * iw / ih
            c.drawImage(img, fx + (fs - w) / 2, fy + 2, w, h)

        y = PAGE_H - 220
        for title, items, size in (
            ("КОНТАКТЫ", data["contacts"], 7.5),
            ("НАВЫКИ", data["skills"], 7.2),
            ("ЯЗЫКИ", data["languages"], 7.5),
            ("ФОРМАТ РАБОТЫ", data["work_format"], 7.5),
        ):
            c.setFillColor(LIGHT_BLUE)
            c.setFont("Sans-Bold", 9)
            c.drawString(SIDE_X, y, title)
            c.setStrokeColor(LIGHT_BLUE)
            c.setLineWidth(0.5)
            c.line(SIDE_X, y - 3.5, SIDE_R, y - 3.5)
            y -= 16
            c.setFillColor(white)
            c.setFont("Sans", size)
            for item in items:
                c.drawString(SIDE_X, y, item)
                y -= size + 4.2
            y -= 14

    # -- main column -----------------------------------------------------
    def section(self, y, title):
        c = self.c
        c.setFillColor(BLUE)
        c.setFont("Sans-Bold", 10)
        c.drawString(MAIN_X, y, title)
        c.setStrokeColor(BLUE)
        c.setLineWidth(1)
        c.line(MAIN_X, y - 3, MAIN_R, y - 3)
        return y - 14

    def entry(self, y, e):
        c = self.c
        c.setFillColor(TEXT)
        c.setFont("Sans-Bold", 8.5)
        c.drawString(MAIN_X, y, e["role"])
        if e["org"]:
            x = MAIN_X + pdfmetrics.stringWidth(e["role"], "Sans-Bold", 8.5)
            c.setFillColor(GREY)
            c.setFont("Sans", 7.5)
            c.drawString(x, y, f"  | {e['org']}")
            x += pdfmetrics.stringWidth(f"  | {e['org']}", "Sans", 7.5)
            if e["date"] and x > MAIN_R - pdfmetrics.stringWidth(e["date"], "Sans", 7.5) - 6:
                sys.exit(f"Заголовок наезжает на дату: {e['role']} | {e['org']}")
        if e["date"]:
            c.setFillColor(GREY)
            c.setFont("Sans", 7.5)
            c.drawRightString(MAIN_R, y, e["date"])
        y -= 11.5
        for b in e["bullets"]:
            lines = wrap(b, "Sans", 7.5, MAIN_R - MAIN_X - 12)
            c.setFillColor(BLUE)
            c.setFont("Sans", 8)
            c.drawString(MAIN_X + 3, y, "—")
            c.setFillColor(TEXT)
            c.setFont("Sans", 7.5)
            for line in lines:
                c.drawString(MAIN_X + 12, y, line)
                y -= 9.6
        return y - 4

    def main(self, data):
        c = self.c
        c.setFillColor(BLUE)
        c.setFont("Sans-Bold", 22)
        c.drawString(MAIN_X, PAGE_H - 56, data["last_name"])
        c.drawString(MAIN_X, PAGE_H - 84, data["first_name"])
        c.setFillColor(GREY)
        c.setFont("Sans", 11)
        c.drawString(MAIN_X, PAGE_H - 102, data["title"])

        y = self.section(PAGE_H - 134, "О СЕБЕ")
        c.setFillColor(TEXT)
        c.setFont("Sans", 7.8)
        for line in wrap(data["about"], "Sans", 7.8, MAIN_R - MAIN_X):
            c.drawString(MAIN_X, y, line)
            y -= 10.2
        y -= 8

        for title, key in (
            ("ОПЫТ РАБОТЫ И ПРОЕКТЫ", "experience"),
            ("ДОСТИЖЕНИЯ", "achievements"),
            ("ОБРАЗОВАНИЕ", "education"),
        ):
            y = self.section(y, title)
            for e in data[key]:
                y = self.entry(y, e)
            y -= 6
        return y


def build():
    register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Буйдалин Денис — резюме")
    c.setAuthor("Буйдалин Денис Степанович")
    r = Resume(c)
    r.sidebar(RESUME)
    y = r.main(RESUME)
    c.save()
    if y < BOTTOM:
        sys.exit(f"Контент не влезает на страницу (y={y:.0f} < {BOTTOM}) — сократите текст")
    print(f"OK: {OUT} (запас снизу {y - BOTTOM:.0f} pt)")


if __name__ == "__main__":
    build()
