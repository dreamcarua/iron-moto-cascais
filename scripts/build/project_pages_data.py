"""Structured source data for generated project pages."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[2]

LANGUAGE_SECTIONS = {
    "ENGLISH": "en",
    "PORTUGUÊS (pt-PT)": "pt",
    "РУССКИЙ": "ru",
    "УКРАЇНСЬКА": "uk",
}

MARKDOWN_PROJECT_CONFIGS = {
    "fighter": {
        "source": SITE_ROOT / "content/projects/fighter_4lang.md",
        "year": "2014",
        "published_iso": "2026-07-27T12:00:00+01:00",
        "hero_base": "/photos/projects/fighter",
        "hero_source": "Fighter_HERO.jpg",
        "gallery_base": "/photos/projects/gallery/fighter/fighter",
        "gallery_sources": [
            "134632_000_3727.jpg",
            "141001_000_3785.jpg",
            "135441_000_3736.jpg",
            "142638_000_3830.jpg",
            "142159_000_3819.jpg",
            "135357_000_3732.jpg",
            "135823_000_3753.jpg",
            "142952_000_3842.jpg",
            "135340_000_3729.jpg",
            "135727_000_3748.jpg",
            "141201_000_3792.jpg",
        ],
        "ui": {
            "en": {
                "home": "Home",
                "projects": "Projects",
                "badge": "Long Chopper · Full Custom",
                "year_label": "Year",
                "category_label": "Category",
                "category": "Long Chopper · Full Custom",
                "where_label": "Where",
                "where": "Built in Kharkiv, Ukraine",
                "gallery": "Gallery",
                "gallery_title": "<em>Fighter</em> — in detail.",
            },
            "pt": {
                "home": "Início",
                "projects": "Projetos",
                "badge": "Long Chopper · Full Custom",
                "year_label": "Ano",
                "category_label": "Categoria",
                "category": "Long Chopper · Full Custom",
                "where_label": "Local",
                "where": "Construído em Kharkiv, Ucrânia",
                "gallery": "Galeria",
                "gallery_title": "<em>Fighter</em> — em detalhe.",
            },
            "ru": {
                "home": "Главная",
                "projects": "Проекты",
                "badge": "Лонг-чоппер · Full Custom",
                "year_label": "Год",
                "category_label": "Категория",
                "category": "Лонг-чоппер · Full Custom",
                "where_label": "Где",
                "where": "Построен в Харькове, Украина",
                "gallery": "Галерея",
                "gallery_title": "<em>Fighter</em> — в деталях.",
            },
            "uk": {
                "home": "Головна",
                "projects": "Проєкти",
                "badge": "Лонг-чопер · Full Custom",
                "year_label": "Рік",
                "category_label": "Категорія",
                "category": "Лонг-чопер · Full Custom",
                "where_label": "Де",
                "where": "Збудовано у Харкові, Україна",
                "gallery": "Галерея",
                "gallery_title": "<em>Fighter</em> — у деталях.",
            },
        },
        "gallery_alts": {
            "en": [
                "Fighter long chopper rear fender and custom taillight detail",
                "Fighter long chopper passenger seat and Green Plazma paint detail",
                "Fighter long chopper RevTech engine and Samson exhaust detail",
                "Fighter long chopper Spyke ignition and engine detail",
                "Fighter long chopper BDL open primary drive detail",
                "Fighter long chopper RevTech 110 engine detail",
                "Fighter long chopper fuel tank and cockpit detail",
                "Fighter long chopper Wicked Image wheel and brake detail",
                "Fighter long chopper Green Plazma fuel tank and fork detail",
                "Fighter long chopper full side view",
                "Fighter long chopper with rider outdoors",
            ],
            "pt": [
                "Fighter long chopper, detalhe do guarda-lamas traseiro e farolim custom",
                "Fighter long chopper, detalhe do lugar de pendura e pintura Green Plazma",
                "Fighter long chopper, detalhe do motor RevTech e escape Samson",
                "Fighter long chopper, detalhe da ignição Spyke e do motor",
                "Fighter long chopper, detalhe da primária aberta BDL",
                "Fighter long chopper, detalhe do motor RevTech 110",
                "Fighter long chopper, detalhe do depósito e posto de condução",
                "Fighter long chopper, detalhe da roda Wicked Image e travão",
                "Fighter long chopper, detalhe do depósito Green Plazma e forquilha",
                "Fighter long chopper, vista lateral completa",
                "Fighter long chopper com piloto no exterior",
            ],
            "ru": [
                "Fighter лонг-чоппер — заднее крыло и кастомный фонарь",
                "Fighter лонг-чоппер — пассажирское сиденье и краска Green Plazma",
                "Fighter лонг-чоппер — мотор RevTech и выхлоп Samson",
                "Fighter лонг-чоппер — зажигание Spyke и детали мотора",
                "Fighter лонг-чоппер — открытая первичная передача BDL",
                "Fighter лонг-чоппер — мотор RevTech 110",
                "Fighter лонг-чоппер — бак и кокпит",
                "Fighter лонг-чоппер — колесо Wicked Image и тормоз",
                "Fighter лонг-чоппер — бак Green Plazma и вилка",
                "Fighter лонг-чоппер — полный вид сбоку",
                "Fighter лонг-чоппер с пилотом",
            ],
            "uk": [
                "Fighter лонг-чопер — заднє крило та кастомний ліхтар",
                "Fighter лонг-чопер — пасажирське сидіння та фарба Green Plazma",
                "Fighter лонг-чопер — мотор RevTech і вихлоп Samson",
                "Fighter лонг-чопер — запалювання Spyke та деталі мотора",
                "Fighter лонг-чопер — відкрита первинна передача BDL",
                "Fighter лонг-чопер — мотор RevTech 110",
                "Fighter лонг-чопер — бак і кокпіт",
                "Fighter лонг-чопер — колесо Wicked Image і гальмо",
                "Fighter лонг-чопер — бак Green Plazma та вилка",
                "Fighter лонг-чопер — повний вигляд збоку",
                "Fighter лонг-чопер із пілотом",
            ],
        },
    },
    "cocktail": {
        "source": SITE_ROOT / "content/projects/cocktail_4lang.md",
        "year": "2013",
        "published_iso": "2026-08-01T14:55:25+01:00",
        "modified_iso": "2026-08-04T07:03:42+01:00",
        "hero_base": "/photos/projects/cocktail",
        "hero_source": "Cocktail_HERO.jpg",
        "gallery_base": "/photos/projects/gallery/cocktail/cocktail",
        "gallery_sources": [
            "100507_DSC_5007.jpg",
            "100516_DSC_5008.jpg",
            "181033_IMG_9708.jpg",
            "100447_DSC_5005.jpg",
            "183048_IMG_9728.jpg",
            "183830_IMG_9744.jpg",
            "144307_DSC_5364.jpg",
            "144351_DSC_5369.jpg",
            "190848_IMG_5720.jpg",
            "190740_IMG_5716.jpg",
        ],
        "jpeg_fallback": True,
        "integrations": {
            "custom": True,
            "harley_custom": True,
        },
        "ui": {
            "en": {
                "home": "Home",
                "projects": "Projects",
                "badge": "Bagger · Full Custom",
                "year_label": "Year",
                "category_label": "Category",
                "category": "Bagger · Full Custom",
                "where_label": "Where",
                "where": "Built in Kharkiv, Ukraine",
                "gallery": "Gallery",
                "gallery_title": "<em>Cocktail</em> — in detail.",
            },
            "pt": {
                "home": "Início",
                "projects": "Projetos",
                "badge": "Bagger · Full Custom",
                "year_label": "Ano",
                "category_label": "Categoria",
                "category": "Bagger · Full Custom",
                "where_label": "Local",
                "where": "Construído em Kharkiv, Ucrânia",
                "gallery": "Galeria",
                "gallery_title": "<em>Cocktail</em> — em detalhe.",
            },
            "ru": {
                "home": "Главная",
                "projects": "Проекты",
                "badge": "Бэггер · Full Custom",
                "year_label": "Год",
                "category_label": "Категория",
                "category": "Бэггер · Full Custom",
                "where_label": "Где",
                "where": "Построен в Харькове, Украина",
                "gallery": "Галерея",
                "gallery_title": "<em>Cocktail</em> — в деталях.",
            },
            "uk": {
                "home": "Головна",
                "projects": "Проєкти",
                "badge": "Беггер · Full Custom",
                "year_label": "Рік",
                "category_label": "Категорія",
                "category": "Беггер · Full Custom",
                "where_label": "Де",
                "where": "Збудовано у Харкові, Україна",
                "gallery": "Галерея",
                "gallery_title": "<em>Cocktail</em> — у деталях.",
            },
        },
        "gallery_alts": {
            "en": [
                "Cocktail custom bagger dashboard and Dakota digital gauges",
                "Cocktail custom bagger rear three-quarter view at Motobike-2013",
                "Cocktail custom bagger in motion with its rider",
                "Cocktail custom bagger front wheel and fairing at Motobike-2013",
                "Cocktail custom bagger full left-side view outdoors",
                "Cocktail custom bagger front three-quarter view outdoors",
                "Cocktail chromed Twin Cam 96 engine and airbrush detail",
                "Cocktail custom bagger with its rider outdoors",
                "Cocktail Sony Marine speaker installation detail",
                "Cocktail chromed Twin Cam 96 engine detail",
            ],
            "pt": [
                "Cocktail bagger custom, painel e mostradores digitais Dakota",
                "Cocktail bagger custom, vista traseira a três quartos no Motobike-2013",
                "Cocktail bagger custom em andamento com o piloto",
                "Cocktail bagger custom, roda dianteira e carenagem no Motobike-2013",
                "Cocktail bagger custom, vista lateral esquerda completa no exterior",
                "Cocktail bagger custom, vista dianteira a três quartos no exterior",
                "Cocktail, detalhe do motor Twin Cam 96 cromado e da aerografia",
                "Cocktail bagger custom com o piloto no exterior",
                "Cocktail, detalhe da instalação do altifalante Sony Marine",
                "Cocktail, detalhe do motor Twin Cam 96 cromado",
            ],
            "ru": [
                "Cocktail — панель бэггера и цифровые приборы Dakota",
                "Cocktail — бэггер сзади в три четверти на выставке Мотобайк-2013",
                "Cocktail — кастом-бэггер в движении с райдером",
                "Cocktail — переднее колесо и обтекатель на выставке Мотобайк-2013",
                "Cocktail — полный вид кастом-бэггера слева",
                "Cocktail — кастом-бэггер спереди в три четверти",
                "Cocktail — хромированный Twin Cam 96 и аэрография",
                "Cocktail — кастом-бэггер с райдером",
                "Cocktail — установка динамика Sony Marine",
                "Cocktail — детали хромированного Twin Cam 96",
            ],
            "uk": [
                "Cocktail — панель беггера та цифрові прилади Dakota",
                "Cocktail — беггер ззаду у три чверті на виставці Мотобайк-2013",
                "Cocktail — кастом-беггер у русі з райдером",
                "Cocktail — переднє колесо та обтічник на виставці Мотобайк-2013",
                "Cocktail — повний вигляд кастом-беггера зліва",
                "Cocktail — кастом-беггер спереду у три чверті",
                "Cocktail — хромований Twin Cam 96 та аерографія",
                "Cocktail — кастом-беггер із райдером",
                "Cocktail — встановлення динаміка Sony Marine",
                "Cocktail — деталі хромованого Twin Cam 96",
            ],
        },
    },
    "fetish": {
        "source": SITE_ROOT / "content/projects/fetish_4lang.md",
        "year": "2013",
        "published_iso": "2026-08-03T21:43:44+01:00",
        "modified_iso": "2026-08-04T07:03:42+01:00",
        "hero_base": "/photos/projects/fetish",
        "hero_source": "Fetish-Hero.jpg",
        "gallery_base": "/photos/projects/gallery/fetish/fetish",
        "gallery_sources": [
            "144806_IMG_0187.jpg",
            "145120_IMG_0194.jpg",
            "150354_IMG_0229.jpg",
            "150258_IMG_0222.jpg",
            "141211_IMG_0160.jpg",
            "150000_IMG_0209.jpg",
            "141156_IMG_0158.jpg",
            "145936_IMG_0208.jpg",
            "162628_IMG_9442.jpg",
            "151508_IMG_0242.jpg",
            "150405_IMG_0230.jpg",
            "145708_IMG_0203.jpg",
            "151902_IMG_0252.jpg",
        ],
        "jpeg_fallback": True,
        "integrations": {
            "custom": True,
            "harley_custom": True,
            "reciprocal_projects": ["cocktail"],
        },
        "ui": {
            "en": {
                "home": "Home",
                "projects": "Projects",
                "badge": "Chopper · Full Custom",
                "year_label": "Year",
                "category_label": "Category",
                "category": "Chopper · Full Custom",
                "where_label": "Where",
                "where": "Built in Kharkiv, Ukraine",
                "gallery": "Gallery",
                "gallery_title": "<em>Fetish</em> — in detail.",
            },
            "pt": {
                "home": "Início",
                "projects": "Projetos",
                "badge": "Chopper · Full Custom",
                "year_label": "Ano",
                "category_label": "Categoria",
                "category": "Chopper · Full Custom",
                "where_label": "Local",
                "where": "Construído em Kharkiv, Ucrânia",
                "gallery": "Galeria",
                "gallery_title": "<em>Fetish</em> — em detalhe.",
            },
            "ru": {
                "home": "Главная",
                "projects": "Проекты",
                "badge": "Чоппер · Full Custom",
                "year_label": "Год",
                "category_label": "Категория",
                "category": "Чоппер · Full Custom",
                "where_label": "Где",
                "where": "Построен в Харькове, Украина",
                "gallery": "Галерея",
                "gallery_title": "<em>Fetish</em> — в деталях.",
            },
            "uk": {
                "home": "Головна",
                "projects": "Проєкти",
                "badge": "Чопер · Full Custom",
                "year_label": "Рік",
                "category_label": "Категорія",
                "category": "Чопер · Full Custom",
                "where_label": "Де",
                "where": "Збудовано у Харкові, Україна",
                "gallery": "Галерея",
                "gallery_title": "<em>Fetish</em> — у деталях.",
            },
        },
        "gallery_alts": {
            "en": [
                "Fetish custom chopper front three-quarter view",
                "Fetish custom chopper with Harley-Davidson Rocker C engine",
                "Fetish fuel tank, skull airbrush and speedometer detail",
                "Fetish polished nitrous bottle, oil cooler and exhaust detail",
                "Fetish B-17 fork, front brake and skull wheel artwork detail",
                "Fetish 26-inch solid front wheel and skull airbrush artwork",
                "Fetish front brake disc and skull wheel artwork close-up",
                "Fetish Harley-Davidson engine and Bassani exhaust detail",
                "Fetish custom chopper low front-wheel view",
                "Fetish rear wheel, chain drive and two-part seat detail",
                "Fetish Bassani exhaust outlet close-up",
                "Fetish solid rear wheel and skull airbrush detail",
                "Fetish DNA sprotor, chain and rear wheel detail",
            ],
            "pt": [
                "Fetish chopper custom, vista dianteira a três quartos",
                "Fetish chopper custom com motor Harley-Davidson Rocker C",
                "Fetish, detalhe do depósito, aerografia de caveiras e velocímetro",
                "Fetish, detalhe da garrafa de nitro polida, radiador de óleo e escape",
                "Fetish, detalhe da forquilha B-17, travão dianteiro e arte de caveiras na roda",
                "Fetish, roda dianteira maciça de 26 polegadas e aerografia de caveiras",
                "Fetish, close-up do disco dianteiro e da arte de caveiras na roda",
                "Fetish, detalhe do motor Harley-Davidson e escape Bassani",
                "Fetish chopper custom, vista baixa a partir da roda dianteira",
                "Fetish, detalhe da roda traseira, transmissão por corrente e assento bipartido",
                "Fetish, close-up da saída do escape Bassani",
                "Fetish, roda traseira maciça e aerografia de caveiras",
                "Fetish, detalhe do sprotor DNA, corrente e roda traseira",
            ],
            "ru": [
                "Fetish — кастом-чоппер спереди в три четверти",
                "Fetish — кастом-чоппер с мотором Harley-Davidson Rocker C",
                "Fetish — бак, аэрография с черепами и спидометр",
                "Fetish — полированный баллон закиси, маслорадиатор и выхлоп",
                "Fetish — вилка B-17, передний тормоз и аэрография колеса",
                "Fetish — цельное 26-дюймовое переднее колесо с аэрографией",
                "Fetish — передний тормозной диск и рисунок с черепами крупным планом",
                "Fetish — мотор Harley-Davidson и выхлоп Bassani",
                "Fetish — кастом-чоппер с нижнего ракурса у переднего колеса",
                "Fetish — заднее колесо, цепной привод и двухсекционное сиденье",
                "Fetish — выпуск Bassani крупным планом",
                "Fetish — цельное заднее колесо и аэрография с черепами",
                "Fetish — sprotor DNA, цепь и заднее колесо",
            ],
            "uk": [
                "Fetish — кастом-чопер спереду у три чверті",
                "Fetish — кастом-чопер із мотором Harley-Davidson Rocker C",
                "Fetish — бак, аерографія з черепами та спідометр",
                "Fetish — полірований балон закису, маслорадіатор і вихлоп",
                "Fetish — вилка B-17, переднє гальмо й аерографія колеса",
                "Fetish — суцільне 26-дюймове переднє колесо з аерографією",
                "Fetish — передній гальмівний диск і малюнок із черепами великим планом",
                "Fetish — мотор Harley-Davidson і вихлоп Bassani",
                "Fetish — кастом-чопер із нижнього ракурсу біля переднього колеса",
                "Fetish — заднє колесо, ланцюговий привід і двосекційне сидіння",
                "Fetish — випуск Bassani великим планом",
                "Fetish — суцільне заднє колесо й аерографія з черепами",
                "Fetish — sprotor DNA, ланцюг і заднє колесо",
            ],
        },
    },
    "the-first": {
        "source": SITE_ROOT / "content/projects/the-first_4lang.md",
        "year": "2012",
        "published_iso": "2026-08-03T22:07:40+01:00",
        "modified_iso": "2026-08-03T22:07:40+01:00",
        "hero_base": "/photos/projects/the-first",
        "hero_source": "First_Hero.jpg",
        "gallery_base": "/photos/projects/gallery/the-first/the-first",
        "gallery_sources": [
            "152053_IMG_0363.jpg",
            "144334_IMG_4093.jpg",
            "152027_IMG_0359.jpg",
            "151624_IMG_0345.jpg",
            "142440_IMG_0075.jpg",
            "135619_IMG_0019.jpg",
            "142509_IMG_0079.jpg",
            "135722_IMG_0024.jpg",
            "135821_IMG_0028.jpg",
            "140054_IMG_0034.jpg",
            "152026_IMG_3957.jpg",
        ],
        "jpeg_fallback": True,
        "integrations": {
            "custom": True,
            "harley_custom": True,
            "reciprocal_projects": ["cocktail", "fetish"],
        },
        "ui": {
            "en": {
                "home": "Home",
                "projects": "Projects",
                "badge": "Power Cruiser · Full Custom",
                "year_label": "Year",
                "category_label": "Category",
                "category": "Power Cruiser · Full Custom",
                "where_label": "Where",
                "where": "Built in Kharkiv, Ukraine",
                "gallery": "Gallery",
                "gallery_title": "<em>The First</em> — in detail.",
            },
            "pt": {
                "home": "Início",
                "projects": "Projetos",
                "badge": "Power Cruiser · Full Custom",
                "year_label": "Ano",
                "category_label": "Categoria",
                "category": "Power Cruiser · Full Custom",
                "where_label": "Local",
                "where": "Construído em Kharkiv, Ucrânia",
                "gallery": "Galeria",
                "gallery_title": "<em>The First</em> — em detalhe.",
            },
            "ru": {
                "home": "Главная",
                "projects": "Проекты",
                "badge": "Пауэр-круизер · Full Custom",
                "year_label": "Год",
                "category_label": "Категория",
                "category": "Пауэр-круизер · Full Custom",
                "where_label": "Где",
                "where": "Построен в Харькове, Украина",
                "gallery": "Галерея",
                "gallery_title": "<em>The First</em> — в деталях.",
            },
            "uk": {
                "home": "Головна",
                "projects": "Проєкти",
                "badge": "Пауер-круїзер · Full Custom",
                "year_label": "Рік",
                "category_label": "Категорія",
                "category": "Пауер-круїзер · Full Custom",
                "where_label": "Де",
                "where": "Збудовано у Харкові, Україна",
                "gallery": "Галерея",
                "gallery_title": "<em>The First</em> — у деталях.",
            },
        },
        "gallery_alts": {
            "en": [
                "The First perforated handlebar grip and mirror detail",
                "The First Night Rod custom in motion with its rider",
                "The First handlebar clamp and instrument cluster detail",
                "The First custom fuel tank and Harley-Davidson lettering detail",
                "The First Night Rod custom rear three-quarter view",
                "The First front wheel, brake disc and fork detail",
                "The First Night Rod custom front three-quarter view by a glass facade",
                "The First rear wheel, brake disc and NLC swingarm detail",
                "The First V-Rod engine and matte-black exhaust detail",
                "The First Night Rod custom with its rider by a graffiti wall",
                "The First Night Rod custom during a rear-tyre burnout",
            ],
            "pt": [
                "The First, detalhe do punho perfurado e do espelho",
                "The First Night Rod custom em andamento com o piloto",
                "The First, detalhe da abraçadeira do guiador e da instrumentação",
                "The First, detalhe do depósito custom e da inscrição Harley-Davidson",
                "The First Night Rod custom, vista traseira a três quartos",
                "The First, detalhe da roda dianteira, disco de travão e forquilha",
                "The First Night Rod custom, vista dianteira a três quartos junto a uma fachada de vidro",
                "The First, detalhe da roda traseira, disco de travão e braço oscilante NLC",
                "The First, detalhe do motor V-Rod e do escape preto mate",
                "The First Night Rod custom com o piloto junto a uma parede de graffiti",
                "The First Night Rod custom durante um burnout do pneu traseiro",
            ],
            "ru": [
                "The First — перфорированная грипса и зеркало",
                "The First — кастом Night Rod в движении с райдером",
                "The First — крепление руля и приборная панель",
                "The First — кастомный бак и надпись Harley-Davidson",
                "The First — кастом Night Rod сзади в три четверти",
                "The First — переднее колесо, тормозной диск и вилка",
                "The First — кастом Night Rod спереди в три четверти у стеклянного фасада",
                "The First — заднее колесо, тормозной диск и маятник NLC",
                "The First — мотор V-Rod и матовый черный выхлоп",
                "The First — кастом Night Rod с райдером у стены с граффити",
                "The First — кастом Night Rod во время бернаута задней шины",
            ],
            "uk": [
                "The First — перфорована грипса та дзеркало",
                "The First — кастом Night Rod у русі з райдером",
                "The First — кріплення керма та панель приладів",
                "The First — кастомний бак і напис Harley-Davidson",
                "The First — кастом Night Rod ззаду у три чверті",
                "The First — переднє колесо, гальмівний диск і вилка",
                "The First — кастом Night Rod спереду у три чверті біля скляного фасаду",
                "The First — заднє колесо, гальмівний диск і маятник NLC",
                "The First — мотор V-Rod і матовий чорний вихлоп",
                "The First — кастом Night Rod із райдером біля стіни з графіті",
                "The First — кастом Night Rod під час бернауту задньої шини",
            ],
        },
    },
}

LEGACY_PROJECT_DATA_PATH = SITE_ROOT / "content/projects/legacy_projects_4lang.json"
LEGACY_PROJECT_ORDER = [
    "inspirium",
    "beckman",
    "unbreakable",
    "quanta-r",
    "burly",
    "sturmvogel",
    "geometric",
    "joker",
    "hellboy",
    "true-religion",
]

# The publication timestamp is the first Git commit that introduced the
# legacy project pages. Modified timestamps are the already-published sitemap
# content dates and remain language-specific where Git history differs.
LEGACY_PROJECT_DATES = {
    "inspirium": "2026-06-20T11:33:40+01:00",
    "beckman": "2026-08-01T19:17:10+01:00",
    "unbreakable": {
        "en": "2026-07-24T20:10:52+01:00",
        "ru": "2026-07-24T20:10:52+01:00",
        "uk": "2026-07-24T20:10:53+01:00",
        "pt": "2026-07-24T20:10:52+01:00",
    },
    "quanta-r": "2026-06-20T11:33:40+01:00",
    "burly": "2026-06-20T11:33:40+01:00",
    "sturmvogel": "2026-08-01T19:17:10+01:00",
    "geometric": "2026-06-20T11:33:40+01:00",
    "joker": "2026-06-20T11:33:40+01:00",
    "hellboy": "2026-08-01T19:17:10+01:00",
    "true-religion": "2026-06-20T11:33:40+01:00",
}

PROJECT_EXHIBITION_MEDIA = {
    "sturmvogel": {
        "base": "/photos/projects/exhibition/sturmvogel-exhibition",
        "widths": [800, 1600],
        "alts": {
            "en": "Sturmvogel — dieselpunk custom motorcycle in the Iron Custom Motors workshop exhibition next to the rider lounge, Cascais",
            "pt": "Sturmvogel — mota custom dieselpunk na exposição permanente da oficina Iron Custom Motors, em Cascais",
            "ru": "Sturmvogel — дизельпанк-кастом в постоянной экспозиции мастерской Iron Custom Motors в Cascais",
            "uk": "Sturmvogel — дизельпанк-кастом у постійній експозиції майстерні Iron Custom Motors у Cascais",
        },
    },
    "beckman": {
        "base": "/photos/projects/exhibition/beckman-exhibition",
        "widths": [800, 1600],
        "alts": {
            "en": "Beckman — 2016 AMD World Champion custom motorcycle in the Iron Custom Motors exhibition, Cascais",
            "pt": "Beckman — Campeão Mundial AMD de 2016 na exposição permanente da Iron Custom Motors, em Cascais",
            "ru": "Beckman — чемпион мира AMD 2016 года в постоянной экспозиции Iron Custom Motors в Cascais",
            "uk": "Beckman — чемпіон світу AMD 2016 року в постійній експозиції Iron Custom Motors у Cascais",
        },
    },
    "hellboy": {
        "base": "/photos/projects/exhibition/hellboy-exhibition",
        "widths": [800, 1600],
        "alts": {
            "en": "Hell Boy — Best Paint award-winning custom trike in the Iron Custom Motors exhibition, Cascais",
            "pt": "Hell Boy — triciclo custom vencedor do Best Paint na exposição permanente da Iron Custom Motors, em Cascais",
            "ru": "Hell Boy — кастом-трайк с наградой Best Paint в постоянной экспозиции Iron Custom Motors в Cascais",
            "uk": "Hell Boy — кастом-трайк із нагородою Best Paint у постійній експозиції Iron Custom Motors у Cascais",
        },
    },
}

_LEGACY_PROJECT_DATA = json.loads(
    LEGACY_PROJECT_DATA_PATH.read_text(encoding="utf-8")
)

PROJECT_CONFIGS = {
    slug: {
        "source": LEGACY_PROJECT_DATA_PATH,
        "source_format": "localized_html",
        "published_iso": "2026-05-05T21:37:36+02:00",
        "modified_iso": LEGACY_PROJECT_DATES[slug],
        "integrations": {"custom": True},
    }
    for slug in LEGACY_PROJECT_ORDER
}
for _slug, _media in PROJECT_EXHIBITION_MEDIA.items():
    PROJECT_CONFIGS[_slug]["exhibition_media"] = _media
PROJECT_CONFIGS.update(MARKDOWN_PROJECT_CONFIGS)
for _markdown_project in MARKDOWN_PROJECT_CONFIGS.values():
    _markdown_project["source_format"] = "markdown"
    _markdown_project.setdefault("modified_iso", _markdown_project["published_iso"])
for _project_config in PROJECT_CONFIGS.values():
    _project_config.setdefault("integrations", {})["custom"] = True
PROJECT_CONFIGS["fighter"]["visible_text_sha256"] = {
    "en": "3a105c2135bad232b2d6e01b8cdb83686f7c87b1a4fefcf3e69b74d899bc9395",
    "ru": "725b26e490480f786b929fc893853f41ad33b6642aca888af32231db2f543b53",
    "uk": "d5e061959c0d98b0e59681f50a53fdcbaf64aa2f621ef17b634ebbbf32df9d78",
    "pt": "3f8cc1b58b14eea3dd0155cb717dd5a61b473e3e451b2a4ff0103a66fef21f6c",
}
PROJECT_CONFIGS["cocktail"]["visible_text_sha256"] = {
    "en": "aeb808131a6434feb5cf470eae6860386a25f21438b054d649c55400bfab5788",
    "pt": "108c29f63c0312314c3edcf6f31986201d76a778914fb6d359b6343a16972850",
    "ru": "eace9e88de511dae1e34d3939139926db7fe23a2a9f450293a52ceb0d1ac5616",
    "uk": "a68f14e92058f1afc811e1106c753ba47be815432d090a08325688fb49f9e9e1",
}
PROJECT_CONFIGS["fetish"]["visible_text_sha256"] = {
    "en": "feeabfa58cf00f614015d82657016d988b3ad5a8ca34bc8ad92512e800afa76d",
    "pt": "b85999b3bf7e9cca0084b237612e0929aaabb97f3507fb45bb3e2912a91cfaff",
    "ru": "156db88c9c22f6fa9e0d43a5dfd01036625bd606bf1a5615333cf3f5433105f3",
    "uk": "60b81d6d0e66c3f85a96b1855052013d88f18c801c44ed09a4464297f5634b0c",
}
PROJECT_CONFIGS["the-first"]["visible_text_sha256"] = {
    "en": "6d8b844eb09df82698c3ee6c134350b69e0f892d7de51998e3bd6d549c3c764d",
    "pt": "0d6d46fedf310bb46f6970e18e362c1b5c71b4248e8725222ea477d9aa2655dd",
    "ru": "20217f22e09aa31c2664471c2b2178f1d3902951e02de507c12f3471f65701fa",
    "uk": "1dda45d82a1787335a5a53cf0bfc1ca918e32a2183b34859adb1f3b9a5e0a87f",
}

REDIRECT_CONFIGS = {
    "nezlamniy": {
        "target": "unbreakable",
        "labels": {
            "en": {
                "title": "Redirecting to Unbreakable | Iron Custom Motors",
                "message": "Redirecting to",
                "target_name": "Unbreakable",
            },
            "ru": {
                "title": "Переход на Unbreakable | Iron Custom Motors",
                "message": "Переход на",
                "target_name": "Unbreakable",
            },
            "uk": {
                "title": "Перехід на Unbreakable | Iron Custom Motors",
                "message": "Перехід на",
                "target_name": "Unbreakable",
            },
            "pt": {
                "title": "A redirecionar para Unbreakable | Iron Custom Motors",
                "message": "A redirecionar para",
                "target_name": "Unbreakable",
            },
        },
    },
    "quanta": {
        "target": "quanta-r",
        "labels": {
            "en": {
                "title": "Redirecting to Quanta R | Iron Custom Motors",
                "message": "Redirecting to",
                "target_name": "Quanta R",
            },
            "ru": {
                "title": "Переход на Quanta R | Iron Custom Motors",
                "message": "Переход на",
                "target_name": "Quanta R",
            },
            "uk": {
                "title": "Перехід на Quanta R | Iron Custom Motors",
                "message": "Перехід на",
                "target_name": "Quanta R",
            },
            "pt": {
                "title": "A redirecionar para Quanta R | Iron Custom Motors",
                "message": "A redirecionar para",
                "target_name": "Quanta R",
            },
        },
    },
}


def inline_markdown(value: str) -> str:
    """Render the limited inline Markdown used by project copy."""
    rendered = html.escape(value, quote=False)
    rendered = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: f'<a href="{html.escape(match.group(2), quote=True)}">{match.group(1)}</a>',
        rendered,
    )
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    return rendered


def parse_body_blocks(raw_body: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    paragraph: list[str] = []

    def flush_paragraph():
        if paragraph:
            blocks.append({"type": "p", "text": " ".join(paragraph)})
            paragraph.clear()

    for line in raw_body.splitlines():
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            blocks.append({"type": "h2", "text": stripped[3:]})
            continue
        paragraph.append(stripped)
    flush_paragraph()
    return blocks


def blocks_to_html(blocks: list[dict[str, str]]) -> str:
    output = []
    for block in blocks:
        if block["type"] == "h2":
            output.append(f"<h2>{html.escape(block['text'])}</h2>")
        else:
            output.append(f"<p>{inline_markdown(block['text'])}</p>")
    return "\n".join(output)


def parse_project_source(source_path: Path) -> dict[str, dict]:
    text = source_path.read_text(encoding="utf-8")
    matches = list(
        re.finditer(
            r"^## (ENGLISH|PORTUGUÊS \(pt-PT\)|РУССКИЙ|УКРАЇНСЬКА)\s*$",
            text,
            flags=re.MULTILINE,
        )
    )
    parsed: dict[str, dict] = {}

    for index, match in enumerate(matches):
        lang = LANGUAGE_SECTIONS[match.group(1)]
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end():end].strip()
        section = re.sub(r"\n---\s*$", "", section).strip()

        title_match = re.search(r"^\*\*SEO Title:\*\* (.+)$", section, flags=re.MULTILINE)
        meta_match = re.search(r"^\*\*Meta Description:\*\* (.+)$", section, flags=re.MULTILINE)
        slug_match = re.search(r"^\*\*Slug:\*\* (.+)$", section, flags=re.MULTILINE)
        h1_match = re.search(r"^# (.+)$", section, flags=re.MULTILINE)
        subtitle_match = re.search(r"^\*(.+)\*$", section, flags=re.MULTILINE)
        image_match = re.search(r"^\[IMAGE:.*\| ALT: (.+)\]$", section, flags=re.MULTILINE)

        required = [title_match, meta_match, slug_match, h1_match, subtitle_match, image_match]
        if any(item is None for item in required):
            raise ValueError(f"Incomplete project source section: {match.group(1)}")

        body_start = image_match.end()
        raw_body = section[body_start:].strip()
        blocks = parse_body_blocks(raw_body)
        if not blocks or blocks[-1]["type"] != "p":
            raise ValueError(f"Project closing paragraph missing: {match.group(1)}")
        closing = blocks.pop()

        parsed[lang] = {
            "title": title_match.group(1),
            "description": meta_match.group(1),
            "slug": slug_match.group(1),
            "h1": h1_match.group(1),
            "subtitle": subtitle_match.group(1),
            "hero_alt": image_match.group(1),
            "body_html": blocks_to_html(blocks),
            "closing_html": blocks_to_html([closing]),
        }

    if set(parsed) != {"en", "pt", "ru", "uk"}:
        raise ValueError(f"Expected four languages in {source_path}")
    return parsed


def load_project(slug: str) -> dict:
    config = PROJECT_CONFIGS[slug]
    if config["source_format"] == "localized_html":
        content = _LEGACY_PROJECT_DATA[slug]["languages"]
    else:
        content = parse_project_source(config["source"])
    return {**config, "slug": slug, "content": content}


def project_modified_iso(project: dict, lang: str) -> str:
    value = project["modified_iso"]
    if isinstance(value, dict):
        return value[lang]
    return value


PROJECT_PAGE_META = {
    slug: {
        lang: {
            "title": values["title"],
            "description": values["description"],
        }
        for lang, values in load_project(slug)["content"].items()
    }
    for slug in PROJECT_CONFIGS
}
