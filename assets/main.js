/* ======================================================================
   IRON CUSTOM MOTORS — Interactivity & i18n
   ====================================================================== */

/* ---------- Private, cookie-free lead measurement ---------- */
const ICM_LEADS_EVENT_URL = 'https://icm-leads.vg-ab6.workers.dev/event';
const ICM_LEAD_TYPES = new Set(['whatsapp', 'tel', 'form_submit', 'form_view']);
const ICM_LEADS_TEST_PAGE = '/**test**/';

function leadPageLang(){
  const match = location.pathname.match(/^\/(pt|ru|uk)(?:\/|$)/);
  return match ? match[1] : 'en';
}

function leadRefSource(){
  if(!document.referrer) return 'direct';
  try{
    const host = new URL(document.referrer).hostname.toLowerCase();
    return host === location.hostname.toLowerCase() ? 'internal' : host;
  }catch(e){
    return 'direct';
  }
}

function sendLeadEvent(type){
  if(!ICM_LEAD_TYPES.has(type)) return;
  const isAcceptanceTest = new URLSearchParams(location.search).get('icm-leads-test') === '1';
  const payload = JSON.stringify({
    type,
    page: isAcceptanceTest ? ICM_LEADS_TEST_PAGE : location.pathname,
    lang: isAcceptanceTest ? 'en' : leadPageLang(),
    ref: leadRefSource()
  });
  if(navigator.sendBeacon && navigator.sendBeacon(ICM_LEADS_EVENT_URL, payload)) return;
  fetch(ICM_LEADS_EVENT_URL, {
    method: 'POST',
    body: payload,
    mode: 'cors',
    keepalive: true,
    headers: {'Content-Type': 'text/plain;charset=UTF-8'}
  }).catch(()=>{});
}

window.icmSendLeadEvent = sendLeadEvent;

/* ---------- Translations ---------- */
const I18N = {
  en: {
    "nav.services":"Services","nav.brands":"Brands","nav.harleyHub":"Harley Hub","nav.harleyService":"Service","nav.harleyTuning":"Tuning","nav.harleyCustom":"Custom","nav.authorizedDealer":"Authorized Dealer","nav.authorizedDealerHub":"Dealer hub","nav.dealerCway":"C-Way","nav.projects":"Projects","nav.pricing":"Pricing","nav.about":"About","nav.aboutUs":"About us","nav.community":"Community","nav.reviews":"Reviews","nav.faq":"FAQ","nav.contact":"Contact","nav.blog":"Blog","nav.news":"News","nav.allServices":"All services","nav.allProjects":"All projects","nav.preInsp":"Pre-purchase inspection","nav.tyreServ":"Tyre fitting & wheel balancing","nav.expatWorkshop":"For expats","nav.brandHarley":"Harley-Davidson","nav.brandBmw":"BMW Motorrad","nav.brandDucati":"Ducati","nav.brandSuzuki":"Suzuki","nav.brandHonda":"Honda","nav.brandRoyalEnfield":"Royal Enfield","nav.brandTriumph":"Triumph","nav.bmwServ":"BMW Motorrad service","nav.hdServ":"Harley-Davidson service","nav.ducServ":"Ducati service","nav.suzukiServ":"Suzuki service","nav.hondaServ":"Honda service",
    "cta.bookHeader":"Book service","cta.bookService":"Book service","cta.whatsapp":"WhatsApp us","cta.requestForm":"Send request",
    "wa.prefill":"Hi Iron Custom Motors, I'd like to ask about service for my motorcycle. Please reply when you can.","contact.directions":"Get directions","brands.label":"Multi-brand workshop · OEM & aftermarket parts sourcing",
    "homeHarley.eyebrow":"Harley-Davidson at ICM","homeHarley.title":"Everything for your Harley.","homeHarley.text":"Service, diagnostics, tuning, custom builds and parts in one independent specialist workshop.","homeHarley.link":"Open Harley Hub","homeHarley.alt":"Harley-Davidson motorcycles at Iron Custom Motors in Cascais",
    "cookie.text":"We use cookies to measure traffic and improve the site. No third-party advertising.","cookie.accept":"Accept","cookie.reject":"Reject",
    "hero.pill1":"Cascais · Greater Lisbon","hero.pill2":"Since 2010","hero.pill3":"<a href=\"/english-speaking-motorcycle-workshop/\" hreflang=\"en\">EN</a><span class=\"lang-sep\">·</span><a href=\"/ru/english-speaking-motorcycle-workshop/\" hreflang=\"ru\">RU</a><span class=\"lang-sep\">·</span><a href=\"/uk/english-speaking-motorcycle-workshop/\" hreflang=\"uk\">UA</a><span class=\"lang-sep\">·</span><a href=\"/pt/english-speaking-motorcycle-workshop/\" hreflang=\"pt\">PT</a>",
    "hero.title1":"Premium","hero.title2":"motorcycle","hero.title3":"service","hero.title4":"in Cascais",
    "hero.sub":"Diagnostics, maintenance, repair, spare parts and consumables, tuning solutions and custom project expertise — by the team behind world-champion builds and a Bonneville record.",
    "hero.tag1":"AMD World Champions","hero.tag2":"Bonneville record holders","hero.tag3":"BMW Motorrad Champ. 2023",
    "hero.scroll":"Scroll · Iron Custom Motors",
    "services.learn":"Learn more","services.eyebrow":"What we do","services.title":"Service. Parts.<br/>Upgrades. Custom.","services.sub":"Iron Custom Motors services motorcycles, supplies spare parts and consumables, and offers tuning and upgrade solutions from major global catalogs and brands.",
    "services.s1.title":"Motorcycle service & repair","services.s1.desc":"Diagnostics, scheduled maintenance, oil & filter, brake and suspension service, chain & sprockets, tires, electrical diagnostics and general repair.","services.cta":"Book service",
    "services.s2.title":"Parts & consumables","services.s2.desc":"OEM, aftermarket and tuning parts. Service consumables and accessories. Sourced through major international catalogs — request even if you don't need our workshop.","services.cta2":"Request parts",
    "services.s3.title":"Upgrades & tuning","services.s3.desc":"Performance, suspension, brakes, exhaust, lighting, protection, touring and luggage. Functional upgrades selected for how you actually ride.","services.cta3":"Ask about upgrades",
    "services.s4.title":"Custom & special projects","services.s4.desc":"Custom consultations, bespoke builds, individual engineering solutions and project planning. The team that delivered world-champion motorcycles is the team that builds yours.","services.cta4":"Discuss a project",
    "services.s5.title":"Tyre fitting & wheel balancing","services.s5.desc":"Motorcycle-specific tyre fitting and wheel balancing for wheels up to 30 inches and 400 mm, including spoked, vintage, Harley fat and custom wheels.","services.cta5":"Tyre service",
    "services.s6.title":"Pre-purchase inspection","services.s6.desc":"Independent expert check before you buy a used motorcycle in Portugal. Mechanics, electrics, frame and hidden wear — written report with photos within 24 hours.","services.cta6":"Inspection details",
    "pricing.eyebrow":"Pricing · 2025","pricing.title":"Transparent pricing,<br/>no surprises.","pricing.sub":"Written estimates before any work begins. Fixed or \"from\" prices for every service. All taxes included. The full 2025 price list covers diagnostics, scheduled maintenance, brakes, valves, wheels, accessories, tuning and seasonal preparation.","pricing.p1.title":"Pre-purchase inspection","pricing.p1.desc":"Full technical check before you buy a used motorcycle in Portugal.","pricing.p1.price":"150","pricing.p1.cur":"EUR","pricing.p2.title":"Scheduled service","pricing.p2.desc":"Manufacturer-spec maintenance. Consumables included in the price.","pricing.p2.price":"150","pricing.p2.cur":"EUR","pricing.p2.from":"from","pricing.p3.title":"Fault diagnostics","pricing.p3.desc":"We find the root cause, not just the symptom. Electrics, engine, running gear.","pricing.p3.price":"50–350","pricing.p3.cur":"EUR","pricing.p4.title":"Hourly work","pricing.p4.desc":"Anything outside the price list — transparent time tracking, written estimate up front.","pricing.p4.price":"50","pricing.p4.cur":"EUR / hour","pricing.cta":"View full price list","pricing.tax":"All prices include taxes and fees",
    "why.eyebrow":"Why Iron Custom Motors","why.title":"Championship-grade<br/>workshop, daily-rider service","why.sub":"A world-class custom team that actually picks up the phone when your bike won't start. That's the gap we close.",
    "why.r1.t":"World-level engineering","why.r1.d":"AMD World Champions. Bonneville record holders. BMW Motorrad Customizing Champions 2023. The expertise behind your routine service.",
    "why.r2.t":"Parts sourcing in-house","why.r2.d":"OEM, aftermarket, tuning components and consumables from major international catalogs — one point of contact for service and parts.",
    "why.r3.t":"Service in your language","why.r3.d":"English, Russian, Ukrainian and Portuguese. No language tax — clear communication, written estimates, honest timelines.",
    "why.r4.t":"Transparent process","why.r4.d":"Diagnose first, then quote. Photos and updates during the work. No surprise invoices.",
    "why.r5.t":"Complex jobs welcome","why.r5.d":"Wiring nightmares, custom parts fabrication, fitment problems, lost specs — the work other shops decline.",
    "why.r6.t":"Treat the machine right","why.r6.d":"Clean workspace. Torque specs. Original or premium parts. The way we'd service our own bikes — because we do.",
    "why.badge":"years building, racing, fixing",
    "community.stripTitle":"The <span class=\"accent\">Inspirium</span> · Bonneville record holder, on display.","exterior.title":"Drop in. <span class=\"accent\">We're here.</span>","teamBanner.title":"The team that <span class=\"accent\">picks up the phone.</span>","teamBanner.sub":"World-champion engineers behind every routine service. Same hands. Same standard. Now in Cascais.","teamBanner.row1":"<strong>15+</strong> years building, racing, fixing","teamBanner.row2":"<strong>3×</strong> world championships","teamBanner.row3":"Cascais · Lisboa · Portugal","story.eyebrow":"Our story","story.title":"From a Kharkiv<br/>workshop to world<br/>championship podiums",
    "story.p1":"Iron Custom Motors was founded in 2010 with one goal — to build motorcycles that could stand on the world stage. Six years later we did exactly that: AMD World Champions, café racer class, with the project Beckman.",
    "story.p2":"In 2017 the team set a world speed record at Bonneville Salt Flats with the Inspirium 350APS-VG. In 2023 — BMW Motorrad Customizing Champions. Projects shown at the world's top motorcycle events.",
    "story.p3":"In 2025 we brought the workshop to Cascais, Greater Lisbon. Same team, same engineering culture, now within reach of every rider on the Portuguese coast.",
    "story.quote":"“The same hands that built world-champion motorcycles now keep yours running every day.”",
    "story.stat1l":"Founded","story.stat1s":"15 years of continuous craft","story.stat2l":"World championships","story.stat2s":"AMD · BMW Motorrad · Bonneville","story.stat3l":"Projects delivered","story.stat3s":"Service · custom · engineering","story.stat4l":"Brands serviced","story.stat4s":"From BMW to one-off builds",
    "community.eyebrow":"Lounge & Community","community.title":"More than a service.<br/>A place for riders, stories<br/>and motorcycle culture.","community.sub":"The Iron Custom Motors lounge is where the brand lives offline — championship bikes, trophies, conversations and coffee. Come by even if your bike is fine.",
    "community.heroTitle":"A lounge built around <em>real</em> stories.","community.heroSub":"Inspirium Bonneville salt-flat bike, championship trophies, riding gear and racing memorabilia. This is where the workshop becomes a brand.","community.heroBadge":"Cascais · Open Tue–Sat","community.ctaVisit":"Plan your visit",
    "community.introTitle":"Beyond the workshop.","community.introP1":"The lounge is part of what makes Iron Custom Motors feel like Iron Custom Motors. Wood-panelled walls, championship-winning machines on the floor, race-worn leathers on the wall, trophies from Bonneville, helmets, books, magazines, riding masks.","community.introP2":"It's a place to wait while your bike is being serviced — but more importantly, it's a place to drop in even when you don't need anything fixed. Have a coffee. Look at the Inspirium up close. Talk to people who actually rode it.","community.introP3":"No pretension, no membership, no dress code. If you ride or you love motorcycles — you're welcome.",
    "community.findTitle":"What you'll find here","community.f1.t":"Championship machines","community.f1.d":"Inspirium Bonneville record bike on display, plus other custom builds.","community.f2.t":"Trophies & race artifacts","community.f2.d":"AMD World Championship, Bonneville Speed Week, BMW Motorrad — the actual hardware.","community.f3.t":"Coffee & conversation","community.f3.d":"Drop in, sit down, talk bikes. Tuesday to Saturday during workshop hours.","community.f4.t":"Books, magazines, gear","community.f4.d":"Riding leathers, helmets, masks, books and curated motorcycle memorabilia.","community.f5.t":"A place to be a rider","community.f5.d":"Group rides, project presentations, themed evenings, rider meetups — building the local scene.",
    "community.promiseTitle":"You're always welcome to drop by, have a coffee, talk motorcycles and spend time with <span class=\"em\">people who get it.</span>","community.promiseSub":"Even without an appointment, even without a service request — the door is open. That's how we want this place to feel.",
    "projects.p1.label":"World Speed Record · Bonneville 2017","projects.p1.title":"Inspirium","projects.p1.desc":"World speed record motorcycle. Class 350APS-VG, Bonneville Salt Flats. Vintage 1953 IZH-49 platform.","projects.p2.label":"AMD World Champion · 2016","projects.p2.title":"Beckman","projects.p2.desc":"World champion café racer. Hand-built three-cylinder engine. AMD World Championship 2016 winner.","projects.p3.label":"BMW Motorrad Customizing Champion","projects.p3.title":"Unbreakable","projects.p3.desc":"BMW Motorrad Customizing Championship winner. Exhibited at BMW Motorrad Welt.","projects.p4.label":"Geneva · Goodwood Concept","projects.p4.title":"Quanta R","projects.p4.desc":"Concept for Geneva Motor Show and Goodwood. AWD, 2.5L turbo boxer, up to 600 hp, handmade aluminum body.","projects.p5.label":"BMW R 18 Custom Dragster","projects.p5.title":"Burly","projects.p5.desc":"BMW R 18 reborn as a custom dragster. Foundation for a full line of carbon, exhaust and styling kits.","projects.p6.label":"Café Racer podium · Ericeira 2026","projects.p6.title":"Sturmvogel","projects.p6.desc":"Sturmvogel added a new Portuguese result to its history: 2nd place in the Café Racer category at Ericeira Kustom Fest 2026.","projects.p7.label":"Retro-Futurist · AMD 2018","projects.p7.title":"Geometric","projects.p7.desc":"Retro-futurist build. AMD World Championship 2018, world's first spoked hubless front wheel.","projects.p8.label":"Custom Harley-Davidson Dyna","projects.p8.title":"Joker","projects.p8.desc":"Harley-Davidson Dyna Street Bob with bold urban stance, premium hardware and pop-art paint.","projects.p9.label":"Best Paint winner · Ericeira 2026","projects.p9.title":"Hell Boy","projects.p9.desc":"Hell Boy won 1st place in Best Paint at Ericeira Kustom Fest 2026, confirming the build's theatrical airbrush identity.","projects.p10.label":"American Custom · Harley spirit","projects.p10.title":"True Religion","projects.p10.desc":"Built around freedom, attitude and the timeless spirit of American custom culture.","projects.eyebrow":"Selected projects","projects.title":"A few of the bikes<br/>we're proud of","projects.sub":"Award-winning builds that put us on the international map. The same engineering goes into every service we do.",
    
    
    
    
    "process.eyebrow":"How it works","process.title":"From request to ride —<br/>five steps, no surprises",
    "process.s1t":"Request","process.s1d":"Send a message via WhatsApp, form or call. Tell us what you ride and what's wrong.",
    "process.s2t":"Diagnostics","process.s2d":"We inspect, run diagnostics and identify the real cause — not just the symptom.",
    "process.s3t":"Estimate","process.s3d":"Written estimate, parts list, timeline. You approve before we lift a wrench.",
    "process.s4t":"Work","process.s4d":"Service or build, with photo updates. Torque specs, clean install, no shortcuts.",
    "process.s5t":"Ride away","process.s5d":"Test, hand-over, follow-up. We're here for the next service too.",
    "reviews.basedOn":"Based on","reviews.gReviews":"Google reviews","reviews.viewAll":"View all on Google →","reviews.leaveReview":"Leave a review on Google","reviews.eyebrow":"What riders say","reviews.title":"Trusted by riders<br/>and builders worldwide",
    "reviews.r1.text":"“Brought my BMW R nineT for a stubborn electrical issue three other shops couldn't solve. Iron Custom diagnosed it in under an hour and explained it in plain English. Honest pricing, world-class work.”","reviews.r1.role":"BMW R nineT · UK expat in Cascais",
    "reviews.r2.text":"“Pre-purchase inspection saved me €4,200. The bike looked perfect — they found a hidden frame issue. Sent me a detailed report with photos the same day. This is how it should work.”","reviews.r2.role":"Ducati Monster buyer · Lisbon",
    "reviews.r3.text":"“Finally a workshop in Portugal that treats a Harley like a Harley. Custom exhaust, suspension setup and a tuning session — bike feels brand new. They speak Russian, which made everything easier.”","reviews.r3.role":"Harley-Davidson FXDR · Estoril",
    "faq.eyebrow":"Frequently asked","faq.title":"Answers before<br/>you ask","faq.sub":"Don't see your question? WhatsApp us — we usually reply within an hour during business days.","faq.cta":"Ask on WhatsApp",
    "faq.q1":"What kind of motorcycles do you work with?","faq.a1":"We work with motorcycles across different segments and service requests — routine maintenance, repairs, upgrades, parts supply and selected custom work. Send your model, year and request via WhatsApp and we'll confirm.",
    "faq.q2":"Can I contact you only for parts?","faq.a2":"Yes. We supply spare parts, service consumables, accessories and tuning solutions sourced from major international catalogs and brands — even if you don't need our workshop.",
    "faq.q3":"Do you only do custom motorcycles?","faq.a3":"No. Custom expertise is part of our background, but the workshop is built around real motorcycle service, repair, parts supply, upgrades and selected projects.",
    "faq.q4":"How should I contact you?","faq.a4":"The fastest option is WhatsApp at +351 917 961 230. Send your motorcycle model, year and request, and we'll respond with the next step.",
    "faq.q5":"Can you help with upgrades and tuning parts?","faq.a5":"Yes. We supply and install upgrades, accessories and tuning parts sourced from major global catalogs and brands. We approach upgrades as functional, rider-specific improvements based on real use.",
    "faq.q6":"Do I need an appointment?","faq.a6":"For service work — yes, it lets us prepare parts and a workspace. For quick advice or parts requests, just message us. WhatsApp is the fastest channel.",
    "faq.q7":"Where exactly is the workshop?","faq.a7":"R. António José da Silva 100 B, 2785-253 São Domingos de Rana, Cascais, Lisbon, Portugal. Open Tuesday to Saturday, 10:00–18:00.",
    "contact.eyebrow":"Get in touch","contact.title":"Tell us about<br/>your machine","contact.sub":"Service, parts, upgrades or custom — we'll point you to the right next step. Reply during business hours, usually within an hour.","contact.phone":"Phone","contact.address":"Workshop",
    "footer.tagline":"Premium motorcycle service, parts, upgrades and custom expertise in Cascais. Engineering culture from world-champion projects, applied to every job.",
    "footer.col1":"Services","footer.col2":"Company","footer.col3":"Workshop",
    "footer.hours":"Tue–Sat · 10:00–18:00<br/>Closed Sun &amp; Mon","footer.rights":"All rights reserved",
    "form.title":"Send a request","form.sub":"Service, parts, upgrades or custom — tell us what you need. We'll come back to you within business hours.",
    "form.name":"Your name","form.phone":"Phone / WhatsApp","form.email":"Email (optional)","form.vehicle":"Motorcycle (brand · model · year)","form.service":"Request type",
    "form.opt1":"Motorcycle service & repair","form.opt2":"Parts & consumables","form.opt3":"Upgrades & tuning","form.opt4":"Custom & special project","form.opt5":"Other / not sure",
    "form.message":"Tell us about the job","form.note":"By sending you agree to be contacted about this request. No spam, ever.","form.submit":"Send request","form.successT":"Request received","form.successP":"We'll reply via WhatsApp or email within business hours. Talk soon."
  },
  ru: {
    "nav.services":"Услуги","nav.brands":"Бренды","nav.harleyHub":"Harley Hub","nav.harleyService":"Сервис","nav.harleyTuning":"Тюнинг","nav.harleyCustom":"Кастом","nav.authorizedDealer":"Официальный дилер","nav.authorizedDealerHub":"Дилерский хаб","nav.dealerCway":"C-Way","nav.projects":"Проекты","nav.pricing":"Цены","nav.about":"О нас","nav.aboutUs":"О нас","nav.community":"Сообщество","nav.reviews":"Отзывы","nav.faq":"FAQ","nav.contact":"Контакты","nav.blog":"Блог","nav.news":"Новости","nav.allServices":"Все услуги","nav.allProjects":"Все проекты","nav.preInsp":"Инспекция перед покупкой","nav.tyreServ":"Шиномонтаж и балансировка","nav.expatWorkshop":"Для экспатов","nav.brandHarley":"Harley-Davidson","nav.brandBmw":"BMW Motorrad","nav.brandDucati":"Ducati","nav.brandSuzuki":"Suzuki","nav.brandHonda":"Honda","nav.brandRoyalEnfield":"Royal Enfield","nav.brandTriumph":"Triumph","nav.bmwServ":"Сервис BMW Motorrad","nav.hdServ":"Сервис Harley-Davidson","nav.ducServ":"Сервис Ducati","nav.suzukiServ":"Сервис Suzuki","nav.hondaServ":"Сервис Honda",
    "cta.bookHeader":"Записаться","cta.bookService":"Записаться на сервис","cta.whatsapp":"Написать в WhatsApp","cta.requestForm":"Отправить заявку",
    "wa.prefill":"Здравствуйте, Iron Custom Motors! Хочу обсудить сервис для своего мотоцикла. Ответьте, когда сможете.","contact.directions":"Маршрут","brands.label":"Мульти-бренд сервис · поставка OEM и aftermarket запчастей",
    "homeHarley.eyebrow":"Harley-Davidson в ICM","homeHarley.title":"Всё для вашего Harley.","homeHarley.text":"Сервис, диагностика, тюнинг, кастом-проекты и запчасти в одной независимой специализированной мастерской.","homeHarley.link":"Открыть Harley Hub","homeHarley.alt":"Мотоциклы Harley-Davidson в Iron Custom Motors, Кашкайш",
    "cookie.text":"Мы используем cookies, чтобы понимать посещаемость и улучшать сайт. Без сторонней рекламы.","cookie.accept":"Принять","cookie.reject":"Отклонить",
    "hero.pill1":"Кашкайш · Лиссабон","hero.pill2":"С 2010 года","hero.pill3":"<a href=\"/english-speaking-motorcycle-workshop/\" hreflang=\"en\">EN</a><span class=\"lang-sep\">·</span><a href=\"/ru/english-speaking-motorcycle-workshop/\" hreflang=\"ru\">RU</a><span class=\"lang-sep\">·</span><a href=\"/uk/english-speaking-motorcycle-workshop/\" hreflang=\"uk\">UA</a><span class=\"lang-sep\">·</span><a href=\"/pt/english-speaking-motorcycle-workshop/\" hreflang=\"pt\">PT</a>",
    "hero.title1":"Премиальный","hero.title2":"мотосервис","hero.title3":"в Кашкайше","hero.title4":"",
    "hero.sub":"Диагностика, обслуживание, ремонт, оригинальные и тюнинг-запчасти, расходники, апгрейды и кастом-проекты — от команды чемпионов мира и рекордсменов Bonneville.",
    "hero.tag1":"Чемпионы мира AMD","hero.tag2":"Рекорд Bonneville","hero.tag3":"Чемпионы BMW Motorrad 2023",
    "hero.scroll":"Прокрути · Iron Custom Motors",
    "services.learn":"Подробнее","services.eyebrow":"Что мы делаем","services.title":"Сервис. Запчасти.<br/>Апгрейды. Кастом.","services.sub":"Iron Custom Motors обслуживает мотоциклы, поставляет оригинальные и тюнинг-запчасти, расходники и аксессуары из ведущих международных каталогов и брендов.",
    "services.s1.title":"Сервис и ремонт","services.s1.desc":"Диагностика, плановое ТО, замена масла и фильтров, тормоза, подвеска, цепь и звёзды, шиномонтаж, электрика и общий ремонт.","services.cta":"Записаться",
    "services.s2.title":"Запчасти и расходники","services.s2.desc":"OEM, афтермаркет и тюнинг-запчасти. Расходники и аксессуары из ведущих международных каталогов — даже если вам не нужен наш сервис, можем заказать.","services.cta2":"Запросить запчасти",
    "services.s3.title":"Апгрейды и тюнинг","services.s3.desc":"Производительность, подвеска, тормоза, выхлоп, свет, защита, тур-обвес и кофры. Функциональные апгрейды под ваш стиль езды.","services.cta3":"Узнать про апгрейды",
    "services.s4.title":"Кастом и спец-проекты","services.s4.desc":"Кастом-консультации, индивидуальные сборки, инженерные решения и планирование проекта. Та же команда, что строила чемпионов мира — для вашего мотоцикла.","services.cta4":"Обсудить проект",
    "services.s5.title":"Шиномонтаж и балансировка","services.s5.desc":"Профильный мотоциклетный шиномонтаж и балансировка колёс до 30 дюймов и 400 мм, включая спицы, винтаж, Harley fat и кастом.","services.cta5":"Шиномонтаж",
    "services.s6.title":"Предпокупочная инспекция","services.s6.desc":"Независимая экспертная проверка перед покупкой б/у мотоцикла в Португалии. Механика, электрика, рама и скрытый износ — письменный отчёт с фото в течение 24 часов.","services.cta6":"Подробнее об инспекции",
    "pricing.eyebrow":"Прайс-лист · 2025","pricing.title":"Прозрачные цены,<br/>без сюрпризов.","pricing.sub":"Письменная смета до начала работ. Фиксированные цены или «от» на каждую услугу. Все налоги включены. Полный прайс 2025 года покрывает диагностику, плановое ТО, тормоза, клапаны, колёса, аксессуары, тюнинг и сезонную подготовку.","pricing.p1.title":"Диагностика перед покупкой","pricing.p1.desc":"Полная техническая проверка перед покупкой б/у мотоцикла в Португалии.","pricing.p1.price":"150","pricing.p1.cur":"EUR","pricing.p2.title":"Плановое ТО","pricing.p2.desc":"Обслуживание по нормативам производителя. Расходники включены в цену.","pricing.p2.price":"150","pricing.p2.cur":"EUR","pricing.p2.from":"от","pricing.p3.title":"Диагностика неисправностей","pricing.p3.desc":"Ищем причину, а не симптом. Электрика, двигатель, ходовая часть.","pricing.p3.price":"50–350","pricing.p3.cur":"EUR","pricing.p4.title":"Почасовая работа","pricing.p4.desc":"Всё, что не вошло в прайс — прозрачный учёт времени, смета вперёд.","pricing.p4.price":"50","pricing.p4.cur":"EUR / час","pricing.cta":"Посмотреть полный прайс","pricing.tax":"Все цены включают налоги и сборы",
    "why.eyebrow":"Почему Iron Custom Motors","why.title":"Чемпионская мастерская,<br/>сервис каждый день","why.sub":"Команда мирового уровня, которая действительно отвечает на звонок, когда мотоцикл не заводится. Этот разрыв мы и закрываем.",
    "why.r1.t":"Инжиниринг мирового уровня","why.r1.d":"Чемпионы мира AMD. Рекордсмены Bonneville. Чемпионы BMW Motorrad 2023. Эта экспертиза стоит за каждым рутинным сервисом.",
    "why.r2.t":"Запчасти под одной крышей","why.r2.d":"OEM, афтермаркет, тюнинг и расходники из ведущих международных каталогов — один контакт для сервиса и запчастей.",
    "why.r3.t":"Сервис на вашем языке","why.r3.d":"Английский, русский, украинский, португальский. Чёткая коммуникация, письменные сметы, честные сроки.",
    "why.r4.t":"Прозрачный процесс","why.r4.d":"Сначала диагностика, потом смета. Фото и обновления по ходу работ. Никаких сюрпризов в счёте.",
    "why.r5.t":"Беремся за сложное","why.r5.d":"Запутанная электрика, изготовление кастом-деталей, проблемы фитмента, утерянные спецификации — то, от чего отказываются другие.",
    "why.r6.t":"Уважение к технике","why.r6.d":"Чистая мастерская. Моменты затяжки. Оригинальные или премиум-запчасти. Так, как обслуживали бы свой мотоцикл — потому что мы это и делаем.",
    "why.badge":"лет строим, гоняем, чиним",
    "community.stripTitle":"<span class=\"accent\">Inspirium</span> · рекордсмен Bonneville, на экспозиции.","exterior.title":"Заезжайте. <span class=\"accent\">Мы здесь.</span>","teamBanner.title":"Команда, которая <span class=\"accent\">берёт трубку.</span>","teamBanner.sub":"Инженеры мирового уровня за каждым рутинным сервисом. Те же руки. Тот же стандарт. Теперь в Кашкайше.","teamBanner.row1":"<strong>15+</strong> лет строим, гоняем, чиним","teamBanner.row2":"<strong>3×</strong> чемпионы мира","teamBanner.row3":"Кашкайш · Лиссабон · Португалия","story.eyebrow":"Наша история","story.title":"От мастерской в Харькове<br/>до подиумов мировых<br/>чемпионатов",
    "story.p1":"Iron Custom Motors основан в 2010 году с одной целью — строить мотоциклы, которые смогут выйти на мировую сцену. Через шесть лет мы это сделали: чемпионы мира AMD в классе café racer с проектом Beckman.",
    "story.p2":"В 2017 команда установила мировой рекорд скорости на солончаке Bonneville на Inspirium 350APS-VG. В 2023 — чемпионы BMW Motorrad Customizing. Проекты на ведущих мотовыставках мира.",
    "story.p3":"В 2025 мы привезли мастерскую в Кашкайш, Большой Лиссабон. Та же команда, та же инженерная культура — теперь в шаговой доступности для каждого райдера на побережье Португалии.",
    "story.quote":"«Те же руки, что строили чемпионов мира, теперь поддерживают ваш мотоцикл в форме каждый день.»",
    "story.stat1l":"Основание","story.stat1s":"15 лет непрерывной работы","story.stat2l":"Чемпионств мира","story.stat2s":"AMD · BMW Motorrad · Bonneville","story.stat3l":"Реализованных проектов","story.stat3s":"Сервис · кастом · инжиниринг","story.stat4l":"Брендов в работе","story.stat4s":"От BMW до индивидуальных сборок",
    "community.eyebrow":"Lounge и Сообщество","community.title":"Больше, чем сервис.<br/>Место для райдеров, историй<br/>и мотокультуры.","community.sub":"Lounge-зона Iron Custom Motors — это бренд офлайн: чемпионские мотоциклы, трофеи, разговоры и кофе. Заезжайте, даже если с мотоциклом всё в порядке.",
    "community.heroTitle":"Lounge на <em>настоящих</em> историях.","community.heroSub":"Inspirium с солончака Bonneville, чемпионские трофеи, гоночная экипировка и racing-атрибутика. Здесь мастерская превращается в бренд.","community.heroBadge":"Кашкайш · Вт–Сб","community.ctaVisit":"Спланировать визит",
    "community.introTitle":"Не только мастерская.","community.introP1":"Lounge — часть того, что делает Iron Custom Motors собой. Деревянные стены, чемпионские мотоциклы на полу, гоночные костюмы на стенах, трофеи Bonneville, шлемы, книги, журналы, гоночные маски.","community.introP2":"Это место, где можно подождать, пока обслуживают ваш мотоцикл — но главное, сюда можно заехать просто так. Выпить кофе. Посмотреть на Inspirium вблизи. Поговорить с людьми, которые на нём ехали.","community.introP3":"Без пафоса, без членства, без дресс-кода. Если вы ездите или любите мотоциклы — вам сюда.",
    "community.findTitle":"Что вы здесь найдёте","community.f1.t":"Чемпионские машины","community.f1.d":"Рекордсмен Bonneville Inspirium на постаменте, а также другие кастом-сборки.","community.f2.t":"Трофеи и гоночные артефакты","community.f2.d":"AMD World Championship, Bonneville Speed Week, BMW Motorrad — оригинальная атрибутика.","community.f3.t":"Кофе и общение","community.f3.d":"Заезжайте, садитесь, говорим о мотоциклах. Вторник–суббота в рабочие часы.","community.f4.t":"Книги, журналы, экипировка","community.f4.d":"Гоночные костюмы, шлемы, маски, книги и тщательно подобранная мотоатрибутика.","community.f5.t":"Место быть райдером","community.f5.d":"Совместные выезды, презентации проектов, тематические вечера, встречи райдеров — строим локальную сцену.",
    "community.promiseTitle":"Всегда можно заехать, выпить кофе, поговорить о мотоциклах и провести время с <span class=\"em\">правильными людьми.</span>","community.promiseSub":"Даже без записи, даже без сервисной задачи — дверь открыта. Именно такой атмосферы мы и добиваемся.",
    "projects.p1.label":"Мировой рекорд · Bonneville 2017","projects.p1.title":"Inspirium","projects.p1.desc":"Мотоцикл — мировой рекорд скорости. Класс 350APS-VG, солончак Бонневилль. Винтажная платформа ИЖ-49 1953.","projects.p2.label":"Чемпион мира AMD · 2016","projects.p2.title":"Beckman","projects.p2.desc":"Чемпион мира café racer. Трёхцилиндровый двигатель ручной работы. Победитель AMD World Championship 2016.","projects.p3.label":"Победитель BMW Motorrad Customizing","projects.p3.title":"Unbreakable","projects.p3.desc":"Победитель BMW Motorrad Customizing Championship. Экспонировался в BMW Motorrad Welt.","projects.p4.label":"Концепт Geneva · Goodwood","projects.p4.title":"Quanta R","projects.p4.desc":"Концепт для Geneva Motor Show и Goodwood. AWD, турбобоксер 2.5L до 600 л.с., алюминиевый кузов ручной работы.","projects.p5.label":"BMW R 18 кастом-драгстер","projects.p5.title":"Burly","projects.p5.desc":"BMW R 18, переродившийся как кастом-драгстер. Основа для линейки carbon, выхлопа и стайлинг-комплектов.","projects.p6.label":"Café Racer · 2-е место Ericeira 2026","projects.p6.title":"Sturmvogel","projects.p6.desc":"Sturmvogel добавил к своей истории новый португальский результат: 2-е место в категории Café Racer на Ericeira Kustom Fest 2026.","projects.p7.label":"Ретро-футуризм · AMD 2018","projects.p7.title":"Geometric","projects.p7.desc":"Ретро-футуристическая сборка. AMD World Championship 2018, первое в мире спицованное безступичное переднее колесо.","projects.p8.label":"Кастом Harley-Davidson Dyna","projects.p8.title":"Joker","projects.p8.desc":"Harley-Davidson Dyna Street Bob с агрессивной городской посадкой, премиум-компонентами и поп-арт окраской.","projects.p9.label":"Best Paint · победитель Ericeira 2026","projects.p9.title":"Hell Boy","projects.p9.desc":"Hell Boy занял 1-е место в Best Paint на Ericeira Kustom Fest 2026, подтвердив силу своей театральной аэрографии.","projects.p10.label":"Американский кастом · Дух Harley","projects.p10.title":"True Religion","projects.p10.desc":"Построен вокруг свободы, характера и вневременного духа американской кастом-культуры.","projects.eyebrow":"Избранные проекты","projects.title":"Несколько мотоциклов,<br/>которыми мы гордимся","projects.sub":"Победные сборки, выведшие нас на международную карту. Тот же инжиниринг идёт в каждый сервис.",
    
    
    
    
    "process.eyebrow":"Как мы работаем","process.title":"От заявки до выезда —<br/>пять шагов, без сюрпризов",
    "process.s1t":"Заявка","process.s1d":"WhatsApp, форма или звонок. Расскажите, что у вас за мотоцикл и что не так.",
    "process.s2t":"Диагностика","process.s2d":"Осматриваем, проводим диагностику и ищем причину — не симптом.",
    "process.s3t":"Смета","process.s3d":"Письменная смета, список запчастей, сроки. Согласовываем до начала работ.",
    "process.s4t":"Работа","process.s4d":"Сервис или сборка, с фото-апдейтами. Моменты затяжки, чистая установка, без срезаний углов.",
    "process.s5t":"Выдача","process.s5d":"Тест, передача, follow-up. Мы рядом и для следующего сервиса.",
    "reviews.basedOn":"На основе","reviews.gReviews":"отзывов в Google","reviews.viewAll":"Все отзывы в Google →","reviews.leaveReview":"Оставить отзыв в Google","reviews.eyebrow":"Что говорят райдеры","reviews.title":"Доверяют райдеры и<br/>билдеры по всему миру",
    "reviews.r1.text":"«Привёз свой BMW R nineT с упрямой электрикой, которую три других сервиса не смогли решить. Iron Custom разобрался меньше чем за час и объяснил всё простым языком. Честные цены, мировой уровень.»","reviews.r1.role":"BMW R nineT · экспат из UK в Кашкайше",
    "reviews.r2.text":"«Предпокупочная инспекция спасла мне 4 200 €. Мотоцикл выглядел идеально, но ребята нашли скрытую проблему с рамой. Прислали детальный отчёт с фото в тот же день. Вот как должно работать.»","reviews.r2.role":"Покупатель Ducati Monster · Лиссабон",
    "reviews.r3.text":"«Наконец сервис в Португалии, который относится к Harley как к Harley. Кастомный выхлоп, настройка подвески и тюнинг — мотоцикл как новый. Говорят по-русски, всё намного проще.»","reviews.r3.role":"Harley-Davidson FXDR · Эшторил",
    "faq.eyebrow":"Частые вопросы","faq.title":"Ответы до того,<br/>как вы спросите","faq.sub":"Нет вашего вопроса? Напишите в WhatsApp — обычно отвечаем в течение часа в рабочее время.","faq.cta":"Спросить в WhatsApp",
    "faq.q1":"С какими мотоциклами вы работаете?","faq.a1":"Работаем с мотоциклами разных сегментов и под разные задачи — плановое ТО, ремонт, апгрейды, поставка запчастей и кастом-проекты. Пришлите модель, год и запрос в WhatsApp — подтвердим.",
    "faq.q2":"Можно обратиться только за запчастями?","faq.a2":"Да. Мы поставляем OEM и афтермаркет-запчасти, расходники, аксессуары и тюнинг-компоненты из ведущих международных каталогов — даже если сервис не нужен.",
    "faq.q3":"Вы делаете только кастом?","faq.a3":"Нет. Кастом-экспертиза — наш бэкграунд, но мастерская построена вокруг реального сервиса, ремонта, поставки запчастей, апгрейдов и отдельных проектов.",
    "faq.q4":"Как с вами связаться?","faq.a4":"Быстрее всего в WhatsApp на +351 917 961 230. Пришлите модель, год и описание запроса — ответим со следующим шагом.",
    "faq.q5":"Поможете с апгрейдами и тюнинг-запчастями?","faq.a5":"Да. Поставляем и устанавливаем апгрейды, аксессуары и тюнинг-запчасти из ведущих мировых каталогов. Подходим к апгрейдам как к функциональным улучшениям под конкретного райдера.",
    "faq.q6":"Нужна ли запись?","faq.a6":"На сервисные работы — да, чтобы подготовить запчасти и пост. Для быстрой консультации или запроса запчастей — просто напишите. WhatsApp — самый быстрый канал.",
    "faq.q7":"Где находится мастерская?","faq.a7":"R. António José da Silva 100 B, 2785-253 São Domingos de Rana, Cascais, Lisbon, Portugal. Вторник–суббота, 10:00–18:00.",
    "contact.eyebrow":"Свяжитесь с нами","contact.title":"Расскажите о<br/>вашем мотоцикле","contact.sub":"Сервис, запчасти, апгрейды или кастом — подскажем правильный следующий шаг. Отвечаем в рабочее время, обычно в течение часа.","contact.phone":"Телефон","contact.address":"Мастерская",
    "footer.tagline":"Премиальный мотосервис, запчасти, апгрейды и кастом-экспертиза в Кашкайше. Инженерная культура из чемпионских проектов — в каждой работе.",
    "footer.col1":"Услуги","footer.col2":"Компания","footer.col3":"Мастерская",
    "footer.hours":"Вт–Сб · 10:00–18:00<br/>Вс и Пн — выходные","footer.rights":"Все права защищены",
    "form.title":"Отправить заявку","form.sub":"Сервис, запчасти, апгрейды или кастом — расскажите, что нужно. Ответим в рабочее время.",
    "form.name":"Ваше имя","form.phone":"Телефон / WhatsApp","form.email":"Email (необязательно)","form.vehicle":"Мотоцикл (бренд · модель · год)","form.service":"Тип запроса",
    "form.opt1":"Сервис и ремонт","form.opt2":"Запчасти и расходники","form.opt3":"Апгрейды и тюнинг","form.opt4":"Кастом и спец-проект","form.opt5":"Другое / не уверен",
    "form.message":"Расскажите о работе","form.note":"Отправляя, вы соглашаетесь, что мы свяжемся с вами по данному запросу. Без спама.","form.submit":"Отправить заявку","form.successT":"Заявка получена","form.successP":"Ответим в WhatsApp или на email в рабочее время. До связи."
  },
  uk: {
    "nav.services":"Послуги","nav.brands":"Бренди","nav.harleyHub":"Harley Hub","nav.harleyService":"Сервіс","nav.harleyTuning":"Тюнінг","nav.harleyCustom":"Кастом","nav.authorizedDealer":"Офіційний дилер","nav.authorizedDealerHub":"Дилерський хаб","nav.dealerCway":"C-Way","nav.projects":"Проєкти","nav.pricing":"Ціни","nav.about":"Про нас","nav.aboutUs":"Про нас","nav.community":"Спільнота","nav.reviews":"Відгуки","nav.faq":"FAQ","nav.contact":"Контакти","nav.blog":"Блог","nav.news":"Новини","nav.allServices":"Усі послуги","nav.allProjects":"Усі проєкти","nav.preInsp":"Інспекція перед купівлею","nav.tyreServ":"Шиномонтаж і балансування","nav.expatWorkshop":"Для експатів","nav.brandHarley":"Harley-Davidson","nav.brandBmw":"BMW Motorrad","nav.brandDucati":"Ducati","nav.brandSuzuki":"Suzuki","nav.brandHonda":"Honda","nav.brandRoyalEnfield":"Royal Enfield","nav.brandTriumph":"Triumph","nav.bmwServ":"Сервіс BMW Motorrad","nav.hdServ":"Сервіс Harley-Davidson","nav.ducServ":"Сервіс Ducati","nav.suzukiServ":"Сервіс Suzuki","nav.hondaServ":"Сервіс Honda",
    "cta.bookHeader":"Записатися","cta.bookService":"Записатися на сервіс","cta.whatsapp":"Написати в WhatsApp","cta.requestForm":"Надіслати заявку",
    "wa.prefill":"Привіт, Iron Custom Motors! Хочу обговорити сервіс для свого мотоцикла. Дайте відповідь, коли зможете.","contact.directions":"Маршрут","brands.label":"Мульти-бренд сервіс · постачання OEM і aftermarket запчастин",
    "homeHarley.eyebrow":"Harley-Davidson в ICM","homeHarley.title":"Усе для вашого Harley.","homeHarley.text":"Сервіс, діагностика, тюнінг, кастом-проєкти та запчастини в одній незалежній спеціалізованій майстерні.","homeHarley.link":"Відкрити Harley Hub","homeHarley.alt":"Мотоцикли Harley-Davidson в Iron Custom Motors, Кашкайш",
    "cookie.text":"Ми використовуємо cookies, щоб розуміти відвідуваність і покращувати сайт. Без сторонньої реклами.","cookie.accept":"Прийняти","cookie.reject":"Відхилити",
    "hero.pill1":"Кашкайш · Лісабон","hero.pill2":"З 2010 року","hero.pill3":"<a href=\"/english-speaking-motorcycle-workshop/\" hreflang=\"en\">EN</a><span class=\"lang-sep\">·</span><a href=\"/ru/english-speaking-motorcycle-workshop/\" hreflang=\"ru\">RU</a><span class=\"lang-sep\">·</span><a href=\"/uk/english-speaking-motorcycle-workshop/\" hreflang=\"uk\">UA</a><span class=\"lang-sep\">·</span><a href=\"/pt/english-speaking-motorcycle-workshop/\" hreflang=\"pt\">PT</a>",
    "hero.title1":"Преміальний","hero.title2":"мотосервіс","hero.title3":"у Кашкайші","hero.title4":"",
    "hero.sub":"Діагностика, обслуговування, ремонт, оригінальні та тюнінг-запчастини, витратні матеріали, апгрейди й кастом-проекти — від команди чемпіонів світу і рекордсменів Bonneville.",
    "hero.tag1":"Чемпіони світу AMD","hero.tag2":"Рекорд Bonneville","hero.tag3":"Чемпіони BMW Motorrad 2023",
    "hero.scroll":"Прогорни · Iron Custom Motors",
    "services.learn":"Детальніше","services.eyebrow":"Що ми робимо","services.title":"Сервіс. Запчастини.<br/>Апгрейди. Кастом.","services.sub":"Iron Custom Motors обслуговує мотоцикли, постачає оригінальні і тюнінг-запчастини, витратні матеріали та аксесуари з провідних міжнародних каталогів і брендів.",
    "services.s1.title":"Сервіс і ремонт","services.s1.desc":"Діагностика, планове ТО, заміна оливи та фільтрів, гальма, підвіска, ланцюг і зірки, шиномонтаж, електрика і загальний ремонт.","services.cta":"Записатися",
    "services.s2.title":"Запчастини та витратники","services.s2.desc":"OEM, афтермаркет та тюнінг-запчастини. Витратні матеріали та аксесуари з провідних міжнародних каталогів — навіть якщо вам не потрібен наш сервіс.","services.cta2":"Замовити запчастини",
    "services.s3.title":"Апгрейди та тюнінг","services.s3.desc":"Продуктивність, підвіска, гальма, вихлоп, світло, захист, тур-обвіс і кофри. Функціональні апгрейди під ваш стиль їзди.","services.cta3":"Дізнатися про апгрейди",
    "services.s4.title":"Кастом і спецпроекти","services.s4.desc":"Кастом-консультації, індивідуальні збірки, інженерні рішення та планування проекту. Та сама команда, що будувала чемпіонів світу — для вашого мотоцикла.","services.cta4":"Обговорити проект",
    "services.s5.title":"Шиномонтаж і балансування","services.s5.desc":"Профільний мотоциклетний шиномонтаж і балансування коліс до 30 дюймів і 400 мм, зокрема спиці, вінтаж, Harley fat і кастом.","services.cta5":"Шиномонтаж",
    "services.s6.title":"Інспекція перед купівлею","services.s6.desc":"Незалежна експертна перевірка перед купівлею б/в мотоцикла в Португалії. Механіка, електрика, рама та прихований знос — письмовий звіт із фото протягом 24 годин.","services.cta6":"Деталі інспекції",
    "pricing.eyebrow":"Прайс-лист · 2025","pricing.title":"Прозорі ціни,<br/>без сюрпризів.","pricing.sub":"Письмовий кошторис до початку робіт. Фіксовані ціни або «від» на кожну послугу. Усі податки включено. Повний прайс 2025 року покриває діагностику, планове ТО, гальма, клапани, колеса, аксесуари, тюнінг і сезонну підготовку.","pricing.p1.title":"Діагностика перед купівлею","pricing.p1.desc":"Повна технічна перевірка перед купівлею б/в мотоцикла в Португалії.","pricing.p1.price":"150","pricing.p1.cur":"EUR","pricing.p2.title":"Планове ТО","pricing.p2.desc":"Обслуговування за нормативами виробника. Витратні матеріали включено в ціну.","pricing.p2.price":"150","pricing.p2.cur":"EUR","pricing.p2.from":"від","pricing.p3.title":"Діагностика несправностей","pricing.p3.desc":"Шукаємо причину, а не симптом. Електрика, двигун, ходова частина.","pricing.p3.price":"50–350","pricing.p3.cur":"EUR","pricing.p4.title":"Погодинна робота","pricing.p4.desc":"Усе, що не увійшло до прайсу — прозорий облік часу, кошторис наперед.","pricing.p4.price":"50","pricing.p4.cur":"EUR / год","pricing.cta":"Переглянути повний прайс","pricing.tax":"Усі ціни включають податки та збори",
    "why.eyebrow":"Чому Iron Custom Motors","why.title":"Чемпіонська майстерня,<br/>сервіс щодня","why.sub":"Команда світового рівня, яка справді бере слухавку, коли мотоцикл не заводиться. Цей розрив ми й закриваємо.",
    "why.r1.t":"Інжиніринг світового рівня","why.r1.d":"Чемпіони світу AMD. Рекордсмени Bonneville. Чемпіони BMW Motorrad 2023. Ця експертиза стоїть за кожним рутинним сервісом.",
    "why.r2.t":"Запчастини під одним дахом","why.r2.d":"OEM, неоригінал, тюнінг і витратники з провідних міжнародних каталогів — один контакт для сервісу і запчастин.",
    "why.r3.t":"Сервіс вашою мовою","why.r3.d":"Англійська, російська, українська, португальська. Чітка комунікація, письмові кошториси, чесні строки.",
    "why.r4.t":"Прозорий процес","why.r4.d":"Спочатку діагностика, потім кошторис. Фото і апдейти під час робіт. Жодних сюрпризів у рахунку.",
    "why.r5.t":"Беремося за складне","why.r5.d":"Заплутана електрика, виготовлення кастом-деталей, проблеми фітменту, втрачені специфікації — те, від чого відмовляються інші.",
    "why.r6.t":"Повага до техніки","why.r6.d":"Чиста майстерня. Моменти затяжки. Оригінальні або преміум-запчастини. Так, як обслуговували б свій мотоцикл — бо ми це й робимо.",
    "why.badge":"років будуємо, гонимо, лагодимо",
    "community.stripTitle":"<span class=\"accent\">Inspirium</span> · рекордсмен Bonneville, на експозиції.","exterior.title":"Заїжджайте. <span class=\"accent\">Ми тут.</span>","teamBanner.title":"Команда, що <span class=\"accent\">бере слухавку.</span>","teamBanner.sub":"Інженери світового рівня за кожним рутинним сервісом. Ті самі руки. Той самий стандарт. Тепер у Кашкайші.","teamBanner.row1":"<strong>15+</strong> років будуємо, гонимо, лагодимо","teamBanner.row2":"<strong>3×</strong> чемпіони світу","teamBanner.row3":"Кашкайш · Лісабон · Португалія","story.eyebrow":"Наша історія","story.title":"Від майстерні в Харкові<br/>до подіумів світових<br/>чемпіонатів",
    "story.p1":"Iron Custom Motors засновано у 2010 році з однією метою — будувати мотоцикли, які зможуть вийти на світову сцену. Через шість років ми це зробили: чемпіони світу AMD у класі café racer з проектом Beckman.",
    "story.p2":"У 2017 команда встановила світовий рекорд швидкості на солончаку Bonneville на Inspirium 350APS-VG. У 2023 — чемпіони BMW Motorrad Customizing. Проекти на провідних мотовиставках світу.",
    "story.p3":"У 2025 ми привезли майстерню до Кашкайша, Великий Лісабон. Та сама команда, та сама інженерна культура — тепер у пішій доступності для кожного райдера на узбережжі Португалії.",
    "story.quote":"«Ті самі руки, що будували чемпіонів світу, тепер тримають у формі ваш мотоцикл щодня.»",
    "story.stat1l":"Заснування","story.stat1s":"15 років безперервної роботи","story.stat2l":"Чемпіонств світу","story.stat2s":"AMD · BMW Motorrad · Bonneville","story.stat3l":"Реалізованих проектів","story.stat3s":"Сервіс · кастом · інжиніринг","story.stat4l":"Брендів у роботі","story.stat4s":"Від BMW до індивідуальних збірок",
    "community.eyebrow":"Lounge і Спільнота","community.title":"Більше, ніж сервіс.<br/>Місце для райдерів, історій<br/>і мотокультури.","community.sub":"Lounge-зона Iron Custom Motors — це бренд офлайн: чемпіонські мотоцикли, трофеї, розмови і кава. Заїжджайте, навіть якщо з мотоциклом усе гаразд.",
    "community.heroTitle":"Lounge на <em>справжніх</em> історіях.","community.heroSub":"Inspirium з солончаку Bonneville, чемпіонські трофеї, гоночна екіпіровка і racing-атрибутика. Тут майстерня стає брендом.","community.heroBadge":"Кашкайш · Вт–Сб","community.ctaVisit":"Спланувати візит",
    "community.introTitle":"Не лише майстерня.","community.introP1":"Lounge — частина того, що робить Iron Custom Motors собою. Дерев'яні стіни, чемпіонські мотоцикли на підлозі, гоночні костюми на стінах, трофеї Bonneville, шоломи, книги, журнали, гоночні маски.","community.introP2":"Це місце, де можна почекати, поки обслуговують ваш мотоцикл — але головне, сюди можна заїхати просто так. Випити кави. Подивитися на Inspirium зблизька. Поговорити з людьми, які на ньому їхали.","community.introP3":"Без пафосу, без членства, без дрес-коду. Якщо ви їздите або любите мотоцикли — вам сюди.",
    "community.findTitle":"Що ви тут знайдете","community.f1.t":"Чемпіонські машини","community.f1.d":"Рекордсмен Bonneville Inspirium на постаменті, а також інші кастом-збірки.","community.f2.t":"Трофеї і гоночні артефакти","community.f2.d":"AMD World Championship, Bonneville Speed Week, BMW Motorrad — оригінальна атрибутика.","community.f3.t":"Кава і спілкування","community.f3.d":"Заїжджайте, сідайте, говоримо про мотоцикли. Вівторок–субота в робочі години.","community.f4.t":"Книги, журнали, екіпіровка","community.f4.d":"Гоночні костюми, шоломи, маски, книги і ретельно дібрана мотоатрибутика.","community.f5.t":"Місце бути райдером","community.f5.d":"Спільні виїзди, презентації проектів, тематичні вечори, зустрічі райдерів — будуємо локальну сцену.",
    "community.promiseTitle":"Завжди можна заїхати, випити кави, поговорити про мотоцикли і провести час з <span class=\"em\">правильними людьми.</span>","community.promiseSub":"Навіть без запису, навіть без сервісної задачі — двері відчинені. Саме такої атмосфери ми й прагнемо.",
    "projects.p1.label":"Світовий рекорд · Bonneville 2017","projects.p1.title":"Inspirium","projects.p1.desc":"Мотоцикл — світовий рекорд швидкості. Клас 350APS-VG, солончак Бонневілль. Вінтажна платформа ІЖ-49 1953.","projects.p2.label":"Чемпіон світу AMD · 2016","projects.p2.title":"Beckman","projects.p2.desc":"Чемпіон світу café racer. Трициліндровий двигун ручної роботи. Переможець AMD World Championship 2016.","projects.p3.label":"Переможець BMW Motorrad Customizing","projects.p3.title":"Unbreakable","projects.p3.desc":"Переможець BMW Motorrad Customizing Championship. Експонувався у BMW Motorrad Welt.","projects.p4.label":"Концепт Geneva · Goodwood","projects.p4.title":"Quanta R","projects.p4.desc":"Концепт для Geneva Motor Show та Goodwood. AWD, турбобоксер 2.5L до 600 к.с., алюмінієвий кузов ручної роботи.","projects.p5.label":"BMW R 18 кастом-драгстер","projects.p5.title":"Burly","projects.p5.desc":"BMW R 18, що переродився як кастом-драгстер. Основа для лінійки carbon, вихлопу та стайлінг-комплектів.","projects.p6.label":"Café Racer · 2-ге місце Ericeira 2026","projects.p6.title":"Sturmvogel","projects.p6.desc":"Sturmvogel додав до своєї історії новий португальський результат: 2-ге місце в категорії Café Racer на Ericeira Kustom Fest 2026.","projects.p7.label":"Ретро-футуризм · AMD 2018","projects.p7.title":"Geometric","projects.p7.desc":"Ретро-футуристична збірка. AMD World Championship 2018, перше у світі спицьоване безступичне переднє колесо.","projects.p8.label":"Кастом Harley-Davidson Dyna","projects.p8.title":"Joker","projects.p8.desc":"Harley-Davidson Dyna Street Bob з агресивною міською посадкою, преміум-компонентами та поп-арт фарбуванням.","projects.p9.label":"Best Paint · переможець Ericeira 2026","projects.p9.title":"Hell Boy","projects.p9.desc":"Hell Boy посів 1-ше місце в Best Paint на Ericeira Kustom Fest 2026, підтвердивши силу своєї театральної аерографії.","projects.p10.label":"Американський кастом · Дух Harley","projects.p10.title":"True Religion","projects.p10.desc":"Побудований навколо свободи, характеру та позачасового духу американської кастом-культури.","projects.eyebrow":"Обрані проекти","projects.title":"Кілька мотоциклів,<br/>якими ми пишаємось","projects.sub":"Переможні збірки, що вивели нас на міжнародну мапу. Той самий інжиніринг іде в кожен сервіс.",
    
    
    
    
    "process.eyebrow":"Як ми працюємо","process.title":"Від заявки до виїзду —<br/>п'ять кроків, без сюрпризів",
    "process.s1t":"Заявка","process.s1d":"WhatsApp, форма або дзвінок. Розкажіть, що у вас за мотоцикл і що не так.",
    "process.s2t":"Діагностика","process.s2d":"Оглядаємо, проводимо діагностику й шукаємо причину — не симптом.",
    "process.s3t":"Кошторис","process.s3d":"Письмовий кошторис, перелік запчастин, строки. Узгоджуємо до початку робіт.",
    "process.s4t":"Робота","process.s4d":"Сервіс або збірка, з фото-апдейтами. Моменти затяжки, чисте встановлення, без зрізань кутів.",
    "process.s5t":"Видача","process.s5d":"Тест, передача, follow-up. Ми поруч і для наступного сервісу.",
    "reviews.basedOn":"На основі","reviews.gReviews":"відгуків у Google","reviews.viewAll":"Усі відгуки в Google →","reviews.leaveReview":"Залишити відгук у Google","reviews.eyebrow":"Що кажуть райдери","reviews.title":"Довіряють райдери та<br/>білдери по всьому світу",
    "reviews.r1.text":"«Привіз свій BMW R nineT з упертою електрикою, яку три інші сервіси не змогли вирішити. Iron Custom розібрався менш ніж за годину і пояснив усе простою мовою. Чесні ціни, світовий рівень.»","reviews.r1.role":"BMW R nineT · експат з UK у Кашкайші",
    "reviews.r2.text":"«Передкупівельна інспекція врятувала мені 4 200 €. Мотоцикл виглядав ідеально, але хлопці знайшли приховану проблему з рамою. Надіслали детальний звіт із фото того ж дня. Ось як має працювати.»","reviews.r2.role":"Покупець Ducati Monster · Лісабон",
    "reviews.r3.text":"«Нарешті сервіс у Португалії, який ставиться до Harley як до Harley. Кастомний вихлоп, налаштування підвіски і тюнінг — мотоцикл як новий. Говорять російською, все простіше.»","reviews.r3.role":"Harley-Davidson FXDR · Ешторил",
    "faq.eyebrow":"Часті питання","faq.title":"Відповіді до того,<br/>як ви запитаєте","faq.sub":"Немає вашого питання? Напишіть у WhatsApp — зазвичай відповідаємо протягом години в робочий час.","faq.cta":"Запитати в WhatsApp",
    "faq.q1":"З якими мотоциклами ви працюєте?","faq.a1":"Працюємо з мотоциклами різних сегментів і під різні задачі — планове ТО, ремонт, апгрейди, постачання запчастин і кастом-проекти. Надішліть модель, рік і запит у WhatsApp — підтвердимо.",
    "faq.q2":"Чи можна звернутися лише за запчастинами?","faq.a2":"Так. Постачаємо OEM та афтермаркет-запчастини, витратні матеріали, аксесуари і тюнінг-компоненти з провідних міжнародних каталогів — навіть якщо сервіс не потрібен.",
    "faq.q3":"Ви робите тільки кастом?","faq.a3":"Ні. Кастом-експертиза — наш бекграунд, але майстерня побудована навколо реального сервісу, ремонту, постачання запчастин, апгрейдів і окремих проектів.",
    "faq.q4":"Як з вами зв'язатися?","faq.a4":"Найшвидше в WhatsApp на +351 917 961 230. Надішліть модель, рік і опис запиту — відповімо з наступним кроком.",
    "faq.q5":"Допоможете з апгрейдами і тюнінг-запчастинами?","faq.a5":"Так. Постачаємо і встановлюємо апгрейди, аксесуари та тюнінг-запчастини з провідних світових каталогів. Підходимо до апгрейдів як до функціональних покращень під конкретного райдера.",
    "faq.q6":"Чи потрібен запис?","faq.a6":"На сервісні роботи — так, щоб підготувати запчастини і пост. Для швидкої консультації або запиту запчастин — просто напишіть. WhatsApp — найшвидший канал.",
    "faq.q7":"Де знаходиться майстерня?","faq.a7":"R. António José da Silva 100 B, 2785-253 São Domingos de Rana, Cascais, Lisbon, Portugal. Вівторок–субота, 10:00–18:00.",
    "contact.eyebrow":"Зв'яжіться з нами","contact.title":"Розкажіть про<br/>ваш мотоцикл","contact.sub":"Сервіс, запчастини, апгрейди або кастом — підкажемо правильний наступний крок. Відповідаємо в робочий час, зазвичай протягом години.","contact.phone":"Телефон","contact.address":"Майстерня",
    "footer.tagline":"Преміальний мотосервіс, запчастини, апгрейди й кастом-експертиза у Кашкайші. Інженерна культура з чемпіонських проектів — у кожній роботі.",
    "footer.col1":"Послуги","footer.col2":"Компанія","footer.col3":"Майстерня",
    "footer.hours":"Вт–Сб · 10:00–18:00<br/>Нд та Пн — вихідні","footer.rights":"Усі права захищені",
    "form.title":"Надіслати заявку","form.sub":"Сервіс, запчастини, апгрейди або кастом — розкажіть, що потрібно. Відповімо в робочий час.",
    "form.name":"Ваше ім'я","form.phone":"Телефон / WhatsApp","form.email":"Email (необов'язково)","form.vehicle":"Мотоцикл (бренд · модель · рік)","form.service":"Тип запиту",
    "form.opt1":"Сервіс і ремонт","form.opt2":"Запчастини та витратники","form.opt3":"Апгрейди і тюнінг","form.opt4":"Кастом і спецпроект","form.opt5":"Інше / не впевнений",
    "form.message":"Розкажіть про роботу","form.note":"Надсилаючи, ви погоджуєтесь, що ми зв'яжемося з вами щодо цього запиту. Жодного спаму.","form.submit":"Надіслати заявку","form.successT":"Заявку отримано","form.successP":"Відповімо у WhatsApp або на email у робочий час. До зв'язку."
  },
  pt: {
    "nav.services":"Serviços","nav.brands":"Marcas","nav.harleyHub":"Harley Hub","nav.harleyService":"Serviço","nav.harleyTuning":"Tuning","nav.harleyCustom":"Custom","nav.authorizedDealer":"Revendedor Oficial","nav.authorizedDealerHub":"Hub revendedor","nav.dealerCway":"C-Way","nav.projects":"Projetos","nav.pricing":"Preços","nav.about":"Sobre","nav.aboutUs":"Sobre nós","nav.community":"Comunidade","nav.reviews":"Avaliações","nav.faq":"FAQ","nav.contact":"Contacto","nav.blog":"Blog","nav.news":"Notícias","nav.allServices":"Todos os serviços","nav.allProjects":"Todos os projetos","nav.preInsp":"Inspeção pré-compra","nav.tyreServ":"Pneus e equilibragem","nav.expatWorkshop":"Para expatriados","nav.brandHarley":"Harley-Davidson","nav.brandBmw":"BMW Motorrad","nav.brandDucati":"Ducati","nav.brandSuzuki":"Suzuki","nav.brandHonda":"Honda","nav.brandRoyalEnfield":"Royal Enfield","nav.brandTriumph":"Triumph","nav.bmwServ":"Serviço BMW Motorrad","nav.hdServ":"Serviço Harley-Davidson","nav.ducServ":"Serviço Ducati","nav.suzukiServ":"Serviço Suzuki","nav.hondaServ":"Serviço Honda",
    "cta.bookHeader":"Marcar serviço","cta.bookService":"Marcar serviço","cta.whatsapp":"WhatsApp","cta.requestForm":"Enviar pedido",
    "wa.prefill":"Olá Iron Custom Motors, gostaria de saber sobre o serviço para a minha moto. Respondam quando puderem.","contact.directions":"Como chegar","brands.label":"Oficina multi-marca · sourcing de peças OEM e aftermarket",
    "homeHarley.eyebrow":"Harley-Davidson na ICM","homeHarley.title":"Tudo para a sua Harley.","homeHarley.text":"Serviço, diagnóstico, tuning, projetos custom e peças numa oficina especialista independente.","homeHarley.link":"Abrir o Harley Hub","homeHarley.alt":"Motas Harley-Davidson na Iron Custom Motors, Cascais",
    "cookie.text":"Usamos cookies para medir tráfego e melhorar o site. Sem publicidade de terceiros.","cookie.accept":"Aceitar","cookie.reject":"Rejeitar",
    "hero.pill1":"Cascais · Grande Lisboa","hero.pill2":"Desde 2010","hero.pill3":"<a href=\"/english-speaking-motorcycle-workshop/\" hreflang=\"en\">EN</a><span class=\"lang-sep\">·</span><a href=\"/ru/english-speaking-motorcycle-workshop/\" hreflang=\"ru\">RU</a><span class=\"lang-sep\">·</span><a href=\"/uk/english-speaking-motorcycle-workshop/\" hreflang=\"uk\">UA</a><span class=\"lang-sep\">·</span><a href=\"/pt/english-speaking-motorcycle-workshop/\" hreflang=\"pt\">PT</a>",
    "hero.title1":"Serviço","hero.title2":"premium de moto","hero.title3":"em Cascais","hero.title4":"",
    "hero.sub":"Diagnóstico, manutenção, reparação, peças e consumíveis, soluções de tuning e projetos custom — pela equipa por trás de construções campeãs do mundo e de um recorde em Bonneville.",
    "hero.tag1":"Campeões do mundo AMD","hero.tag2":"Recorde Bonneville","hero.tag3":"BMW Motorrad Champ. 2023",
    "hero.scroll":"Scroll · Iron Custom Motors",
    "services.learn":"Saber mais","services.eyebrow":"O que fazemos","services.title":"Serviço. Peças.<br/>Upgrades. Custom.","services.sub":"Iron Custom Motors faz serviço a motos, fornece peças e consumíveis, e oferece soluções de tuning e upgrade dos principais catálogos e marcas internacionais.",
    "services.s1.title":"Serviço e reparação","services.s1.desc":"Diagnóstico, manutenção programada, óleo e filtros, travões, suspensão, corrente e cremalheira, pneus, eletricidade e reparação geral.","services.cta":"Marcar serviço",
    "services.s2.title":"Peças e consumíveis","services.s2.desc":"Peças OEM, aftermarket e tuning. Consumíveis e acessórios obtidos através dos principais catálogos internacionais — mesmo sem precisar do nosso workshop.","services.cta2":"Pedir peças",
    "services.s3.title":"Upgrades e tuning","services.s3.desc":"Performance, suspensão, travões, escape, iluminação, proteção, touring e bagagem. Upgrades funcionais escolhidos para o seu estilo de condução.","services.cta3":"Sobre upgrades",
    "services.s4.title":"Custom e projetos especiais","services.s4.desc":"Consultoria custom, builds bespoke, soluções de engenharia e planeamento de projetos. A equipa que entregou motos campeãs do mundo é a que constrói a sua.","services.cta4":"Discutir projeto",
    "services.s5.title":"Pneus e equilibragem","services.s5.desc":"Montagem de pneus de mota e equilibragem em equipamento dedicado para rodas até 30 polegadas e 400 mm, incluindo raios, clássicas, Harley fat e custom.","services.cta5":"Serviço de pneus",
    "services.s6.title":"Inspeção pré-compra","services.s6.desc":"Verificação técnica independente antes de comprar uma mota usada em Portugal. Mecânica, elétrica, quadro e desgaste oculto — relatório escrito com fotos em 24 horas.","services.cta6":"Detalhes da inspeção",
    "pricing.eyebrow":"Tabela de preços · 2025","pricing.title":"Preços transparentes,<br/>sem surpresas.","pricing.sub":"Orçamento escrito antes do início dos trabalhos. Preços fixos ou \"desde\" para cada serviço. Todos os impostos incluídos. A tabela completa de 2025 cobre diagnóstico, manutenção programada, travões, válvulas, rodas, acessórios, afinação e preparação sazonal.","pricing.p1.title":"Inspeção pré-compra","pricing.p1.desc":"Verificação técnica completa antes de comprar uma moto usada em Portugal.","pricing.p1.price":"150","pricing.p1.cur":"EUR","pricing.p2.title":"Manutenção programada","pricing.p2.desc":"Manutenção segundo normas do fabricante. Consumíveis incluídos no preço.","pricing.p2.price":"150","pricing.p2.cur":"EUR","pricing.p2.from":"desde","pricing.p3.title":"Diagnóstico de avarias","pricing.p3.desc":"Procuramos a causa, não o sintoma. Elétrica, motor, chassis.","pricing.p3.price":"50–350","pricing.p3.cur":"EUR","pricing.p4.title":"Trabalho à hora","pricing.p4.desc":"Tudo o que não está na tabela — registo transparente do tempo, orçamento prévio.","pricing.p4.price":"50","pricing.p4.cur":"EUR / hora","pricing.cta":"Ver tabela completa","pricing.tax":"Todos os preços incluem impostos e taxas",
    "why.eyebrow":"Porquê Iron Custom Motors","why.title":"Workshop de nível campeonato,<br/>serviço de todos os dias","why.sub":"Uma equipa custom de classe mundial que atende o telefone quando a sua moto não pega. É essa lacuna que fechamos.",
    "why.r1.t":"Engenharia de classe mundial","why.r1.d":"Campeões do Mundo AMD. Detentores de recorde em Bonneville. Campeões BMW Motorrad Customizing 2023. A expertise por trás do seu serviço de rotina.",
    "why.r2.t":"Peças sourcing in-house","why.r2.d":"OEM, aftermarket, tuning e consumíveis dos principais catálogos internacionais — um único ponto de contacto para serviço e peças.",
    "why.r3.t":"Serviço na sua língua","why.r3.d":"Inglês, russo, ucraniano e português. Comunicação clara, orçamentos por escrito, prazos honestos.",
    "why.r4.t":"Processo transparente","why.r4.d":"Diagnóstico primeiro, depois orçamento. Fotos e atualizações durante o trabalho. Sem surpresas na fatura.",
    "why.r5.t":"Trabalhos complexos bem-vindos","why.r5.d":"Pesadelos elétricos, fabricação de peças custom, problemas de fitment, especificações perdidas — o trabalho que outros recusam.",
    "why.r6.t":"Tratar a máquina bem","why.r6.d":"Espaço limpo. Binários certos. Peças originais ou premium. Como faríamos à nossa própria moto — porque o fazemos.",
    "why.badge":"anos a construir, correr, reparar",
    "community.stripTitle":"A <span class=\"accent\">Inspirium</span> · detentora do recorde de Bonneville, em exposição.","exterior.title":"Apareça. <span class=\"accent\">Estamos cá.</span>","teamBanner.title":"A equipa que <span class=\"accent\">atende o telefone.</span>","teamBanner.sub":"Engenheiros campeões do mundo por trás de cada serviço de rotina. As mesmas mãos. O mesmo padrão. Agora em Cascais.","teamBanner.row1":"<strong>15+</strong> anos a construir, correr, reparar","teamBanner.row2":"<strong>3×</strong> campeões do mundo","teamBanner.row3":"Cascais · Lisboa · Portugal","story.eyebrow":"A nossa história","story.title":"De um workshop em Kharkiv<br/>aos pódios dos campeonatos<br/>mundiais",
    "story.p1":"Iron Custom Motors foi fundada em 2010 com um único objetivo — construir motos capazes de competir no palco mundial. Seis anos depois conseguimos: campeões do mundo AMD, classe café racer, com o projeto Beckman.",
    "story.p2":"Em 2017 a equipa estabeleceu um recorde mundial de velocidade nas Bonneville Salt Flats com a Inspirium 350APS-VG. Em 2023 — campeões BMW Motorrad Customizing. Projetos apresentados nos maiores eventos do mundo.",
    "story.p3":"Em 2025 trouxemos o workshop para Cascais, Grande Lisboa. A mesma equipa, a mesma cultura de engenharia, agora ao alcance de qualquer rider na costa portuguesa.",
    "story.quote":"«As mesmas mãos que construíram motos campeãs do mundo agora mantêm a sua a rolar todos os dias.»",
    "story.stat1l":"Fundada","story.stat1s":"15 anos de craft contínuo","story.stat2l":"Campeonatos do mundo","story.stat2s":"AMD · BMW Motorrad · Bonneville","story.stat3l":"Projetos entregues","story.stat3s":"Serviço · custom · engenharia","story.stat4l":"Marcas servidas","story.stat4s":"De BMW a builds únicos",
    "community.eyebrow":"Lounge e Comunidade","community.title":"Mais do que um serviço.<br/>Um lugar para riders, histórias<br/>e cultura motociclista.","community.sub":"O lounge da Iron Custom Motors é onde a marca vive offline — motas campeãs, troféus, conversas e café. Apareça mesmo que a sua moto esteja em ordem.",
    "community.heroTitle":"Um lounge construído sobre histórias <em>reais</em>.","community.heroSub":"A Inspirium de Bonneville, troféus de campeonato, fato de corrida e memorabilia. Aqui a oficina torna-se uma marca.","community.heroBadge":"Cascais · Aberto Ter–Sáb","community.ctaVisit":"Planear a visita",
    "community.introTitle":"Para além da oficina.","community.introP1":"O lounge é parte do que faz a Iron Custom Motors ser ela mesma. Paredes em madeira, motos campeãs no chão, fatos de corrida nas paredes, troféus de Bonneville, capacetes, livros, revistas, máscaras de pilotagem.","community.introP2":"É um sítio para esperar enquanto a sua moto é servida — mas, mais importante, é um sítio para passar mesmo sem precisar de nada. Tomar um café. Ver a Inspirium de perto. Falar com as pessoas que a guiaram.","community.introP3":"Sem pretensão, sem inscrição, sem dress code. Se anda de moto ou ama motas — é bem-vindo.",
    "community.findTitle":"O que vai encontrar aqui","community.f1.t":"Máquinas campeãs","community.f1.d":"Inspirium recordista de Bonneville em exposição, mais outros builds custom.","community.f2.t":"Troféus e artefactos de corrida","community.f2.d":"AMD World Championship, Bonneville Speed Week, BMW Motorrad — o hardware real.","community.f3.t":"Café e conversa","community.f3.d":"Apareça, sente-se, falemos de motas. De terça a sábado durante o horário da oficina.","community.f4.t":"Livros, revistas, equipamento","community.f4.d":"Fatos de corrida, capacetes, máscaras, livros e memorabilia de motociclismo.","community.f5.t":"Um sítio para ser rider","community.f5.d":"Saídas em grupo, apresentações de projetos, noites temáticas, encontros — a construir a cena local.",
    "community.promiseTitle":"É sempre bem-vindo a aparecer, tomar um café, falar de motas e passar tempo com <span class=\"em\">pessoas que percebem.</span>","community.promiseSub":"Sem marcação, sem pedido de serviço — a porta está aberta. É assim que queremos que este sítio se sinta.",
    "projects.p1.label":"Recorde Mundial · Bonneville 2017","projects.p1.title":"Inspirium","projects.p1.desc":"Moto recorde mundial de velocidade. Classe 350APS-VG, Bonneville Salt Flats. Plataforma vintage IZH-49 de 1953.","projects.p2.label":"Campeão Mundial AMD · 2016","projects.p2.title":"Beckman","projects.p2.desc":"Café racer campeão do mundo. Motor de três cilindros feito à mão. Vencedor do AMD World Championship 2016.","projects.p3.label":"Vencedor BMW Motorrad Customizing","projects.p3.title":"Unbreakable","projects.p3.desc":"Vencedor do BMW Motorrad Customizing Championship. Exibido no BMW Motorrad Welt.","projects.p4.label":"Conceito Geneva · Goodwood","projects.p4.title":"Quanta R","projects.p4.desc":"Conceito para Geneva Motor Show e Goodwood. AWD, boxer turbo 2.5L até 600 cv, carroçaria de alumínio feita à mão.","projects.p5.label":"Custom Dragster BMW R 18","projects.p5.title":"Burly","projects.p5.desc":"BMW R 18 renascida como custom dragster. Base para uma linha completa de kits de carbono, escape e estilo.","projects.p6.label":"Café Racer · 2.º lugar Ericeira 2026","projects.p6.title":"Sturmvogel","projects.p6.desc":"A Sturmvogel juntou um novo resultado português à sua história: 2.º lugar na categoria Café Racer no Ericeira Kustom Fest 2026.","projects.p7.label":"Retro-Futurista · AMD 2018","projects.p7.title":"Geometric","projects.p7.desc":"Construção retro-futurista. AMD World Championship 2018, primeira roda dianteira sem cubo com raios do mundo.","projects.p8.label":"Custom Harley-Davidson Dyna","projects.p8.title":"Joker","projects.p8.desc":"Harley-Davidson Dyna Street Bob com postura urbana arrojada, componentes premium e pintura pop-art.","projects.p9.label":"Vencedor Best Paint · Ericeira 2026","projects.p9.title":"Hell Boy","projects.p9.desc":"O Hell Boy ganhou o 1.º lugar em Best Paint no Ericeira Kustom Fest 2026, confirmando a força da sua aerografia teatral.","projects.p10.label":"Custom Americano · Espírito Harley","projects.p10.title":"True Religion","projects.p10.desc":"Construído em torno da liberdade, atitude e do espírito intemporal da cultura custom americana.","projects.eyebrow":"Projetos selecionados","projects.title":"Algumas das motas<br/>de que nos orgulhamos","projects.sub":"Builds premiadas que nos colocaram no mapa internacional. A mesma engenharia entra em cada serviço.",
    
    
    
    
    "process.eyebrow":"Como funciona","process.title":"Do pedido à estrada —<br/>cinco passos, sem surpresas",
    "process.s1t":"Pedido","process.s1d":"WhatsApp, formulário ou chamada. Diga-nos o que conduz e o que se passa.",
    "process.s2t":"Diagnóstico","process.s2d":"Inspecionamos, fazemos diagnóstico e identificamos a causa real — não apenas o sintoma.",
    "process.s3t":"Orçamento","process.s3d":"Orçamento por escrito, lista de peças, prazos. Aprova antes de levantarmos uma chave.",
    "process.s4t":"Trabalho","process.s4d":"Serviço ou build, com atualizações em foto. Binários certos, instalação limpa, sem atalhos.",
    "process.s5t":"Volta à estrada","process.s5d":"Teste, entrega, follow-up. Estamos cá para o próximo serviço também.",
    "reviews.basedOn":"Com base em","reviews.gReviews":"avaliações Google","reviews.viewAll":"Ver todas no Google →","reviews.leaveReview":"Deixar avaliação no Google","reviews.eyebrow":"O que dizem os riders","reviews.title":"Confiança de riders<br/>e builders no mundo todo",
    "reviews.r1.text":"«Levei a minha BMW R nineT com um problema elétrico que três outros workshops não conseguiram resolver. Iron Custom diagnosticou em menos de uma hora e explicou em português claro. Preço honesto, qualidade mundial.»","reviews.r1.role":"BMW R nineT · expat UK em Cascais",
    "reviews.r2.text":"«A inspeção pré-compra poupou-me 4 200 €. A moto parecia perfeita — encontraram um problema oculto no chassi. Enviaram relatório detalhado com fotos no mesmo dia. É assim que deve ser.»","reviews.r2.role":"Comprador Ducati Monster · Lisboa",
    "reviews.r3.text":"«Finalmente um workshop em Portugal que trata uma Harley como uma Harley. Escape custom, suspensão e sessão de tuning — moto como nova. Falam russo, o que tornou tudo mais fácil.»","reviews.r3.role":"Harley-Davidson FXDR · Estoril",
    "faq.eyebrow":"Perguntas frequentes","faq.title":"Respostas antes<br/>de perguntar","faq.sub":"Não vê a sua pergunta? Mande-nos WhatsApp — costumamos responder em uma hora durante o horário de trabalho.","faq.cta":"Perguntar no WhatsApp",
    "faq.q1":"Que tipo de motos trabalham?","faq.a1":"Trabalhamos com motos em diferentes segmentos e pedidos — manutenção de rotina, reparações, upgrades, fornecimento de peças e custom selecionado. Envie modelo, ano e pedido via WhatsApp e confirmamos.",
    "faq.q2":"Posso contactar só para peças?","faq.a2":"Sim. Fornecemos peças, consumíveis, acessórios e soluções de tuning através dos principais catálogos internacionais — mesmo sem precisar do nosso workshop.",
    "faq.q3":"Só fazem custom?","faq.a3":"Não. A expertise custom faz parte do nosso background, mas o workshop está construído em torno de serviço real, reparação, fornecimento de peças, upgrades e projetos selecionados.",
    "faq.q4":"Como vos contacto?","faq.a4":"Mais rápido por WhatsApp em +351 917 961 230. Envie modelo, ano e pedido — respondemos com o próximo passo.",
    "faq.q5":"Ajudam com upgrades e peças de tuning?","faq.a5":"Sim. Fornecemos e instalamos upgrades, acessórios e peças de tuning dos principais catálogos. Tratamos upgrades como melhorias funcionais específicas do rider.",
    "faq.q6":"Preciso de marcação?","faq.a6":"Para serviço — sim, permite preparar peças e o posto. Para conselho rápido ou pedidos de peças — basta enviar mensagem. WhatsApp é o canal mais rápido.",
    "faq.q7":"Onde fica o workshop?","faq.a7":"R. António José da Silva 100 B, 2785-253 São Domingos de Rana, Cascais, Lisboa, Portugal. Aberto terça a sábado, 10:00–18:00.",
    "contact.eyebrow":"Em contacto","contact.title":"Conte-nos sobre<br/>a sua máquina","contact.sub":"Serviço, peças, upgrades ou custom — indicamos o próximo passo certo. Respondemos em horário de trabalho, normalmente em uma hora.","contact.phone":"Telefone","contact.address":"Workshop",
    "footer.tagline":"Serviço premium de moto, peças, upgrades e expertise custom em Cascais. Cultura de engenharia de projetos campeões do mundo, aplicada a cada trabalho.",
    "footer.col1":"Serviços","footer.col2":"Empresa","footer.col3":"Workshop",
    "footer.hours":"Ter–Sáb · 10:00–18:00<br/>Encerrado dom &amp; seg","footer.rights":"Todos os direitos reservados",
    "form.title":"Enviar pedido","form.sub":"Serviço, peças, upgrades ou custom — diga-nos o que precisa. Voltamos em horário de trabalho.",
    "form.name":"O seu nome","form.phone":"Telefone / WhatsApp","form.email":"Email (opcional)","form.vehicle":"Moto (marca · modelo · ano)","form.service":"Tipo de pedido",
    "form.opt1":"Serviço e reparação","form.opt2":"Peças e consumíveis","form.opt3":"Upgrades e tuning","form.opt4":"Custom e projeto especial","form.opt5":"Outro / não tenho a certeza",
    "form.message":"Conte-nos sobre o trabalho","form.note":"Ao enviar concorda em ser contactado sobre este pedido. Sem spam.","form.submit":"Enviar pedido","form.successT":"Pedido recebido","form.successP":"Respondemos via WhatsApp ou email em horário de trabalho. Até já."
  }
};

/* ---------- Language switching ----------
   Each language lives at its own URL:
     /         /motorcycle-service/  /projects/inspirium/   (EN)
     /ru/      /ru/motorcycle-service/  /ru/projects/inspirium/
     /uk/      /uk/...
     /pt/      /pt/...
   Pages are pre-rendered server-side (static HTML in each language).
   JS here just (a) updates UI to reflect current lang, (b) navigates URLs
   when user picks a different language.
   ----------------------------------------------------------------- */
const SUPPORTED_LANGS = ['en','ru','uk','pt'];

function detectLangFromUrl(){
  const m = location.pathname.match(/^\/(ru|uk|pt)(\/|$)/);
  return m ? m[1] : 'en';
}

function pathWithoutLang(){
  // Returns path WITHOUT the leading language segment. Always starts with /.
  const p = location.pathname;
  const m = p.match(/^\/(ru|uk|pt)(\/.*)?$/);
  return m ? (m[2] || '/') : p;
}

const LOCALIZED_PAGE_PATHS = {
  '/motorcycle-tyre-service/': {
    en: '/motorcycle-tyre-service/',
    ru: '/ru/shinomontazh-mototsiklov/',
    uk: '/uk/shynomontazh-mototsykliv/',
    pt: '/pt/montagem-de-pneus-mota/'
  },
  '/shinomontazh-mototsiklov/': {
    en: '/motorcycle-tyre-service/',
    ru: '/ru/shinomontazh-mototsiklov/',
    uk: '/uk/shynomontazh-mototsykliv/',
    pt: '/pt/montagem-de-pneus-mota/'
  },
  '/shynomontazh-mototsykliv/': {
    en: '/motorcycle-tyre-service/',
    ru: '/ru/shinomontazh-mototsiklov/',
    uk: '/uk/shynomontazh-mototsykliv/',
    pt: '/pt/montagem-de-pneus-mota/'
  },
  '/montagem-de-pneus-mota/': {
    en: '/motorcycle-tyre-service/',
    ru: '/ru/shinomontazh-mototsiklov/',
    uk: '/uk/shynomontazh-mototsykliv/',
    pt: '/pt/montagem-de-pneus-mota/'
  }
};

function urlForLang(lang){
  const rest = pathWithoutLang();
  const mapped = LOCALIZED_PAGE_PATHS[rest] && LOCALIZED_PAGE_PATHS[rest][lang];
  if(mapped) return mapped + location.search + location.hash;
  if(lang === 'en') return rest + location.search + location.hash;
  return '/' + lang + (rest === '/' ? '/' : rest) + location.search + location.hash;
}

function navigateLang(lang){
  if(!SUPPORTED_LANGS.includes(lang)) return;
  if(lang === detectLangFromUrl()) return; // already here
  try{ localStorage.setItem('icm-lang', lang);}catch(e){}
  location.href = urlForLang(lang);
}

function normalizeTranslatedHtml(value){
  return String(value).replace(/(\S)\s*<br\s*\/?>\s*/gi, '$1 <br/>');
}

// applyLang is kept for graceful re-rendering if the page somehow has the
// wrong language content. On pre-rendered pages this is a no-op visually.
function applyLang(lang){
  const baseDict = I18N[lang]||I18N.en;
  const pageExtra = (window.ICM_I18N_PAGE && (window.ICM_I18N_PAGE[lang]||window.ICM_I18N_PAGE.en)) || {};
  const dict = Object.assign({}, baseDict, pageExtra);
  document.documentElement.lang = lang;
  document.documentElement.dataset.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const k = el.getAttribute('data-i18n');
    if(dict[k] !== undefined){ el.innerHTML = normalizeTranslatedHtml(dict[k]); }
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el=>{
    const k = el.getAttribute('data-i18n-html');
    if(dict[k] !== undefined){ el.innerHTML = normalizeTranslatedHtml(dict[k]); }
  });
  document.querySelectorAll('[data-i18n-alt]').forEach(el=>{
    const k = el.getAttribute('data-i18n-alt');
    if(dict[k] !== undefined){ el.setAttribute('alt', String(dict[k])); }
  });
  document.querySelectorAll('[data-i18n-proj-label]').forEach(el=>{
    const slug = el.getAttribute('data-i18n-proj-label');
    const k = 'proj.label.' + slug;
    if(dict[k] !== undefined){ el.textContent = String(dict[k]); }
  });
  document.querySelectorAll('[data-i18n-proj-tag]').forEach(el=>{
    const slug = el.getAttribute('data-i18n-proj-tag');
    const k = 'proj.tag.' + slug;
    if(dict[k] !== undefined){ el.textContent = String(dict[k]); }
  });
  const cur = document.getElementById('langCurrent');
  if(cur) cur.textContent = lang.toUpperCase();
  document.querySelectorAll('.lang-menu button, .mobile-langs button').forEach(b=>{
    b.setAttribute('aria-current', b.dataset.lang===lang ? 'true':'false');
  });
}

/* ---------- DOM ready ---------- */
document.addEventListener('DOMContentLoaded', ()=>{
  /* Language comes from the URL — page is already pre-rendered in that language. */
  const currentLang = detectLangFromUrl();
  applyLang(currentLang);

  /* Loader (homepage only) */
  const loader = document.getElementById('loader');
  if(loader) setTimeout(()=>loader.classList.add('hidden'), 1700);

  /* Year (footer — every page) */
  const yrEl = document.getElementById('yr');
  if(yrEl) yrEl.textContent = new Date().getFullYear();

  /* Header scroll state */
  const header = document.getElementById('header');
  const onScroll=()=>{ header.classList.toggle('is-scrolled', window.scrollY>40); };
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

  /* Hero parallax */
  const heroBg = document.getElementById('heroBg');
  const heroTitle = document.getElementById('heroTitle');
  if(heroBg){
    let ticking=false;
    window.addEventListener('scroll', ()=>{
      if(ticking) return;
      requestAnimationFrame(()=>{
        const y = Math.min(window.scrollY*0.35, 200);
        heroBg.style.transform = `translate3d(0, ${y}px, 0) scale(1.05)`;
        if(heroTitle) heroTitle.style.transform = `translate3d(0, ${window.scrollY*0.12}px, 0)`;
        ticking=false;
      });
      ticking=true;
    }, {passive:true});
  }

  /* Hero title reveal */
  setTimeout(()=>{
    document.querySelectorAll('#heroTitle .inner').forEach((el,i)=>{
      el.style.transition = `transform .9s cubic-bezier(.2,.7,.2,1) ${i*0.08}s`;
      el.style.transform = 'translateY(0)';
    });
  }, 1900);

  /* Lang menu */
  const langBtn = document.getElementById('langBtn');
  const langMenu = document.getElementById('langMenu');
  langBtn.addEventListener('click', e=>{ e.stopPropagation(); langMenu.classList.toggle('open'); langBtn.setAttribute('aria-expanded', langMenu.classList.contains('open')); });
  document.addEventListener('click', ()=>{ langMenu.classList.remove('open'); langBtn.setAttribute('aria-expanded','false'); });
  langMenu.addEventListener('click', e=>{
    const b = e.target.closest('button[data-lang]');
    if(!b) return;
    navigateLang(b.dataset.lang);
    langMenu.classList.remove('open');
  });
  document.querySelectorAll('.mobile-langs button').forEach(b=>{
    b.addEventListener('click', ()=>{
      navigateLang(b.dataset.lang);
    });
  });

  /* Mobile menu */
  const mt = document.getElementById('menuToggle');
  const drawer = document.getElementById('mobileDrawer');
  mt.addEventListener('click', ()=>{
    mt.classList.toggle('open');
    drawer.classList.toggle('open');
    document.body.style.overflow = drawer.classList.contains('open')?'hidden':'';
  });
  drawer.querySelectorAll('a').forEach(a=>a.addEventListener('click', ()=>{
    drawer.classList.remove('open');
    mt.classList.remove('open');
    document.body.style.overflow = '';
  }));

  /* Reveal observer */
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }});
  }, {threshold:.12, rootMargin:'0px 0px -60px 0px'});
  document.querySelectorAll('.reveal, .reveal-stagger').forEach(el=>io.observe(el));

  /* Counters */
  const cIo = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(!e.isIntersecting) return;
      const el = e.target;
      const target = parseInt(el.dataset.counter,10);
      const suffix = el.dataset.suffix||'';
      const dur = 1600;
      const start = performance.now();
      const from = 0;
      const tick = (now)=>{
        const t = Math.min((now-start)/dur, 1);
        const eased = 1-Math.pow(1-t,3);
        const v = Math.round(from + (target-from)*eased);
        el.textContent = v + suffix;
        if(t<1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      cIo.unobserve(el);
    });
  }, {threshold:.4});
  document.querySelectorAll('[data-counter]').forEach(el=>cIo.observe(el));

  /* Service hover spotlight */
  document.querySelectorAll('.service').forEach(s=>{
    s.addEventListener('mousemove', e=>{
      const r = s.getBoundingClientRect();
      s.style.setProperty('--mx', ((e.clientX-r.left)/r.width*100)+'%');
      s.style.setProperty('--my', ((e.clientY-r.top)/r.height*100)+'%');
    });
  });

  /* FAQ accordion */
  document.querySelectorAll('.faq-item .faq-q').forEach(q=>{
    q.addEventListener('click', ()=>{
      const item = q.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i=>i.classList.remove('open'));
      if(!wasOpen) item.classList.add('open');
    });
  });

  /* Modal — only present on the homepage */
  const modal = document.getElementById('modal');
  if(modal){
    const openModal = ()=>{
      if(!modal.classList.contains('open')) sendLeadEvent('form_view');
      modal.classList.add('open');
      document.body.style.overflow='hidden';
    };
    const closeModal = ()=>{
      modal.classList.remove('open');
      document.body.style.overflow='';
      document.getElementById('formSuccess')?.classList.remove('show');
      const lf = document.getElementById('leadForm'); if(lf) lf.style.display='';
    };
    document.getElementById('openForm')?.addEventListener('click', openModal);
    document.querySelectorAll('[data-cta="book"]').forEach(b=>{
      b.addEventListener('click', e=>{
        // If it's an anchor pointing somewhere other than #contact, let normal navigation happen
        if(b.tagName === 'A'){
          const href = b.getAttribute('href') || '';
          if(href !== '#contact' && href !== '#') return;
          e.preventDefault();
        }
        openModal();
      });
    });
    document.getElementById('closeModal')?.addEventListener('click', closeModal);
    modal.addEventListener('click', e=>{ if(e.target===modal) closeModal(); });
    document.addEventListener('keydown', e=>{ if(e.key==='Escape' && modal.classList.contains('open')) closeModal(); });
  }

  /* Form — track a valid submit, then let FormSubmit redirect to _next */
  const leadForm = document.getElementById('leadForm');
  if(leadForm){
    leadForm.addEventListener('submit', ()=>{
      sendLeadEvent('form_submit');
    });
  }

  /* Delegated lead clicks and page-title attribution for WhatsApp. */
  const WHATSAPP_PAGE_TEXT = {
    en: "Hi Iron Custom Motors! I'm writing from the page: {title}",
    pt: 'Olá Iron Custom Motors! Escrevo a partir da página: {title}',
    ru: 'Здравствуйте, Iron Custom Motors! Пишу со страницы: {title}',
    uk: 'Вітаю, Iron Custom Motors! Пишу зі сторінки: {title}'
  };
  document.addEventListener('click', event=>{
    const anchor = event.target.closest?.('a[href]');
    if(!anchor) return;
    const rawHref = anchor.getAttribute('href') || '';
    if(rawHref.startsWith('https://wa.me')){
      try{
        const url = new URL(anchor.href);
        if(!url.searchParams.has('text')){
          const template = WHATSAPP_PAGE_TEXT[leadPageLang()] || WHATSAPP_PAGE_TEXT.en;
          url.searchParams.set('text', template.replace('{title}', document.title));
          anchor.href = url.toString();
        }
      }catch(e){}
      sendLeadEvent('whatsapp');
    }else if(rawHref.startsWith('tel:')){
      sendLeadEvent('tel');
    }
  }, true);

  /* Sticky CTA bar — show after hero scroll (homepage only) */
  const stickyCta = document.getElementById('stickyCta');
  const heroEl = document.getElementById('hero');
  if(stickyCta && heroEl){
  const stickyIo = new IntersectionObserver(([e])=>{
    const past = !e.isIntersecting;
    stickyCta.classList.toggle('show', past);
    document.body.classList.toggle('has-sticky-cta', past);
  }, {threshold:0});
  stickyIo.observe(heroEl);
  }
  /* === GOOGLE REVIEWS — live rating/count + editorial curated cards === */
  const REVIEWS_ENDPOINT = (window.ICM_REVIEWS_ENDPOINT) || 'https://icm-reviews.vg-ab6.workers.dev/';
  const REVIEWS_CURATED_URL = '/assets/reviews-curated.json';
  const REVIEWS_LS_KEY = 'icm-reviews-cache-v2';
  const REVIEWS_LS_TTL = 12 * 60 * 60 * 1000; // 12h browser-side cache
  const REVIEWS_TEXT_LIMIT = 380;
  const REVIEW_COPY = {
    en: { more: 'Read more', less: 'Show less', source: 'Google review' },
    pt: { more: 'Ler mais', less: 'Mostrar menos', source: 'Avaliação Google' },
    ru: { more: 'Читать полностью', less: 'Свернуть', source: 'Отзыв Google' },
    uk: { more: 'Читати повністю', less: 'Згорнути', source: 'Відгук Google' },
  };

  function getCachedReviews(){
    try{
      const raw = localStorage.getItem(REVIEWS_LS_KEY);
      if(!raw) return null;
      const obj = JSON.parse(raw);
      if(Date.now() - obj._t > REVIEWS_LS_TTL) return null;
      return obj.data;
    }catch(e){ return null; }
  }
  function setCachedReviews(data){
    try{ localStorage.setItem(REVIEWS_LS_KEY, JSON.stringify({_t: Date.now(), data})); }catch(e){}
  }

  function starsSvg(n, total){
    let html = '';
    for(let i=1; i<=total; i++){
      html += `<svg viewBox="0 0 24 24" class="${i<=n?'':'dim'}"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg>`;
    }
    return html;
  }

  function initials(name){
    if(!name) return 'IC';
    const parts = name.trim().split(/\s+/);
    return ((parts[0]?.[0]||'') + (parts[1]?.[0]||'')).toUpperCase() || 'IC';
  }

  function escapeHtml(s){
    return String(s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  function truncate(s, n){
    s = String(s||'').trim();
    if(s.length <= n) return s;
    return s.slice(0, n).replace(/\s+\S*$/,'') + '…';
  }

  function currentReviewLang(){
    const lang = (document.documentElement.lang || 'en').toLowerCase();
    if(lang.startsWith('pt')) return 'pt';
    if(lang.startsWith('ru')) return 'ru';
    if(lang.startsWith('uk')) return 'uk';
    return 'en';
  }

  function currentReviewCopy(){
    return REVIEW_COPY[currentReviewLang()] || REVIEW_COPY.en;
  }

  function formatReviewDate(iso){
    const copy = currentReviewCopy();
    const date = new Date(iso || '');
    if(Number.isNaN(date.getTime())) return copy.source;
    const locale = {en:'en-GB', pt:'pt-PT', ru:'ru-RU', uk:'uk-UA'}[currentReviewLang()] || 'en-GB';
    return new Intl.DateTimeFormat(locale, {year:'numeric', month:'short', day:'numeric'}).format(date);
  }

  function renderReviewsSummary(data){
    if(!data || typeof data.rating !== 'number') return false;
    const summary = document.getElementById('reviewsSummary');
    if(summary){
      const ratingNode = document.getElementById('rsRating');
      const starsNode = document.getElementById('rsStars');
      const totalNode = document.getElementById('rsTotal');
      if(ratingNode) ratingNode.textContent = data.rating.toFixed(1);
      if(starsNode) starsNode.innerHTML = starsSvg(Math.round(data.rating), 5);
      if(totalNode && data.total) totalNode.textContent = data.total;
      summary.removeAttribute('hidden');
    }
    const foot = document.getElementById('reviewsFoot');
    if(foot) foot.removeAttribute('hidden');
    return true;
  }

  function normalizeCuratedReview(record){
    const author = String(record?.author || '').trim();
    const text = String(record?.text || '').trim();
    const publishedAt = String(record?.publishedAt || '').trim();
    const url = String(record?.url || '').trim();
    if(!author || !text || !publishedAt || !url) return null;
    return {
      author,
      text,
      publishedAt,
      url,
      rating: Math.max(1, Math.min(5, Number(record.rating || 5))),
      lang: String(record.lang || 'en').toLowerCase(),
      avatar: String(record.avatar || '').trim(),
    };
  }

  function selectedCuratedReviews(curated){
    const displayCount = Math.max(1, Math.min(9, Number(curated?.displayCount || 6)));
    let reviews = Array.isArray(curated?.reviews) ? curated.reviews.map(normalizeCuratedReview).filter(Boolean) : [];
    if(curated?.preferPageLanguage){
      const pageLang = currentReviewLang();
      reviews = reviews
        .map((review, index) => ({review, index}))
        .sort((a, b) => Number(a.review.lang !== pageLang) - Number(b.review.lang !== pageLang) || a.index - b.index)
        .map(item => item.review);
    }
    return reviews.slice(0, displayCount);
  }

  function reviewAvatarHtml(review){
    if(review.avatar){
      return `<img class="avatar" src="${escapeHtml(review.avatar)}" alt="${escapeHtml(review.author)}" loading="lazy" referrerpolicy="no-referrer" onerror="this.outerHTML='<div class=&quot;avatar&quot;>${initials(review.author)}</div>'" />`;
    }
    return `<div class="avatar">${initials(review.author)}</div>`;
  }

  function renderCuratedReviews(curated){
    const row = document.getElementById('reviewsRow');
    if(!row) return false;
    const picks = selectedCuratedReviews(curated);
    if(!picks.length) return false;
    const copy = currentReviewCopy();
    row.innerHTML = picks.map(r => {
      const shortText = truncate(r.text, REVIEWS_TEXT_LIMIT);
      const isTruncated = shortText !== r.text;
      const toggle = isTruncated
        ? `<button class="review-toggle" type="button" data-review-toggle data-more="${escapeHtml(copy.more)}" data-less="${escapeHtml(copy.less)}">${escapeHtml(copy.more)}</button>`
        : '';
      return `
        <article class="review">
          <div class="stars">${starsSvg(Math.round(r.rating||5), 5)}</div>
          <p class="review-text" data-full-text="${escapeHtml(r.text)}" data-short-text="${escapeHtml(shortText)}">&ldquo;${escapeHtml(shortText)}&rdquo;</p>
          ${toggle}
          <div class="author">
            ${reviewAvatarHtml(r)}
            <div class="author-info">
              <span class="name">${escapeHtml(r.author)}</span>
              <span class="role">${escapeHtml(copy.source)} · ${escapeHtml(formatReviewDate(r.publishedAt))}</span>
            </div>
          </div>
        </article>
      `;
    }).join('');
    row.classList.add('in');
    const foot = document.getElementById('reviewsFoot');
    if(foot) foot.removeAttribute('hidden');
    return true;
  }

  async function loadCuratedReviews(){
    try{
      const resp = await fetch(REVIEWS_CURATED_URL, { cache: 'no-store' });
      if(!resp.ok) return false;
      return renderCuratedReviews(await resp.json());
    }catch(e){
      return false;
    }
  }

  async function loadReviews(){
    // Try local cache first — instant render
    const cached = getCachedReviews();
    if(cached){ renderReviewsSummary(cached); }
    loadCuratedReviews();

    try{
      const resp = await fetch(REVIEWS_ENDPOINT, { cache: 'no-store' });
      if(!resp.ok) return;
      const data = await resp.json();
      if(data && typeof data.rating === 'number' && data.total){
        setCachedReviews(data);
        renderReviewsSummary(data);
      }
    }catch(e){
      // fail silently — keep static fallback / cached version
    }
  }
  document.addEventListener('click', e => {
    const button = e.target.closest('[data-review-toggle]');
    if(!button) return;
    const review = button.closest('.review');
    const textNode = review?.querySelector('.review-text');
    if(!textNode) return;
    const expanded = button.getAttribute('aria-expanded') === 'true';
    const nextText = expanded ? textNode.dataset.shortText : textNode.dataset.fullText;
    textNode.innerHTML = `&ldquo;${escapeHtml(nextText || '')}&rdquo;`;
    button.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    button.textContent = expanded ? (button.dataset.more || 'Read more') : (button.dataset.less || 'Show less');
  });
  // Lazy-load: fetch only when user scrolls near reviews section
  const reviewsSection = document.getElementById('reviews');
  if(reviewsSection){
    const ro = new IntersectionObserver((entries)=>{
      for(const e of entries){
        if(e.isIntersecting){
          loadReviews();
          ro.disconnect();
          break;
        }
      }
    }, {rootMargin: '300px 0px'});
    ro.observe(reviewsSection);
  }

  /* Make whole-card clickable on desktop AND mobile for cards that contain
     a single primary CTA link. Uses pointer events. Preserves text selection
     and never fires during scroll.
       .service     — home page service tiles (link selector: a.arrow-link)
       .svc-card    — /services/ hub cards         (link selector: a.cta)
       .ctc-card    — /contact/ channel cards      (link selector: a.cta)
  */
  const CARD_PATTERNS = [
    { sel: '.service',  link: 'a.arrow-link' },
    { sel: '.svc-card', link: 'a.cta' },
    { sel: '.ctc-card', link: 'a.cta' },
  ];
  CARD_PATTERNS.forEach(({ sel, link }) => {
    document.querySelectorAll(sel).forEach(card => {
      const a = card.querySelector(link);
      if(!a) return;
      card.style.cursor = 'pointer';
      card.style.webkitTapHighlightColor = 'transparent';

      let downX = 0, downY = 0, downT = 0, moved = false;

      card.addEventListener('pointerdown', e => {
        downX = e.clientX;
        downY = e.clientY;
        downT = Date.now();
        moved = false;
      }, { passive: true });

      card.addEventListener('pointermove', e => {
        if(Math.abs(e.clientX - downX) > 8 || Math.abs(e.clientY - downY) > 8){
          moved = true;
        }
      }, { passive: true });

      card.addEventListener('click', e => {
        if(moved) return;
        if(Date.now() - downT > 500) return;
        if(e.target.closest('a, button')) return;
        const seln = window.getSelection && window.getSelection().toString();
        if(seln && seln.length) return;
        // Honor cmd/ctrl-click → open in new tab
        if(e.metaKey || e.ctrlKey){
          window.open(a.href, '_blank', 'noopener');
        } else if(a.target === '_blank'){
          window.open(a.href, '_blank', 'noopener');
        } else {
          a.click();
        }
      });

      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'link');
      card.addEventListener('keydown', e => {
        if(e.key === 'Enter'){ e.preventDefault(); a.click(); }
      });
    });
  });

  /* Smooth-scroll fallback for #anchors with header offset */
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click', e=>{
      const href = a.getAttribute('href');
      if(href === '#' || href.length<2) return;
      const target = document.querySelector(href);
      if(!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 70;
      window.scrollTo({top, behavior:'smooth'});
    });
  });
});
