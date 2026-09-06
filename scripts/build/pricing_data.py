# -*- coding: utf-8 -*-
"""
Single source of truth for the Iron Custom Motors pricing page.
Edit a value here and re-run build_pricing.py — all 4 language pages regenerate.

Extracted verbatim from the approved 2025 PDFs uploaded by Pylyp:
  - ICM_price-list_2025_EN.pdf
  - ICM_tabela-precos_2025_PT.pdf
  - ICM_прайс-лист_2025_RU.pdf
  - ICM_прайс-лист_2025_UA.pdf
"""

LANGS = ["en", "ru", "uk", "pt"]

# ----- Page-level labels (shared across the page) -----
LABELS = {
    "en": {
        "page_title": "Motorcycle Service Prices 2026, Cascais | Iron Custom Motors",
        "page_description": "Motorcycle service prices 2026 in Cascais: maintenance from 150 €, Harley-Davidson 300 €, diagnostics 50–350 €, brake fluid 100 €. Written estimates.",
        "eyebrow": "Price list · 2026",
        "h1": "Motorcycle service prices 2026: maintenance, diagnostics and repair in Cascais",
        "lead": "Premium motorcycle service in Cascais. We don't compete on price — we compete on results. The engineering culture of world champions applied to your motorcycle: precise diagnostics, quality parts, transparent pricing and clear timelines.",
        "all_prices_include": "All prices include taxes and fees",
        "download_pdf": "Download PDF",
        "pdf_filename": "/pricing/files/ICM_price-list_2025_EN.pdf",
        "section_label": "Section",
        "book_service": "Book service",
        "whatsapp": "WhatsApp us",
        "from": "from",
        "per_hour": "/hour",
        "currency": "EUR",
        "cta_title": "Ready to book your motorcycle in?",
        "cta_text": "WhatsApp is the fastest way to reach us. Reply during working hours, usually within an hour.",
        "disclaimer_title": "About these prices",
        "disclaimer": "All prices are in euro and include applicable taxes and fees. Prices are indicative: the final amount is determined after diagnostics and depends on the make, model, technical condition of the motorcycle and the actual scope of work. The scheduled-service price includes all necessary consumables, except the air-filter replacement on Indian, BMW, Moto Guzzi, Ducati, Japan and KTM models. For other work, the cost of parts and consumables is not included unless stated otherwise. This price list is for information only and does not constitute a binding offer. Valid from 2025 until the next edition.",
    },
    "ru": {
        "page_title": "Цены на мотосервис 2026 · Кашкайш | Iron Custom Motors",
        "page_description": "Прайс-лист 2026 мотосервиса в Кашкайше: ТО от 150 €, Harley-Davidson 300 €, диагностика 50–350 €, тормозная жидкость 100 €. Письменная смета до работ.",
        "eyebrow": "Прайс-лист · 2026",
        "h1": "Цены на сервис мотоциклов 2026: ТО, диагностика и ремонт в Кашкайше",
        "lead": "Премиальный сервис мотоциклов в Кашкайше. Мы не конкурируем ценой — мы конкурируем результатом. Инженерная культура чемпионов мира применённая к вашему мотоциклу: точная диагностика, качественные запчасти, прозрачные цены и чёткие сроки.",
        "all_prices_include": "Все цены включают налоги и сборы",
        "download_pdf": "Скачать PDF",
        "pdf_filename": "/pricing/files/ICM_прайс-лист_2025_RU.pdf",
        "section_label": "Раздел",
        "book_service": "Записаться",
        "whatsapp": "Написать в WhatsApp",
        "from": "от",
        "per_hour": "/час",
        "currency": "EUR",
        "cta_title": "Готовы записать мотоцикл?",
        "cta_text": "WhatsApp — самый быстрый способ связаться. Ответ в рабочее время, обычно в течение часа.",
        "disclaimer_title": "О ценах",
        "disclaimer": "Все цены указаны в евро и включают применимые налоги и сборы. Цены являются ориентировочными: итоговая сумма определяется по результатам диагностики и зависит от марки, модели, технического состояния мотоцикла и фактического объёма работ. В стоимость планового ТО включены все необходимые расходные материалы, за исключением замены воздушного фильтра у моделей Indian, BMW, Moto Guzzi, Ducati, Japan и KTM. Для прочих работ стоимость запчастей и расходных материалов не включена, если не указано иное. Прайс-лист носит информационный характер и не является публичной офертой. Действителен с 2025 года до следующей редакции.",
    },
    "uk": {
        "page_title": "Ціни на мотосервіс 2026 · Кашкайш | Iron Custom Motors",
        "page_description": "Прайс 2026 мотосервісу Iron Custom Motors у Кашкайші: ТО від 150 €, Harley-Davidson 300 €, діагностика 50–350 €, гальмівна рідина 100 €. Кошторис письмово.",
        "eyebrow": "Прайс · 2026",
        "h1": "Ціни на сервіс мотоциклів 2026: ТО, діагностика та ремонт у Кашкайші",
        "lead": "Преміальний сервіс мотоциклів у Кашкайші. Ми не конкуруємо ціною — ми конкуруємо результатом. Інженерна культура чемпіонів світу застосована до вашого мотоцикла: точна діагностика, якісні запчастини, прозорі ціни та чіткі терміни.",
        "all_prices_include": "Усі ціни включають податки та збори",
        "download_pdf": "Завантажити PDF",
        "pdf_filename": "/pricing/files/ICM_прайс-лист_2025_UA.pdf",
        "section_label": "Розділ",
        "book_service": "Записатися",
        "whatsapp": "Написати в WhatsApp",
        "from": "від",
        "per_hour": "/год",
        "currency": "EUR",
        "cta_title": "Готові записати мотоцикл?",
        "cta_text": "WhatsApp — найшвидший спосіб зв'язатися. Відповідь у робочий час, зазвичай протягом години.",
        "disclaimer_title": "Про ціни",
        "disclaimer": "Усі ціни вказано в євро і включають застосовні податки та збори. Ціни є орієнтовними: підсумкова сума визначається за результатами діагностики й залежить від марки, моделі, технічного стану мотоцикла та фактичного обсягу робіт. До вартості планового ТО входять усі необхідні витратні матеріали, окрім заміни повітряного фільтра у моделей Indian, BMW, Moto Guzzi, Ducati, Japan і KTM. Для інших робіт вартість запчастин і витратних матеріалів не входить, якщо не зазначено інше. Прайс-лист має інформаційний характер і не є публічною офертою. Чинний з 2025 року до наступної редакції.",
    },
    "pt": {
        "page_title": "Preços 2026 · Oficina de Motas Cascais | Iron Custom Motors",
        "page_description": "Preços 2026 da oficina de motas em Cascais: revisão desde 150 €, Harley-Davidson 300 €, diagnóstico 50–350 €, líquido de travões 100 €. Orçamento escrito.",
        "eyebrow": "Tabela de preços · 2026",
        "h1": "Tabela de preços 2026: revisão, diagnóstico e reparação de motas em Cascais",
        "lead": "Serviço premium de motos em Cascais. Não competimos no preço — competimos no resultado. A cultura de engenharia dos campeões mundiais aplicada à sua moto: diagnóstico preciso, peças de qualidade, preços transparentes e prazos claros.",
        "all_prices_include": "Todos os preços incluem impostos e taxas",
        "download_pdf": "Descarregar PDF",
        "pdf_filename": "/pricing/files/ICM_tabela-precos_2025_PT.pdf",
        "section_label": "Secção",
        "book_service": "Marcar serviço",
        "whatsapp": "WhatsApp",
        "from": "desde",
        "per_hour": "/hora",
        "currency": "EUR",
        "cta_title": "Pronto para marcar o serviço da sua moto?",
        "cta_text": "WhatsApp é a forma mais rápida de nos contactar. Resposta em horário de trabalho, normalmente dentro de uma hora.",
        "disclaimer_title": "Sobre estes preços",
        "disclaimer": "Todos os preços estão em euros e incluem os impostos e taxas aplicáveis. Os preços são indicativos: o valor final é determinado após o diagnóstico e depende da marca, modelo, estado técnico da moto e do âmbito real do trabalho. O preço da manutenção programada inclui todos os consumíveis necessários, exceto a substituição do filtro de ar nos modelos Indian, BMW, Moto Guzzi, Ducati, Japan e KTM. Para outros trabalhos, o custo das peças e consumíveis não está incluído salvo indicação em contrário. Esta tabela de preços é meramente informativa e não constitui uma oferta vinculativa. Válida desde 2025 até à próxima edição.",
    },
}


# ----- Section 01: Diagnostics -----
SEC_01 = {
    "num": "01",
    "anchor": "diagnostics",
    "title": {
        "en": "Diagnostics", "ru": "Диагностика",
        "uk": "Діагностика", "pt": "Diagnóstico",
    },
    "h2": {
        "en": "Diagnostics of your motorcycle",
        "ru": "Диагностика мотоцикла",
        "uk": "Діагностика мотоцикла",
        "pt": "Diagnóstico da moto",
    },
    "intro": {
        "en": "An objective assessment of technical condition — before a purchase, before the season or when locating a fault. You get an accurate picture of the motorcycle's condition and a prioritised work plan.",
        "ru": "Объективная оценка технического состояния — до покупки, перед сезоном или при поиске неисправности. Вы получаете точную картину состояния мотоцикла и приоритизированный план работ.",
        "uk": "Об'єктивна оцінка технічного стану — перед купівлею, перед сезоном або під час пошуку несправності. Ви отримуєте точну картину стану мотоцикла та пріоритизований план робіт.",
        "pt": "Uma avaliação objetiva do estado técnico — antes de uma compra, antes da época ou na localização de uma avaria. Recebe uma imagem precisa do estado da moto e um plano de trabalho priorizado.",
    },
    "cards": [
        {
            "name": {
                "en": "Pre-purchase inspection",
                "ru": "Диагностика перед покупкой",
                "uk": "Діагностика перед купівлею",
                "pt": "Inspeção pré-compra",
            },
            "desc": {
                "en": "Full technical inspection of the motorcycle before the deal",
                "ru": "Полная техническая проверка мотоцикла перед сделкой",
                "uk": "Повна технічна перевірка мотоцикла перед угодою",
                "pt": "Inspeção técnica completa da moto antes do negócio",
            },
            "price": "150 EUR",
            "tags": {
                "en": ["Fixed price", "10-point inspection", "Written report"],
                "ru": ["Фиксированная стоимость", "Осмотр по 10 пунктам", "Письменное заключение"],
                "uk": ["Фіксована вартість", "Огляд за 10 пунктами", "Письмовий висновок"],
                "pt": ["Preço fixo", "Inspeção de 10 pontos", "Relatório escrito"],
            },
        },
        {
            "name": {
                "en": "Fault diagnostics",
                "ru": "Диагностика неисправностей",
                "uk": "Діагностика несправностей",
                "pt": "Diagnóstico de avarias",
            },
            "desc": {
                "en": "Locating a specific fault — electrics, engine, running gear",
                "ru": "Поиск и локализация конкретной неисправности — электрика, двигатель, ходовая",
                "uk": "Пошук і локалізація конкретної несправності — електрика, двигун, ходова",
                "pt": "Localização de uma avaria específica — elétrica, motor, chassis",
            },
            "price": "50–350 EUR",
            "tags": {
                "en": ["Depends on case complexity", "Electrics, engine, running gear", "We find the cause, not the symptom"],
                "ru": ["Зависит от сложности случая", "Электрика, двигатель, ходовая", "Ищем причину, а не симптом"],
                "uk": ["Залежить від складності випадку", "Електрика, двигун, ходова", "Шукаємо причину, а не симптом"],
                "pt": ["Depende da complexidade", "Elétrica, motor, chassis", "Procuramos a causa, não o sintoma"],
            },
        },
        {
            "name": {
                "en": "Pre-season check",
                "ru": "Диагностика перед сезоном",
                "uk": "Діагностика перед сезоном",
                "pt": "Verificação pré-época",
            },
            "desc": {
                "en": "Preparation for use after storage, clearance for long trips",
                "ru": "Подготовка к эксплуатации после простоя, допуск к дальней поездке",
                "uk": "Підготовка до експлуатації після простою, допуск до дальньої поїздки",
                "pt": "Preparação para uso após arrumação, aptidão para viagens longas",
            },
            "price_from": True,
            "price": "100 EUR",
            "tags": {
                "en": ["Preparation for use", "Clearance for long trips", "See Section 06"],
                "ru": ["Подготовка к эксплуатации", "Допуск к дальней поездке", "Подробнее — раздел 06"],
                "uk": ["Підготовка до експлуатації", "Допуск до дальньої поїздки", "Докладніше — розділ 06"],
                "pt": ["Preparação para uso", "Aptidão para viagens longas", "Mais na Secção 06"],
            },
        },
    ],
    "note": {
        "en": "Diagnostics is an investment, not an expense. An hour of an engineer's work pinpoints the cause of a fault and assesses the remaining life of key components — before they require major repair. You receive a structured list of recommendations by priority: critical work, advisable work and items that can wait until the next service.",
        "ru": "Диагностика — это инвестиция, а не расход. Час работы инженера позволяет точно локализовать причину неисправности и оценить ресурс ключевых узлов — до того, как они потребуют серьёзного ремонта. По итогам вы получаете структурированный список рекомендаций с приоритетами: критические работы, желательные и те, что можно отложить до следующего сервиса.",
        "uk": "Діагностика — це інвестиція, а не витрата. Година роботи інженера дозволяє точно локалізувати причину несправності й оцінити ресурс ключових вузлів — до того, як вони потребуватимуть серйозного ремонту. За підсумками ви отримуєте структурований перелік рекомендацій із пріоритетами: критичні роботи, бажані та ті, які можна відкласти до наступного сервісу.",
        "pt": "O diagnóstico é um investimento, não uma despesa. Uma hora de trabalho de um engenheiro identifica a causa de uma avaria e avalia a vida útil restante dos componentes principais — antes que exijam uma reparação grande. Recebe uma lista estruturada de recomendações por prioridade: trabalhos críticos, aconselháveis e os que podem esperar pela próxima revisão.",
    },
}


# ----- Section 02: Scheduled service -----
SEC_02 = {
    "num": "02",
    "anchor": "scheduled-service",
    "title": {
        "en": "Scheduled maintenance",
        "ru": "Плановое ТО",
        "uk": "Планове ТО",
        "pt": "Manutenção programada",
    },
    "h2": {
        "en": "Scheduled maintenance",
        "ru": "Плановое обслуживание",
        "uk": "Планове обслуговування",
        "pt": "Manutenção programada",
    },
    "intro": {
        "en": "Scheduled servicing to manufacturer standards. Four main brand groups — the price depends on the model and the service interval.",
        "ru": "Регламентное ТО по стандартам производителя. Четыре основные группы марок — стоимость зависит от модели и регламентного интервала.",
        "uk": "Регламентне ТО за стандартами виробника. Чотири основні групи марок — вартість залежить від моделі та регламентного інтервалу.",
        "pt": "Manutenção programada segundo as normas do fabricante. Quatro grupos principais de marcas — o preço depende do modelo e do intervalo de revisão.",
    },
    "consumables_label": {
        "en": "Consumables included",
        "ru": "Расходники включены",
        "uk": "Витратні матеріали включено",
        "pt": "Consumíveis incluídos",
    },
    "consumables_text": {
        "en": "The scheduled-service price includes all necessary consumables and applicable taxes — oils, oil filters and related consumables: you pay a single amount for fully completed servicing. The only exception is the air-filter replacement on Indian, BMW, Moto Guzzi, Ducati, Japan and KTM models: the filter itself is charged separately (marked in the lists below).",
        "ru": "В стоимость планового ТО входят все необходимые расходные материалы и применимые налоги — масла, масляные фильтры и сопутствующие расходники: вы платите одну сумму за полностью выполненное обслуживание. Единственное исключение — замена воздушного фильтра у моделей Indian, BMW, Moto Guzzi, Ducati, Japan и KTM: сам фильтр оплачивается отдельно (отмечено в списках ниже).",
        "uk": "У вартість планового ТО входять усі необхідні витратні матеріали та застосовні податки — оливи, масляні фільтри та супутні витратні матеріали: ви сплачуєте одну суму за повністю виконане обслуговування. Єдиний виняток — заміна повітряного фільтра у моделей Indian, BMW, Moto Guzzi, Ducati, Japan і KTM: сам фільтр оплачується окремо (позначено в переліках нижче).",
        "pt": "O preço da manutenção programada inclui todos os consumíveis necessários e os impostos aplicáveis — óleos, filtros de óleo e consumíveis associados: paga um valor único pelo serviço totalmente concluído. A única exceção é a substituição do filtro de ar nos modelos Indian, BMW, Moto Guzzi, Ducati, Japan e KTM: o filtro é cobrado à parte (assinalado nas listas abaixo).",
    },
    "groups": [
        {
            "name": "HARLEY-DAVIDSON",
            "price": "300 EUR",
            "checklist": {
                "en": ["Visual inspection","Engine check","Brake system","Suspension","Electrical system","Lighting","Tyres","Wheel bearings","Belt tension","General re-torque","Engine oil change","Gearbox oil change","Clutch oil change","Oil filter change","Air filter clean & oil","Battery check","List of recommendations"],
                "ru": ["Внешний осмотр","Проверка двигателя","Тормозная система","Подвеска","Электрооборудование","Светооптика","Покрышки","Подшипники колёс","Натяжка ремня","Обтяжка мотоцикла","Замена масла в двигателе","Замена масла в КПП","Замена масла в сцеплении","Замена масляного фильтра","Чистка и пропитка воздушного фильтра","Проверка АКБ","Список рекомендаций"],
                "uk": ["Зовнішній огляд","Перевірка двигуна","Гальмівна система","Підвіска","Електрообладнання","Світлооптика","Шини","Підшипники коліс","Натяг ременя","Контроль затягування","Заміна оливи в двигуні","Заміна оливи в КПП","Заміна оливи в зчепленні","Заміна масляного фільтра","Чищення та просочення повітряного фільтра","Перевірка АКБ","Перелік рекомендацій"],
                "pt": ["Inspeção visual","Verificação do motor","Sistema de travagem","Suspensão","Sistema elétrico","Iluminação","Pneus","Rolamentos de roda","Tensão da correia","Reaperto geral","Mudança de óleo do motor","Mudança de óleo da caixa","Mudança de óleo da embraiagem","Mudança do filtro de óleo","Limpeza e óleo do filtro de ar","Verificação da bateria","Lista de recomendações"],
            },
        },
        {
            "name": "INDIAN",
            "price": "200 EUR",
            "checklist": {
                "en": ["Visual inspection","Engine check","Brake system","Suspension","Electrical system","Lighting","Tyres","Wheel bearings","Belt tension","General re-torque","Engine oil change","Oil filter change","Air filter replacement (filter not included)","Battery check","List of recommendations"],
                "ru": ["Внешний осмотр","Проверка двигателя","Тормозная система","Подвеска","Электрооборудование","Светооптика","Покрышки","Подшипники колёс","Натяжка ремня","Обтяжка мотоцикла","Замена масла в двигателе","Замена масляного фильтра","Замена воздушного фильтра (фильтр не включён)","Проверка АКБ","Список рекомендаций"],
                "uk": ["Зовнішній огляд","Перевірка двигуна","Гальмівна система","Підвіска","Електрообладнання","Світлооптика","Шини","Підшипники коліс","Натяг ременя","Контроль затягування","Заміна оливи в двигуні","Заміна масляного фільтра","Заміна повітряного фільтра (фільтр не входить)","Перевірка АКБ","Перелік рекомендацій"],
                "pt": ["Inspeção visual","Verificação do motor","Sistema de travagem","Suspensão","Sistema elétrico","Iluminação","Pneus","Rolamentos de roda","Tensão da correia","Reaperto geral","Mudança de óleo do motor","Mudança do filtro de óleo","Substituição do filtro de ar (filtro não incluído)","Verificação da bateria","Lista de recomendações"],
            },
        },
        {
            "name": "BMW · MOTO GUZZI",
            "price_from": True,
            "price": "180 EUR",
            "checklist": {
                "en": ["Visual inspection","Engine check","Brake system","Suspension","Electrical system","Lighting","Tyres","Wheel bearings","Final-drive check","General re-torque","Engine oil change","Gearbox oil change","Final-drive oil change","Oil filter change","Air filter replacement (filter not included)","Battery check","List of recommendations"],
                "ru": ["Внешний осмотр","Проверка двигателя","Тормозная система","Подвеска","Электрооборудование","Светооптика","Покрышки","Подшипники колёс","Диагностика кардана","Обтяжка мотоцикла","Замена масла в двигателе","Замена масла в КПП","Замена масла в редукторе","Замена масляного фильтра","Замена воздушного фильтра (фильтр не включён)","Проверка АКБ","Список рекомендаций"],
                "uk": ["Зовнішній огляд","Перевірка двигуна","Гальмівна система","Підвіска","Електрообладнання","Світлооптика","Шини","Підшипники коліс","Діагностика кардана","Контроль затягування","Заміна оливи в двигуні","Заміна оливи в КПП","Заміна оливи в редукторі","Заміна масляного фільтра","Заміна повітряного фільтра (фільтр не входить)","Перевірка АКБ","Перелік рекомендацій"],
                "pt": ["Inspeção visual","Verificação do motor","Sistema de travagem","Suspensão","Sistema elétrico","Iluminação","Pneus","Rolamentos de roda","Verificação do cardã","Reaperto geral","Mudança de óleo do motor","Mudança de óleo da caixa","Mudança de óleo do diferencial","Mudança do filtro de óleo","Substituição do filtro de ar (filtro não incluído)","Verificação da bateria","Lista de recomendações"],
            },
        },
        {
            "name": "DUCATI · JAPAN · KTM GROUP",
            "price_from": True,
            "price": "150 EUR",
            "checklist": {
                "en": ["Visual inspection","Engine check","Brake system","Suspension","Electrical system","Lighting","Tyres","Wheel bearings","Chain tension","General re-torque","Engine oil change","Oil filter change","Air filter replacement (filter not included)","Battery check","List of recommendations"],
                "ru": ["Внешний осмотр","Проверка двигателя","Тормозная система","Подвеска","Электрооборудование","Светооптика","Покрышки","Подшипники колёс","Натяжение цепи","Обтяжка мотоцикла","Замена масла в двигателе","Замена масляного фильтра","Замена воздушного фильтра (фильтр не включён)","Проверка АКБ","Список рекомендаций"],
                "uk": ["Зовнішній огляд","Перевірка двигуна","Гальмівна система","Підвіска","Електрообладнання","Світлооптика","Шини","Підшипники коліс","Натяг ланцюга","Контроль затягування","Заміна оливи в двигуні","Заміна масляного фільтра","Заміна повітряного фільтра (фільтр не входить)","Перевірка АКБ","Перелік рекомендацій"],
                "pt": ["Inspeção visual","Verificação do motor","Sistema de travagem","Suspensão","Sistema elétrico","Iluminação","Pneus","Rolamentos de roda","Tensão da corrente","Reaperto geral","Mudança de óleo do motor","Mudança do filtro de óleo","Substituição do filtro de ar (filtro não incluído)","Verificação da bateria","Lista de recomendações"],
            },
        },
    ],
    "note": {
        "en": "The \"from\" price for BMW, Moto Guzzi, Ducati, Japanese brands and KTM-group machines is a starting price — the exact amount depends on the model and is confirmed in a written estimate before work begins. Valve adjustment and carburettor service are not part of scheduled maintenance — see Sections 03 and 04.",
        "ru": "Цена «от» для групп BMW, Moto Guzzi, Ducati, японских марок и техники KTM означает стартовую стоимость — точная сумма зависит от модели и подтверждается в письменной смете до начала работ. Регулировка клапанов и сервис карбюраторов в регламентное ТО не входят — см. разделы 03 и 04.",
        "uk": "Ціна «від» для груп BMW, Moto Guzzi, Ducati, японських марок і техніки KTM означає стартову вартість — точна сума залежить від моделі та підтверджується у письмовому кошторисі до початку робіт. Регулювання клапанів та сервіс карбюраторів до планового ТО не входять — див. розділи 03 і 04.",
        "pt": "O preço \"desde\" para BMW, Moto Guzzi, Ducati, marcas japonesas e grupo KTM é um preço inicial — o valor exato depende do modelo e é confirmado num orçamento escrito antes do início dos trabalhos. A regulação de válvulas e o serviço de carburadores não fazem parte da manutenção programada — ver Secções 03 e 04.",
    },
}


# ----- Section 03: Brakes, consumables, carbs -----
SEC_03 = {
    "num": "03",
    "anchor": "brakes-carbs",
    "title": {
        "en": "Brakes · Carbs", "ru": "Тормоза · Карбюраторы",
        "uk": "Гальма · Карбюратори", "pt": "Travões · Carburadores",
    },
    "h2": {
        "en": "Brakes, consumables and carburettors",
        "ru": "Тормоза, расходники и карбюраторы",
        "uk": "Гальма, витратні матеріали та карбюратори",
        "pt": "Travões, consumíveis e carburadores",
    },
    "intro": {
        "en": "Replacement of fluids, regular consumable operations and fine work on the fuel system. Prices are for labour; parts and fluids are not included unless stated otherwise.",
        "ru": "Замена технических жидкостей, регулярные расходные операции и тонкие работы по системе питания. Цены — за работу; стоимость запчастей и жидкостей не входит, если не указано иное.",
        "uk": "Заміна технічних рідин, регулярні витратні операції та точні роботи з системою живлення. Ціни — за роботу; вартість запчастин і рідин не входить, якщо не зазначено інше.",
        "pt": "Substituição de fluidos, operações regulares de consumíveis e trabalhos de precisão no sistema de alimentação. Preços de mão de obra; peças e fluidos não incluídos salvo indicação.",
    },
    "subgroups": [
        {
            "label": {"en":"Brake system","ru":"Тормозная система","uk":"Гальмівна система","pt":"Sistema de travagem"},
            "items": [
                {"name": {"en":"Brake fluid · non-ABS","ru":"Тормозная жидкость · non-ABS","uk":"Гальмівна рідина · non-ABS","pt":"Líquido de travões · não-ABS"}, "price": "100 EUR"},
                {"name": {"en":"Brake fluid · ABS","ru":"Тормозная жидкость · ABS","uk":"Гальмівна рідина · ABS","pt":"Líquido de travões · ABS"}, "price": "150 EUR", "price_from": True},
            ],
        },
        {
            "label": {"en":"Regular consumable work","ru":"Регулярные расходные работы","uk":"Регулярні витратні роботи","pt":"Trabalhos regulares de consumíveis"},
            "items": [
                {
                    "name": {"en":"Air filter clean & oil","ru":"Чистка и смазка воздушного фильтра","uk":"Чищення та змащення повітряного фільтра","pt":"Limpeza e óleo do filtro de ar"},
                    "desc": {"en":"Servicing of free-flow / OEM filter","ru":"Обслуживание фильтра нулевого сопротивления / штатного","uk":"Обслуговування фільтра нульового опору / штатного","pt":"Manutenção de filtro free-flow / OEM"},
                    "price": "45 EUR",
                },
                {
                    "name": {"en":"Air filter replacement","ru":"Замена воздушного фильтра","uk":"Заміна повітряного фільтра","pt":"Substituição do filtro de ar"},
                    "desc": {"en":"Price depends on model and filter type","ru":"Стоимость зависит от модели и типа фильтра","uk":"Вартість залежить від моделі та типу фільтра","pt":"Preço depende do modelo e tipo de filtro"},
                    "price": "20 EUR", "price_from": True,
                },
                {
                    "name": {"en":"Fork seal & dust-seal replacement","ru":"Замена сальников-пыльников вилки","uk":"Заміна сальників-пильовиків вилки","pt":"Substituição de retentores da forquilha"},
                    "desc": {"en":"Includes fork strip-down and oil change","ru":"С разборкой передней вилки и заменой масла","uk":"З розбиранням передньої вилки та заміною оливи","pt":"Inclui desmontagem da forquilha e mudança de óleo"},
                    "price": "150 EUR", "price_from": True,
                },
                {
                    "name": {"en":"Battery replacement","ru":"Замена АКБ","uk":"Заміна АКБ","pt":"Substituição da bateria"},
                    "desc": {"en":"Removal, fitting, charging-circuit check","ru":"Демонтаж, установка, проверка цепи заряда","uk":"Демонтаж, встановлення, перевірка кола заряду","pt":"Remoção, montagem, verificação da carga"},
                    "price": "20 EUR", "price_from": True,
                },
            ],
        },
        {
            "label": {"en":"Carburettor service","ru":"Сервис карбюраторов","uk":"Сервіс карбюраторів","pt":"Serviço de carburadores"},
            "items": [
                {"name": {"en":"1 carburettor","ru":"1 карбюратор","uk":"1 карбюратор","pt":"1 carburador"}, "price": "75 EUR", "price_from": True},
                {"name": {"en":"2 carburettors","ru":"2 карбюратора","uk":"2 карбюратори","pt":"2 carburadores"}, "price": "150 EUR", "price_from": True},
                {"name": {"en":"4 carburettors","ru":"4 карбюратора","uk":"4 карбюратори","pt":"4 carburadores"}, "price": "200 EUR", "price_from": True},
            ],
        },
    ],
}


# ----- Section 04: Valves, wheels, chain (uses tables) -----
SEC_04 = {
    "num": "04",
    "anchor": "valves-wheels",
    "title": {
        "en": "Valves · Wheels", "ru": "Клапаны · Колёса",
        "uk": "Клапани · Колеса", "pt": "Válvulas · Rodas",
    },
    "h2": {
        "en": "Valves, wheels and chain",
        "ru": "Клапаны, колёса и цепь",
        "uk": "Клапани, колеса та ланцюг",
        "pt": "Válvulas, rodas e corrente",
    },
    "intro": {
        "en": "Valve-train adjustment, tyre fitting by motorcycle class and complete chain-drive care.",
        "ru": "Регулировка газораспределения, шиномонтаж по классам мотоциклов и комплексный уход за цепным приводом.",
        "uk": "Регулювання газорозподілу, шиномонтаж за класами мотоциклів і комплексний догляд за ланцюговим приводом.",
        "pt": "Regulação da distribuição, montagem de pneus por classe de moto e cuidado completo da transmissão por corrente.",
    },
    "valve_table": {
        "title": {"en":"Valve adjustment","ru":"Регулировка клапанов","uk":"Регулювання клапанів","pt":"Regulação de válvulas"},
        "cols": {
            "en": ["Engine type", "Clearance check only", "Check + adjustment"],
            "ru": ["Тип двигателя", "Только проверка зазоров", "Проверка + регулировка"],
            "uk": ["Тип двигуна", "Лише перевірка зазорів", "Перевірка + регулювання"],
            "pt": ["Tipo de motor", "Só verificação de folgas", "Verificação + regulação"],
        },
        "rows": [
            ["BMW Boxer", "150", "300"],
            ["Japanese Inline 2 / 4", "250 / 400", "300 / 650"],
            ["KTM / Japanese", "350–450", "550–750"],
            ["Moto Guzzi / Vintage", "100", "150"],
            ["Ducati Desmo", "550", "1200"],
        ],
        "note": {
            "en": "Prices in euro. Ducati Desmo — the desmodromic mechanism requires separate expertise, so Desmo service is significantly more expensive than a standard adjustment.",
            "ru": "Цены в евро. Ducati Desmo — десмодромный механизм требует отдельной квалификации, поэтому Desmo service существенно дороже обычной регулировки.",
            "uk": "Ціни в євро. Ducati Desmo — десмодромний механізм потребує окремої кваліфікації, тому Desmo service істотно дорожчий за звичайне регулювання.",
            "pt": "Preços em euro. Ducati Desmo — o mecanismo desmodrómico exige qualificação específica, pelo que o serviço Desmo é bastante mais caro do que uma regulação normal.",
        },
    },
    "tyre_table": {
        "title": {"en":"Tyre fitting · labour price","ru":"Шиномонтаж · стоимость работы","uk":"Шиномонтаж · вартість роботи","pt":"Montagem de pneus · mão de obra"},
        "cols": {
            "en": ["Operation", "Street / Sport / Naked", "Chopper / Touring", "Custom"],
            "ru": ["Операция", "Street / Sport / Naked", "Chopper / Touring", "Custom"],
            "uk": ["Операція", "Street / Sport / Naked", "Chopper / Touring", "Custom"],
            "pt": ["Operação", "Street / Sport / Naked", "Chopper / Touring", "Custom"],
        },
        "rows": [
            [{"en":"Front wheel","ru":"Переднее колесо","uk":"Переднє колесо","pt":"Roda dianteira"}, "40+", "80+", "100+"],
            [{"en":"Rear wheel","ru":"Заднее колесо","uk":"Заднє колесо","pt":"Roda traseira"}, "60+", "100+", "100+"],
            [{"en":"Front + rear set","ru":"Комплект перёд + зад","uk":"Комплект перед + зад","pt":"Conjunto frente + trás"}, "90+", "150+", "200+"],
            [{"en":"Puncture repair","ru":"Ремонт проколов","uk":"Ремонт проколів","pt":"Reparação de furos"}, "40+", "40+", "40+"],
        ],
        "note": {"en":"All prices in euro.","ru":"Все цены в евро.","uk":"Усі ціни в євро.","pt":"Todos os preços em euro."},
    },
    "additional_services": [
        {
            "name": {
                "en": "Tubeless conversion of spoked wheels",
                "ru": "Конверсия спицованного колеса в бескамерное",
                "uk": "Конверсія спицьованого колеса в безкамерне",
                "pt": "Conversão tubeless de rodas de raios",
            },
            "price": {
                "en": "€100 per wheel",
                "ru": "€100 за колесо",
                "uk": "€100 за колесо",
                "pt": "100 € por roda",
            },
            "schema_price": "100",
        },
    ],
    "chain": {
        "name": {"en":"Chain clean, lube & adjust","ru":"Чистка, смазка и регулировка цепи","uk":"Чищення, змащення та регулювання ланцюга","pt":"Limpeza, lubrificação e regulação da corrente"},
        "desc": {"en":"Complete chain-drive care — extends chain and sprocket life","ru":"Комплексный уход за цепным приводом — продлевает ресурс цепи и звёзд","uk":"Комплексний догляд за ланцюговим приводом — подовжує ресурс ланцюга та зірок","pt":"Cuidado completo da transmissão — prolonga a vida da corrente e cremalheiras"},
        "price": "40 EUR",
        "note": {
            "en": "The chain rewards regularity. Timely care noticeably extends the life of the chain and sprockets — one of the cheapest preventive jobs in the price list. A neglected chain-and-sprocket set costs many times more.",
            "ru": "Цепь любит регулярность. Своевременный уход заметно продлевает ресурс цепи и звёзд — одна из самых недорогих профилактических работ в прайсе. Запущенный комплект цепь–звёзды обходится в разы дороже.",
            "uk": "Ланцюг любить регулярність. Своєчасний догляд помітно подовжує ресурс ланцюга та зірок — це одна з найбільш недорогих профілактичних робіт у прайсі. Занедбаний комплект ланцюг–зірки коштує в рази дорожче.",
            "pt": "A corrente gosta de regularidade. O cuidado atempado prolonga bastante a vida da corrente e cremalheiras — um dos trabalhos preventivos mais baratos da tabela. Um conjunto descuidado custa muito mais.",
        },
    },
}


# ----- Section 05: Accessories & tuning -----
SEC_05 = {
    "num": "05",
    "anchor": "accessories-tuning",
    "title": {
        "en": "Accessories & Tuning",
        "ru": "Допоборудование и тюнинг",
        "uk": "Дообладнання та тюнінг",
        "pt": "Acessórios e afinação",
    },
    "h2": {
        "en": "Accessories and tuning",
        "ru": "Допоборудование и тюнинг",
        "uk": "Дообладнання та тюнінг",
        "pt": "Acessórios e afinação",
    },
    "intro": {
        "en": "Fitting of accessories, electrical equipment and tuning components. Prices are for fitting labour; the components themselves are quoted separately. A \"+\" mark means \"from the stated amount\".",
        "ru": "Установка аксессуаров, электрооборудования и тюнинг-компонентов. Цены — за работу по установке; стоимость самих компонентов рассчитывается отдельно. Отметка «+» означает «от указанной суммы».",
        "uk": "Встановлення аксесуарів, електрообладнання та тюнінг-компонентів. Ціни — за роботу зі встановлення; вартість самих компонентів розраховується окремо. Позначка «+» означає «від зазначеної суми».",
        "pt": "Montagem de acessórios, equipamento elétrico e componentes de afinação. Preços de mão de obra de montagem; os componentes são orçamentados à parte. O sinal \"+\" significa \"a partir do valor indicado\".",
    },
    "columns": [
        {
            "label": {"en":"Accessories","ru":"Аксессуары","uk":"Аксесуари","pt":"Acessórios"},
            "items": [
                ({"en":"Crash bars","ru":"Дуги защиты","uk":"Дуги захисту","pt":"Barras de proteção"}, "50+ EUR"),
                ({"en":"Luggage systems","ru":"Багажные системы","uk":"Багажні системи","pt":"Sistemas de bagagem"}, "50+ EUR"),
                ({"en":"Hard cases","ru":"Кофры","uk":"Кофри","pt":"Malas rígidas"}, "100+ EUR"),
                ({"en":"Hand guards","ru":"Защита рук","uk":"Захист рук","pt":"Protetores de mãos"}, "50+ EUR"),
                ({"en":"Engine guard","ru":"Защита двигателя","uk":"Захист двигуна","pt":"Proteção do motor"}, "50+ EUR"),
            ],
        },
        {
            "label": {"en":"Electrical equipment","ru":"Электрооборудование","uk":"Електрообладнання","pt":"Equipamento elétrico"},
            "items": [
                ({"en":"USB socket","ru":"USB-разъём","uk":"USB-роз'єм","pt":"Tomada USB"}, "100+ EUR"),
                ({"en":"Auxiliary lights","ru":"Дополнительный свет","uk":"Додаткове світло","pt":"Luzes auxiliares"}, "150+ EUR"),
                ({"en":"Indicators","ru":"Поворотники","uk":"Поворотники","pt":"Piscas"}, "150+ EUR"),
                ({"en":"Brake light","ru":"Стоп-сигнал","uk":"Стоп-сигнал","pt":"Luz de travagem"}, "100+ EUR"),
                ({"en":"Heated grips","ru":"Подогрев ручек","uk":"Підігрів ручок","pt":"Punhos aquecidos"}, "100+ EUR"),
                ({"en":"Bluetooth / audio","ru":"Bluetooth / audio","uk":"Bluetooth / audio","pt":"Bluetooth / áudio"}, "100+ EUR"),
                ({"en":"Navigation","ru":"Навигация","uk":"Навігація","pt":"Navegação"}, "150+ EUR"),
            ],
        },
        {
            "label": {"en":"Tuning","ru":"Тюнинг","uk":"Тюнінг","pt":"Afinação"},
            "items": [
                ({"en":"Exhaust","ru":"Выхлоп","uk":"Вихлоп","pt":"Escape"}, "100+ EUR"),
                ({"en":"Air cleaner / intake","ru":"Air cleaner / intake","uk":"Air cleaner / intake","pt":"Filtro / admissão"}, "100+ EUR"),
                ({"en":"Fuel tuner","ru":"Fuel tuner","uk":"Fuel tuner","pt":"Fuel tuner"}, "150+ EUR"),
                ({"en":"Handlebar","ru":"Руль","uk":"Кермо","pt":"Guiador"}, "100+ EUR"),
                ({"en":"Risers","ru":"Risers","uk":"Risers","pt":"Risers"}, "100+ EUR"),
                ({"en":"Foot pegs","ru":"Foot pegs","uk":"Foot pegs","pt":"Pedais"}, "100+ EUR"),
                ({"en":"Forward controls","ru":"Forward controls","uk":"Forward controls","pt":"Comandos avançados"}, "100+ EUR"),
                ({"en":"Brake lines","ru":"Тормозные шланги","uk":"Гальмівні шланги","pt":"Tubos de travão"}, "150+ EUR"),
                ({"en":"Performance parts","ru":"Performance parts","uk":"Performance parts","pt":"Peças de performance"}, "100+ EUR"),
            ],
        },
    ],
    "note_install": {
        "en": "Fitting is half the result. Auxiliary lights, a fuel tuner or performance components only deliver with correct installation and setup. We select components for your model, agree the estimate and fit to torque spec.",
        "ru": "Установка — половина результата. Дополнительный свет, fuel tuner или performance-компоненты раскрываются только при грамотном монтаже и настройке. Подбираем компоненты под вашу модель, согласуем смету, ставим по моментам затяжки.",
        "uk": "Встановлення — половина результату. Додаткове світло, fuel tuner або performance-компоненти розкриваються лише за грамотного монтажу та налаштування. Підбираємо компоненти під вашу модель, погоджуємо кошторис, ставимо за моментами затягування.",
        "pt": "A montagem é metade do resultado. Luzes auxiliares, fuel tuner ou componentes de performance só rendem com instalação e afinação corretas. Selecionamos os componentes para o seu modelo, acordamos o orçamento e montamos com binário correto.",
    },
    "note_sourcing": {
        "en": "Component sourcing. OEM, aftermarket and tuning parts from major international catalogues. One contact for both service and parts: no need to source parts yourself.",
        "ru": "Подбор компонентов. OEM, aftermarket и тюнинг-детали — из крупных международных каталогов. Один контакт и для сервиса, и для запчастей: не нужно искать детали самостоятельно.",
        "uk": "Підбір компонентів. OEM, aftermarket і тюнінг-деталі — з великих міжнародних каталогів. Один контакт і для сервісу, і для запчастин: не потрібно шукати деталі самостійно.",
        "pt": "Aquisição de componentes. Peças OEM, aftermarket e de afinação dos principais catálogos internacionais. Um único contacto para serviço e peças: não precisa de procurar peças sozinho.",
    },
}


# ----- Section 06: Seasonal & other -----
SEC_06 = {
    "num": "06",
    "anchor": "seasonal-other",
    "title": {
        "en": "Seasonal prep",
        "ru": "Сезонная подготовка",
        "uk": "Сезонна підготовка",
        "pt": "Preparação sazonal",
    },
    "h2": {
        "en": "Seasonal preparation and other work",
        "ru": "Сезонная подготовка и прочие работы",
        "uk": "Сезонна підготовка та інші роботи",
        "pt": "Preparação sazonal e outros trabalhos",
    },
    "intro": {
        "en": "Preparing the motorcycle for a new season or a long trip, hourly and non-standard work. Inspection of key systems before use.",
        "ru": "Подготовка мотоцикла к новому сезону или дальнему путешествию, почасовые и нестандартные работы. Проверка ключевых систем перед эксплуатацией.",
        "uk": "Підготовка мотоцикла до нового сезону або дальньої подорожі, погодинні та нестандартні роботи. Перевірка ключових систем перед експлуатацією.",
        "pt": "Preparação da moto para uma nova época ou viagem longa, trabalhos à hora e não padronizados. Inspeção dos sistemas principais antes do uso.",
    },
    "cards": [
        {
            "name": {"en":"Season / trip preparation","ru":"Подготовка к сезону / путешествию","uk":"Підготовка до сезону / подорожі","pt":"Preparação para época / viagem"},
            "desc": {"en":"Comprehensive technical inspection before departure","ru":"Комплексная техническая проверка перед выездом","uk":"Комплексна технічна перевірка перед виїздом","pt":"Inspeção técnica completa antes da partida"},
            "price": "100 EUR", "price_from": True,
        },
        {
            "name": {"en":"Other work","ru":"Прочие работы","uk":"Інші роботи","pt":"Outros trabalhos"},
            "desc": {"en":"Work not listed — hourly rate","ru":"Работы, не вошедшие в прайс — почасовая ставка","uk":"Роботи, що не увійшли до прайсу — погодинна ставка","pt":"Trabalhos não listados — tarifa horária"},
            "price": "50 EUR",
            "price_suffix": "per_hour",
        },
    ],
    "note": {
        "en": "Transparent timelines and pricing. We state a realistic timeframe and final amount in advance. If additional work is found during the job, we agree it with you separately before continuing. No surprise bills at handover.",
        "ru": "Прозрачные сроки и стоимость. Мы заранее озвучиваем реалистичный срок и итоговую сумму. Если в процессе работ обнаруживается дополнительный объём — согласуем его с вами отдельно до того, как продолжить. Никаких счетов-сюрпризов при выдаче мотоцикла.",
        "uk": "Прозорі терміни та вартість. Ми заздалегідь озвучуємо реалістичний термін і підсумкову суму. Якщо в процесі робіт виявляється додатковий обсяг — узгоджуємо його з вами окремо до того, як продовжити. Жодних рахунків-сюрпризів при видачі мотоцикла.",
        "pt": "Prazos e preços transparentes. Indicamos antecipadamente um prazo realista e o valor final. Se surgir trabalho adicional durante o serviço, acordamo-lo consigo separadamente antes de continuar. Sem faturas surpresa na entrega.",
    },
}


# ----- Section 07: Customizing & Community (no fixed prices) -----
SEC_07 = {
    "num": "07",
    "anchor": "customizing-community",
    "title": {
        "en": "Customizing & community",
        "ru": "Кастомайзинг и сообщество",
        "uk": "Кастомайзинг та спільнота",
        "pt": "Customização e comunidade",
    },
    "h2": {
        "en": "Customizing and community",
        "ru": "Кастомайзинг и сообщество",
        "uk": "Кастомайзинг та спільнота",
        "pt": "Customização e comunidade",
    },
    "intro": {
        "en": "Bespoke motorcycle builds and a space where a community forms around the workshop.",
        "ru": "Индивидуальная постройка мотоциклов и пространство, в котором формируется сообщество вокруг мастерской.",
        "uk": "Індивідуальна побудова мотоциклів і простір, у якому формується спільнота навколо майстерні.",
        "pt": "Construção de motos à medida e um espaço onde se forma uma comunidade à volta da oficina.",
    },
    "custom_title": {
        "en": "From concept to championship build",
        "ru": "От идеи до чемпионского проекта",
        "uk": "Від ідеї до чемпіонського проєкту",
        "pt": "Do conceito ao projeto campeão",
    },
    "custom_body": {
        "en": "Full bespoke motorcycle builds — from concept and technical brief to final assembly and entry into international championships. The same engineering approach that earned ICM the AMD World Champions title, the world speed record at Bonneville and the win at the BMW Motorrad Customizing Championship. We take on the jobs other workshops turn down: tangled wiring, fabrication of non-standard parts, non-standard component fitment, restoration from lost specifications. Custom-project pricing is calculated individually after discussing the concept and technical requirements.",
        "ru": "Полная постройка кастом-мотоциклов под заказ — от концепта и технического задания до финальной сборки и участия в международных чемпионатах. Тот же инженерный подход, который принёс ICM титулы AMD World Champions, мировой рекорд скорости на Бонневиле и победу в BMW Motorrad Customizing Championship. Беремся за задачи, от которых отказываются другие мастерские: запутанная проводка, изготовление нестандартных деталей, нештатная посадка узлов, восстановление по утерянным спецификациям. Стоимость кастом-проектов рассчитывается индивидуально после обсуждения концепции и технических требований.",
        "uk": "Повна побудова кастом-мотоциклів на замовлення — від концепту й технічного завдання до фінального складання та участі в міжнародних чемпіонатах. Той самий інженерний підхід, який приніс ICM титули AMD World Champions, світовий рекорд швидкості на Бонневілі та перемогу в BMW Motorrad Customizing Championship. Беремося за завдання, від яких відмовляються інші майстерні: заплутана проводка, виготовлення нестандартних деталей, нештатна посадка вузлів, відновлення за втраченими специфікаціями. Вартість кастом-проєктів розраховується індивідуально після обговорення концепції та технічних вимог.",
        "pt": "Construção completa de motos à medida — do conceito e caderno técnico à montagem final e participação em campeonatos internacionais. A mesma abordagem de engenharia que deu à ICM o título AMD World Champions, o recorde mundial de velocidade em Bonneville e a vitória no BMW Motorrad Customizing Championship. Aceitamos os trabalhos que outras oficinas recusam: cablagem confusa, fabrico de peças não padrão, montagens fora de norma, restauro a partir de especificações perdidas. O preço dos projetos custom é calculado individualmente após discutir o conceito e os requisitos técnicos.",
    },
    "community": [
        {
            "title": {"en":"Lounge area in the workshop","ru":"Лаунж-зона в мастерской","uk":"Лаунж-зона в майстерні","pt":"Zona lounge na oficina"},
            "body": {"en":"Our space displays championship motorcycles and memorabilia — Beckman, Inspirium, Unbreakable and projects shown at the world's biggest exhibitions. Not a museum behind glass, but a living part of the workshop.","ru":"В нашем пространстве выставлены чемпионские мотоциклы и атрибутика — Beckman, Inspirium, Unbreakable и проекты, участвовавшие в крупнейших мировых выставках. Это не музей за стеклом, а живая часть мастерской.","uk":"У нашому просторі виставлені чемпіонські мотоцикли та атрибутика — Beckman, Inspirium, Unbreakable і проєкти, що брали участь у найбільших світових виставках. Це не музей за склом, а жива частина майстерні.","pt":"O nosso espaço exibe motos campeãs e memorabilia — Beckman, Inspirium, Unbreakable e projetos presentes nas maiores exposições do mundo. Não é um museu atrás de vidro, mas uma parte viva da oficina."},
        },
        {
            "title": {"en":"Drop in just for coffee","ru":"Заходите просто на кофе","uk":"Заїжджайте просто на каву","pt":"Passe só para um café"},
            "body": {"en":"You can drop by without bringing a bike for repair. Coffee, talking machines, discussing projects and routes — it's all part of the ICM atmosphere. Doors open Tuesday to Saturday, 10:00–18:00.","ru":"К нам можно заехать не только с мотоциклом на ремонт. Кофе, разговор о технике, обсуждение проектов и маршрутов — всё это часть атмосферы ICM. Двери открыты со вторника по субботу, 10:00–18:00.","uk":"До нас можна заїхати не лише з мотоциклом на ремонт. Кава, розмова про техніку, обговорення проєктів і маршрутів — усе це частина атмосфери ICM. Двері відчинені з вівторка по суботу, 10:00–18:00.","pt":"Pode passar sem trazer uma moto para reparação. Café, conversa sobre mecânica, projetos e rotas — faz tudo parte do ambiente ICM. Portas abertas de terça a sábado, 10:00–18:00."},
        },
        {
            "title": {"en":"Riders' community","ru":"Сообщество райдеров","uk":"Спільнота райдерів","pt":"Comunidade de motards"},
            "body": {"en":"A community of riders for whom machines are a way of life is forming around the workshop. Group rides, meetups, sharing experience and supporting local motorcycle culture in Greater Lisbon.","ru":"Вокруг мастерской формируется сообщество мотоциклистов, для которых техника — это образ жизни. Совместные выезды, встречи, обмен опытом и поддержка локальной мотокультуры в Большом Лиссабоне.","uk":"Навколо майстерні формується спільнота мотоциклістів, для яких техніка — це спосіб життя. Спільні виїзди, зустрічі, обмін досвідом і підтримка локальної мотокультури у Великому Лісабоні.","pt":"Forma-se à volta da oficina uma comunidade de motards para quem a mecânica é um modo de vida. Saídas em grupo, encontros, troca de experiência e apoio à cultura motard local na Grande Lisboa."},
        },
    ],
    "slogan": {
        "en": "Fix your ride & fuel your soul. This slogan captures what we do: we restore the motorcycle to the technical condition it was designed for — and with it, the very feeling of riding you chose it for.",
        "ru": "Fix your ride & fuel your soul. Этот слоган отражает то, чем мы занимаемся: возвращаем мотоциклу техническое состояние, на которое он рассчитан, а вместе с ним — то самое ощущение езды, ради которого вы его выбрали.",
        "uk": "Fix your ride & fuel your soul. Цей слоган відображає те, чим ми займаємося: повертаємо мотоциклу технічний стан, на який він розрахований, а разом із ним — те саме відчуття їзди, заради якого ви його обрали.",
        "pt": "Fix your ride & fuel your soul. Este lema resume o que fazemos: devolvemos à moto o estado técnico para que foi concebida — e, com ele, a sensação de conduzir pela qual a escolheu.",
    },
}


SECTIONS = [SEC_01, SEC_02, SEC_03, SEC_04, SEC_05, SEC_06, SEC_07]
