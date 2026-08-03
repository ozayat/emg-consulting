#!/usr/bin/env python3
"""Generate the static EMG site.

Header, footer and <head> live here once so the seven pages cannot drift apart.
Output is plain static HTML with no runtime dependency — the built files are what
gets deployed, this script is only for maintenance.

Usage:  python3 tools/build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "EMG Consulting Group"
EMAIL = "emg@emg-consulting-group.com"
TEL_EG_HREF, TEL_EG = "+201061920027", "+20 106 192 0027"
TEL_SA_HREF, TEL_SA = "+966508993750", "+966 50 899 3750"
PDF = "assets/docs/EMG-Reference-Portfolio.pdf"

NAV = [
    ("services.html", "Services"),
    ("projects.html", "Projects"),
    ("expertise.html", "Expertise"),
    ("alliance.html", "Alliance"),
    ("about.html", "About"),
]

ARROW = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M2 8h11M9 4l4 4-4 4"/></svg>')
DOWNLOAD = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M8 2v9M4.5 7.5 8 11l3.5-3.5M2.5 13.5h11"/></svg>')
TICK = ('<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="m4 10.5 4 4 8-9"/></svg>')


def mark(idp):
    """The EMG mark. Ids are namespaced so several copies can share a page."""
    return f'''<svg class="brand-mark" viewBox="0 0 64 64" fill="none" aria-hidden="true">
        <defs>
          <linearGradient id="{idp}-c" x1="9" y1="54" x2="58" y2="12" gradientUnits="userSpaceOnUse">
            <stop offset="0" stop-color="#0A7F92"/><stop offset=".45" stop-color="#17B0C4"/><stop offset="1" stop-color="#6DB77F"/>
          </linearGradient>
          <mask id="{idp}-g">
            <circle cx="35.4" cy="27.2" r="14.6" fill="#fff"/>
            <g stroke="#000" stroke-width="2.1" fill="none" stroke-linecap="round">
              <path d="M22 21.6q8.03 -3.2 16.06 0t16.06 0"/>
              <path d="M21.2 28.3q8.47 -3.4 16.94 0t16.94 0"/>
              <path d="M23 35q7.3 -3 14.6 0t14.6 0"/>
            </g>
          </mask>
        </defs>
        <path d="M5.4 28.6C4.6 44.6 17 57 32.6 57C46.6 57 56.6 47.4 60 30.6C61 25.6 61.7 19.4 61.9 11.8C57.2 19.8 54.2 26.4 52.4 32.2C49 42.4 41.8 48.1 32.6 48.1C22.4 48.1 14.6 40.2 14.4 28.6C14.3 22.5 5.5 22.4 5.4 28.6Z" fill="url(#{idp}-c)"/>
        <circle cx="35.4" cy="27.2" r="14.6" fill="currentColor" mask="url(#{idp}-g)"/>
      </svg>'''


def brand(idp):
    return f'''<a class="brand" href="index.html">
      {mark(idp)}
      <span class="brand-text">
        <span class="brand-name">EMG</span>
        <span class="brand-sub">Consulting Group</span>
      </span>
    </a>'''


def head(title, desc, canonical):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/img/brand/emg-mark.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/ibm-plex-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<link rel="canonical" href="https://www.emg-consulting-group.com/{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://www.emg-consulting-group.com/{canonical}">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
'''


def header(active):
    CUR = ' aria-current="page"'
    links = "".join(
        '      <a href="{}"{}>{}</a>\n'.format(href, CUR if href == active else "", label)
        for href, label in NAV)
    return f'''
<header class="site-header" id="header">
  <div class="wrap">
    {brand("hdr")}
    <button class="burger" aria-label="Toggle navigation" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav">
{links}      <a class="btn btn-ghost header-cta" href="contact.html">Contact</a>
    </nav>
  </div>
</header>

<main id="main">
'''


FOOTER = f'''
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        {brand("ftr")}
        <p class="measure-sm" style="color:#8FB0B7; font-size:.9rem; margin-top:1.1rem">
          Environmental engineering consultancy services provider — water and wastewater treatment
          systems, and water, air and soil pollution control.
        </p>
      </div>
      <div class="footer-col">
        <h4>Practice</h4>
        <ul>
          <li><a href="services.html">Services</a></li>
          <li><a href="projects.html">Reference projects</a></li>
          <li><a href="expertise.html">Scholar expertise</a></li>
          <li><a href="alliance.html">Environmental alliance</a></li>
          <li><a href="about.html">About &amp; quality</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="tel:{TEL_EG_HREF}">{TEL_EG} — Giza</a></li>
          <li><a href="tel:{TEL_SA_HREF}">{TEL_SA} — Riyadh</a></li>
          <li><a href="{PDF}" download>Reference portfolio (PDF)</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="yr">2026</span> {SITE}. All rights reserved.</p>
      <p>Environmental Engineering Consultancy Services Provider</p>
    </div>
  </div>
</footer>

<script src="assets/js/site.js" defer></script>
</body>
</html>
'''


def pagehead(eyebrow, h1, lede, img, alt):
    return f'''
<section class="pagehead">
  <div class="pagehead-media"><img src="{img}" alt="{alt}" fetchpriority="high"></div>
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
'''


def cta(title, text, primary=("contact.html", "Talk to us"), secondary=None):
    sec = ""
    if secondary:
        sec = f'<a class="btn btn-ghost" href="{secondary[0]}">{secondary[1]}</a>'
    return f'''
<section class="section band-dark">
  <div class="wrap">
    <div class="split reveal">
      <div>
        <h2 class="h2">{title}</h2>
        <p class="lede" style="margin-top:1.1rem">{text}</p>
      </div>
      <div style="display:flex; gap:.85rem; flex-wrap:wrap; align-self:center">
        <a class="btn btn-accent" href="{primary[0]}">{primary[1]} {ARROW}</a>
        {sec}
      </div>
    </div>
  </div>
</section>
'''


# ===========================================================================
#  SERVICES
# ===========================================================================
SERVICES = [
    ("Environmental &amp; Social Impact Assessment (ESIA)",
     "Scoping through baseline studies, checklists, matrices and network diagrams. These techniques "
     "collect and present knowledge so that logical decisions can be made about which impacts are "
     "most significant."),
    ("Environmental &amp; Social Action Plans (IFC)",
     "Action plans structured against IFC Performance Standards, written to survive lender and "
     "regulator scrutiny."),
    ("Social Management", ""),
    ("Site Characterisation",
     "Investigation and delineation of contamination across soil, groundwater, sediment and "
     "surface water."),
    ("Waste Management &amp; Waste-to-Energy", ""),
    ("Environmental Remediation",
     "Removal of pollution and contaminants from environmental media, supported by laboratory "
     "analysis and monitoring."),
    ("Pollution Control", ""),
    ("Modelling — air dispersion, microclimate and heat waste", ""),
    ("Climate Change Risk Assessment", ""),
]

EXPERTISE_GROUPS = [
    ("Treatment &amp; conveyance", [
        "Water and wastewater treatment systems",
        "Pumping systems",
        "Process design",
        "Hydraulics",
        "Pilot plants and retrofitting",
    ]),
    ("Modelling &amp; simulation", [
        "Dynamic simulation",
        "CFD modelling",
        "Physical modelling",
        "Process simulation",
    ]),
    ("Assurance &amp; risk", [
        "HAZOP studies",
        "Risk assessment — qualitative and quantitative",
        "Value engineering",
        "Environmental control and laboratory analysis",
    ]),
    ("Studies &amp; research", [
        "Research and development, theses supervision",
        "Feasibility studies",
        "Institutional studies",
        "Social and economic studies",
    ]),
]


def services_page():
    rows = ""
    for i, (title, desc) in enumerate(SERVICES, 1):
        d = f'<span class="svc-d">{desc}</span>' if desc else ""
        rows += (f'      <li class="svc"><span class="svc-n">{i:02d}</span>'
                 f'<span class="svc-t">{title}</span>{d}</li>\n')

    groups = ""
    for name, items in EXPERTISE_GROUPS:
        lis = "".join(f'<li class="chip">{i}</li>' for i in items)
        groups += (f'''      <div>
        <h3 class="h4" style="margin-bottom:1rem">{name}</h3>
        <ul class="chips">{lis}</ul>
      </div>\n''')

    return (
        pagehead("Consultancy services",
                 "Find your potential solution for an environmental problem.",
                 "From impact assessment through remediation and modelling — the full consultancy "
                 "scope EMG has delivered since 1999.",
                 "assets/img/hero/lab-analysis.jpg",
                 "Laboratory water-quality analysis")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Services register</p>
      <h2 class="h2">What we are engaged to do.</h2>
    </div>
    <ol class="svc-list reveal">
{rows}    </ol>
  </div>
</section>

<section class="section band-dark">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Engineering key expertise</p>
      <h2 class="h2">Design is only credible when it is verified.</h2>
      <p class="lede">
        EMG couples treatment process design with hydraulic and dynamic simulation, CFD, physical
        modelling and formal risk study, so that performance is demonstrated before it is built.
      </p>
    </div>
    <div class="grid g-2 reveal">
{groups}    </div>
  </div>
</section>

<section class="section band-alt">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Impact assessment</p>
      <h2 class="h2">A defined process, not a document exercise.</h2>
      <p class="lede">
        The main EIA techniques used in scoping are baseline studies, checklists, matrices and
        network diagrams — presenting information so decisions about significance are defensible.
      </p>
    </div>
    <div class="grid g-3 reveal">
      <figure class="figure"><img src="assets/img/diagrams/eia.png" alt="Key stages of environmental impact assessment" loading="lazy"><figcaption>Key stages of EIA</figcaption></figure>
      <figure class="figure"><img src="assets/img/diagrams/eia-process.png" alt="Environmental impact assessment process" loading="lazy"><figcaption>EIA process</figcaption></figure>
      <figure class="figure"><img src="assets/img/diagrams/eia-procedures.png" alt="Environmental impact assessment procedures" loading="lazy"><figcaption>EIA procedures</figcaption></figure>
    </div>
  </div>
</section>

<section class="section band-paper">
  <div class="wrap">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Applied practice</p>
        <h2 class="h2">Remediation, restoration and recovery.</h2>
        <div class="prose" style="margin-top:1.1rem">
          <p>Environmental remediation deals with the removal of pollution or contaminants from
             environmental media such as soil, groundwater, sediment or surface water.</p>
          <p>Ecosystem restoration assists the recovery of ecosystems that have been degraded or
             destroyed, as well as conserving those still intact — creating the conditions needed
             for recovery so that plants, animals and microorganisms can carry out the work of
             recovery themselves.</p>
        </div>
      </div>
      <div class="grid g-2" style="gap:1rem">
        <figure class="figure"><img src="assets/img/photos/soil-remediation-approach.jpg" alt="Soil remediation approach" loading="lazy"></figure>
        <figure class="figure"><img src="assets/img/photos/waste-to-energy.jpg" alt="Waste-to-energy concept" loading="lazy"></figure>
        <figure class="figure"><img src="assets/img/photos/ecology-birds.jpg" alt="Wetland bird ecology" loading="lazy"></figure>
        <figure class="figure"><img src="assets/img/photos/soil-groundwater.png" alt="Soil and groundwater interaction" loading="lazy"></figure>
      </div>
    </div>
  </div>
</section>
'''
        + cta("Have a problem that needs an engineering answer?",
              "Tell us the constraint — capacity, compliance, cost or programme — and we will tell "
              "you what can be demonstrated.",
              ("contact.html", "Start a conversation"),
              ("projects.html", "See reference projects")))


# ===========================================================================
#  PROJECTS
# ===========================================================================
PROJECTS = [
    dict(title="ICEAS 120,000 CMD — Qarun Lake Water Pollution Control",
         tag="Process design", img="assets/img/diagrams/biowin-simulation.png", sheet=True,
         alt="Process flowsheet for a 120,000 m³/day SBR treatment train",
         client="FWWC — funded by EBRD (€400M)", location="Fayoum, Egypt", year="2020"),
    dict(title="R&amp;D BNR Process System, 1,000 CMD",
         tag="Research &amp; development", img="assets/img/projects/mowe-bnr-stp.jpg", sheet=True,
         alt="Biological nutrient removal research and development record",
         client="KACST", location="Riyadh, Saudi Arabia", year="2005"),
    dict(title="Riyadh STP Aeration Retrofitting",
         tag="Retrofitting", img="assets/img/projects/kacst-bnr-stp.jpg", sheet=True,
         alt="Aeration retrofitting project correspondence and specification",
         client="Riyadh General Water Directorate", location="Riyadh, Saudi Arabia", year="2005"),
    dict(title="King Abdul Aziz Endowment Grey Water Treatment Plant, Towers A–B",
         tag="Grey water", img="assets/img/projects/king-abdulaziz-endowment.jpg", sheet=False,
         alt="King Abdul Aziz Endowment towers, Makkah",
         client="SBG Group", location="Makkah, Saudi Arabia", year="2005"),
    dict(title="Al Khumrah Industrial Treatment Plant, 50,000 CMD",
         tag="Process &amp; instrumentation", img="assets/img/projects/al-khumrah-wwtp.png", sheet=True,
         alt="Process and instrumentation diagram for the Al Khumrah industrial treatment plant",
         client="SuidoKiko Middle East", location="Jeddah, Saudi Arabia", year="2009"),
    dict(title="Dammam Technical Industrial Zone Master Plan",
         tag="Master planning", img="assets/img/projects/dammam-technical-zone.png", sheet=True,
         alt="Organisational structure diagram for the Dammam technical industrial zone",
         client="SOIETZ", location="Dammam, Saudi Arabia", year="2005"),
    dict(title="West Makkah (Hadda) Main Lifting Station, 250,000 m³/day",
         tag="Hydraulics", img="assets/img/projects/west-makkah-lifting-station.png", sheet=True,
         alt="Schematic of the West Makkah main lifting station",
         client="Makkah Al-Mukaramah Water Directorate", location="Jeddah, Saudi Arabia", year="2007"),
    dict(title="Hail Sewage Treatment Plant, 150,000 m³/day",
         tag="Plant layout", img="assets/img/projects/hail-stp.png", sheet=True,
         alt="General layout drawing of the Hail sewage treatment plant",
         client="CWC", location="Hai'l, Saudi Arabia", year="2010"),
    dict(title="Dirab Pumping Station, 75,000 m³/day — CFD Modelling",
         tag="CFD modelling", img="assets/img/projects/dirab-cfd.png", sheet=True,
         alt="CFD velocity field for the Dirab pumping station suction chamber",
         client="NWC Saudi Arabia", location="Riyadh, Saudi Arabia", year="2022"),
]


def projects_page():
    cards = ""
    for p in PROJECTS:
        sheet = " sheet" if p["sheet"] else ""
        cards += f'''      <article class="proj reveal">
        <div class="proj-media{sheet}">
          <span class="proj-tag">{p["tag"]}</span>
          <img src="{p["img"]}" alt="{p["alt"]}" loading="lazy">
        </div>
        <div class="proj-body">
          <h3>{p["title"]}</h3>
          <dl class="spec">
            <div><dt>Client</dt><dd>{p["client"]}</dd></div>
            <div><dt>Location</dt><dd>{p["location"]}</dd></div>
            <div><dt>Year</dt><dd>{p["year"]}</dd></div>
          </dl>
        </div>
      </article>\n'''

    thumbs = "".join(
        f'<img src="assets/img/reference/thumbs/page-{n:03d}.jpg" alt="" loading="lazy">'
        for n in (1, 14, 32, 48, 67, 89, 112, 140))

    return (
        pagehead("Reference projects",
                 "Twenty-five years of delivery across Egypt and the Gulf.",
                 "Work for national water authorities, research councils and international "
                 "contractors — from R&amp;D pilot plants to 250,000 m³/day infrastructure.",
                 "assets/img/hero/treatment-basins.jpg",
                 "Wastewater treatment basins")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Selected work</p>
      <h2 class="h2">Project references.</h2>
      <p class="lede">
        Each entry below is drawn from EMG's reference records. Drawings, flowsheets and simulation
        output are shown as issued rather than cropped for effect.
      </p>
    </div>
    <div class="grid g-3">
{cards}    </div>
  </div>
</section>

<section class="section band-ink">
  <div class="wrap">
    <div class="deck reveal">
      <div>
        <p class="eyebrow">Reference portfolio</p>
        <h2 class="h2">197 pages of documented project history.</h2>
        <p class="lede" style="margin-top:1.1rem">
          The complete reference portfolio records partnerships, plant commissions, research
          programmes and international collaborations across the last quarter century.
        </p>
        <div class="hero-actions" style="margin-top:2rem">
          <a class="btn btn-accent" href="{PDF}" download>{DOWNLOAD} Download PDF (20 MB)</a>
          <a class="btn btn-ghost" href="portfolio.html">Read the portfolio {ARROW}</a>
        </div>
      </div>
      <div class="deck-sheet" aria-hidden="true">{thumbs}</div>
    </div>
  </div>
</section>
'''
        + cta("Need a reference for a similar scheme?",
              "We can supply detailed project records, drawings and client references on request.",
              ("contact.html", "Request references"),
              ("services.html", "Our services")))


# ===========================================================================
#  EXPERTISE  (founder + credentials)
# ===========================================================================
CREDENTIALS = [
    ("unesco-seminar-2004", "UNESCO", "International Seminar certificate, 2004"),
    ("water-middle-east-cert-2003", "Water Middle East", "Certificate, 2003"),
    ("water-middle-east-appreciation-2003", "Water Middle East", "Letter of appreciation, 2003"),
    ("water-middle-east-invite-2003", "Water Middle East", "Invitation letter, 2003"),
    ("water-middle-east-invite-2004", "Water Middle East", "Invitation letter, 2004"),
    ("water-middle-east-2005", "3rd Water Middle East", "Conference, 2005"),
    ("kacst-rd-stp-2005", "KACST", "R&amp;D sewage treatment plant, 2005"),
    ("sbg-makkah-2005", "SBG Makkah", "DKAE grey water scheme, 2005"),
    ("oman-workshop-invite-2005", "MRMEWR Oman", "International workshop invitation, 2005"),
    ("icwrae-2008", "ICWRAE", "Conference certificate, 2008"),
    ("jica-2008", "JICA", "Certificate, 2008"),
    ("oman-mrmwr-2009", "MRMWR Oman", "Certificate, 2009"),
    ("iwrm-2010", "IWRM Karlsruhe 2010", "Invited lecture, Germany"),
    ("icwrae-2010", "ICWRAE", "Conference certificate, 2010"),
    ("oman-mrmwr-2014", "MRMWR Oman", "Certificate, 2014"),
    ("oman-water-society-2014", "Oman Water Society", "Certificate, 2014"),
    ("ewdr-turkey-2014", "EWDR Türkiye", "Certificate, 2014"),
    ("icwrae-2016", "ICWRAE", "7th International Conference on Water Resources and Arid Environments, Riyadh, 2016"),
    ("metito-2020", "Metito", "Certificate, 2020"),
    ("iceas-biowin-2021", "ICEAS &amp; BioWin", "Simulation training, 2021"),
    ("dynamic-simulation-2021", "Dynamic simulation", "Training certificate, 2021"),
    ("mbbr-2021", "MBBR", "Process training, 2021"),
    ("ifas-2021", "IFAS", "Process training, 2021"),
    ("applied-diploma-2021", "Applied diploma", "2021"),
    ("swf-2021", "Stockholm World Water Week", "2021"),
    ("bgi-2023", "BGI", "Certificate, 2023"),
    ("hazop-2024", "HAZOP", "Hazard and operability study, 2024"),
    ("physical-modelling-2024", "Physical modelling", "Complex hydraulic structures, 2024"),
    ("ro-plant-webinar-2024", "Reverse osmosis", "Plant webinar, 2024"),
    ("ro-plants-performance-2024", "Reverse osmosis", "Plant performance, 2024"),
    ("ksa-desalination-2024", "Desalination", "Saudi Arabia sector publication, 2024"),
    ("diploma-phd", "Doctoral diploma", "Cairo University"),
]

EDUCATION = [
    ("1987", "B.Sc. Civil Engineering",
     "Cairo University, Giza"),
    ("Diploma", "Environmental &amp; Sanitary Engineering, Diploma of Higher Studies",
     "Cairo University, Giza"),
    ("M.Sc.", "Master of Science",
     "Cairo University, Giza — <em>Comparative study on activated sludge biological treatment "
     "systems in some Arab cities</em>"),
    ("Ph.D.", "Doctor of Philosophy",
     "Cairo University, with Ruhr University Bochum, Germany as co-referee — "
     "<em>Development of dynamic simulation and modelling for Bio-P removal</em>"),
]


def expertise_page():
    edu = ""
    for term, title, detail in EDUCATION:
        edu += (f'      <div><dt>{term}</dt><dd>{title}<em>{detail}</em></dd></div>\n')

    wall = ""
    for slug, name, detail in CREDENTIALS:
        wall += f'''      <figure class="reveal">
        <div class="shot"><img src="assets/img/credentials/{slug}.jpg" alt="{re.sub("&amp;", "and", name)} — {re.sub("&amp;", "and", detail)}" loading="lazy"></div>
        <figcaption><b>{name}</b>{detail}</figcaption>
      </figure>\n'''

    return (
        pagehead("Scholar expertise",
                 "Dr. Ahmed El-Zayat",
                 "Environmental sanitation and water resources expert, and founder of EMG "
                 "Consulting Group.",
                 "assets/img/hero/water-analysis.jpg",
                 "Water sampling and analysis")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="bio reveal">
      <figure class="bio-portrait" style="margin:0">
        <img src="assets/img/brand/founder-portrait.jpg" alt="Dr. Ahmed El-Zayat delivering a lecture at IWRM Karlsruhe 2010">
        <figcaption>Delivering an invited lecture at IWRM — Integrated Water Resources Management, Karlsruhe, Germany, November 2010.</figcaption>
      </figure>
      <div>
        <p class="eyebrow">Founder</p>
        <h2 class="h2">Dr. Ahmed El-Zayat</h2>
        <p class="bio-role">Environmental sanitation &amp; water resources expert</p>
        <div class="prose" style="margin-top:1.3rem">
          <p>Dr. El-Zayat founded EMG in Egypt in 1999 and has led the practice since, working across
             Egypt, Saudi Arabia, Oman and the wider region. His specialisation is water and
             wastewater treatment systems, and water resources and irrigation.</p>
          <p>His doctoral research developed dynamic simulation and modelling for biological
             phosphorus removal, carried out at Cairo University with Ruhr University Bochum in
             Germany as co-referee — the foundation of the process-simulation capability EMG applies
             to plant design and retrofitting today.</p>
          <p>Alongside consultancy he has contributed to international conferences and training
             programmes, including an invited lecture at IWRM Karlsruhe 2010 on a
             <em>multi-criteria framework for performance benchmarking of the water sectors in the
             Nile Basin</em>.</p>
        </div>

        <h3 class="h4" style="margin-top:2.4rem">Education</h3>
        <dl class="deflist">
{edu}        </dl>

        <h3 class="h4" style="margin-top:2.4rem">Specialisation</h3>
        <ul class="checks" style="margin-top:1rem">
          <li>{TICK}<span>Water &amp; wastewater treatment systems</span></li>
          <li>{TICK}<span>Water resources &amp; irrigation</span></li>
          <li>{TICK}<span>Process simulation and modelling</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section band-alt">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Record</p>
      <h2 class="h2">Certifications, conference contributions and appreciation letters.</h2>
      <p class="lede">
        Continuous academic and professional development across two decades — training
        certifications, invited lectures, and letters from water authorities across the region.
      </p>
    </div>
    <div class="credwall">
{wall}    </div>
  </div>
</section>
'''
        + cta("Looking for a technical reviewer or expert witness?",
              "Dr. El-Zayat undertakes design review, process troubleshooting, training and "
              "research supervision alongside EMG's consultancy work.",
              ("contact.html", "Get in touch"),
              ("projects.html", "Reference projects")))


# ===========================================================================
#  ALLIANCE
# ===========================================================================
def alliance_page():
    logos = [
        ("unesco.png", "UNESCO"), ("un-water.svg", "UN Water"),
        ("iwa.png", "International Water Association"), ("iucn.svg", "IUCN"),
        ("wwc.png", "World Water Council"), ("iwta.png", "International Water Technology Association"),
        ("mwri-egypt.png", "Ministry of Water Resources and Irrigation, Egypt"),
        ("eeaa-egypt.png", "Egyptian Environmental Affairs Agency"),
        ("moa-egypt.png", "Ministry of Agriculture and Land Reclamation, Egypt"),
        ("asrt.png", "Academy of Scientific Research and Technology"),
        ("nwrc.png", "National Water Research Center, Egypt"),
        ("arc.png", "Agricultural Research Center, Egypt"),
        ("bmwk-germany.png", "German Federal Ministry for Economic Affairs and Climate Action"),
        ("gtai.svg", "Germany Trade and Invest"),
        ("ahk-saudi.svg", "German-Saudi Arabian Liaison Office for Economic Affairs"),
        ("research-in-germany.png", "Research in Germany"),
        ("dubai-municipality.png", "Dubai Municipality"),
        ("moc-bahrain.png", "Ministry of Industry and Commerce, Bahrain"),
    ]
    grid = "".join(
        f'      <li><img src="assets/img/partners/{f}" alt="{a}" loading="lazy"></li>\n'
        for f, a in logos)

    return (
        pagehead("Environmental alliance",
                 "Consultancy delivered through a network, not a single office.",
                 "EMG works alongside specialist houses of expertise in Egypt and Germany, and "
                 "through an international water technology association.",
                 "assets/img/hero/engineering-works.jpg",
                 "Engineering works")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="grid g-3">
      <article class="partner reveal">
        <div class="partner-logo"><img src="assets/img/partners/enviglobe.png" alt="EnviGlobe" loading="lazy"></div>
        <p class="mono">Egypt &middot; est. 2010</p>
        <h3 class="h3">EnviGlobe</h3>
        <p>A certified house of expertise in the field of environment, established in 2010, bringing
           more than fifty years of collective experience across engineering, energy and
           environmental consulting.</p>
      </article>

      <article class="partner reveal">
        <div class="partner-logo"><img src="assets/img/partners/knollmann.png" alt="Knollmann Ingenieurgesellschaft mbH" loading="lazy"></div>
        <p class="mono">Germany &middot; engineering</p>
        <h3 class="h3">Knollmann</h3>
        <p>A German engineering practice with thirty years of experience realising large-scale
           projects. Beyond classic consultation and planning, it increasingly takes on
           comprehensive areas of responsibility — advising a project from first idea through to
           operational handover.</p>
      </article>

      <article class="partner reveal">
        <div class="partner-logo"><img src="assets/img/partners/iwta.png" alt="International Water Technology Association" loading="lazy"></div>
        <p class="mono">Association no. 1623 &middot; 2004</p>
        <h3 class="h3">International Water Technology Association</h3>
        <p>Founded by experts and professors as non-governmental association no. 1623 of 2004, and
           restructured in October 2010 into an international association.</p>
      </article>
    </div>

    <div class="sec-head reveal" style="margin-top:clamp(3.5rem,7vw,6rem)">
      <p class="eyebrow">IWTA aims</p>
      <h2 class="h2">What the association sets out to do.</h2>
    </div>
    <div class="grid g-2 reveal">
      <ul class="checks">
        <li>{TICK}<span>Highlight the importance of the water issue socially and economically at local, national and international level</span></li>
        <li>{TICK}<span>Highlight water and resource preservation</span></li>
        <li>{TICK}<span>Spread modern water treatment and desalination technology</span></li>
      </ul>
      <ul class="checks">
        <li>{TICK}<span>Organise training courses</span></li>
        <li>{TICK}<span>Organise scientific and awareness meetings</span></li>
        <li>{TICK}<span>Conduct research on aquatic resources and water management</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section band-alt">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Institutions &amp; collaboration</p>
      <h2 class="h2">Working alongside authorities, research bodies and global water organisations.</h2>
    </div>
    <ul class="logos reveal">
{grid}    </ul>
  </div>
</section>
'''
        + cta("Want to work with the alliance?",
              "Projects that need combined Egyptian delivery and German engineering practice are "
              "where this network is strongest.",
              ("contact.html", "Contact EMG"),
              ("projects.html", "Reference projects")))


# ===========================================================================
#  ABOUT  (firm, vision, QMS, HSE)
# ===========================================================================
METHOD = [
    ("Plan and design water systems", ""),
    ("Develop wastewater treatment facilities", ""),
    ("Analyse surface and groundwater quality", ""),
    ("Design soil remediation systems", ""),
    ("Plan waste collection and disposal", ""),
    ("Reuse wastewater and sludge", ""),
]

APPLICATIONS = ["Water &amp; wastewater treatment", "Government", "Training", "Construction",
                "Research and science", "Natural science", "Civil design", "Energy"]


def about_page():
    steps = "".join(f'      <li><div><h3>{t}</h3>{f"<p>{d}</p>" if d else ""}</div></li>\n'
                    for t, d in METHOD)
    apps = "".join(f'<li class="chip">{a}</li>' for a in APPLICATIONS)

    return (
        pagehead("About EMG",
                 "A specialised consultancy, built to make environmental engineering demonstrable.",
                 "EMG Consulting Group was founded in Egypt in 1999. Our objective is to transfer "
                 "extensive expertise and spread broad knowledge through experience-sharing.",
                 "assets/img/hero/stp-aerial.jpg",
                 "Aerial view of a sewage treatment plant")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="grid g-3 reveal">
      <div>
        <p class="eyebrow">Our vision</p>
        <h2 class="h3">Safe, eco-friendly, cost-effective and innovative practice.</h2>
        <p class="prose" style="margin-top:.9rem">A commitment to practices that deliver value for
           all stakeholders — client, community and environment alike.</p>
      </div>
      <div>
        <p class="eyebrow">Our strategy</p>
        <h2 class="h3">Experts working with cross-functional teams.</h2>
        <p class="prose" style="margin-top:.9rem">Our experts work with cross-functional teams to
           differentiate our clients and capture demand.</p>
      </div>
      <div>
        <p class="eyebrow">Our strength</p>
        <ul class="checks" style="margin-top:.4rem">
          <li>{TICK}<span>Creative and practical solutions</span></li>
          <li>{TICK}<span>Rigorous analysis of the situation</span></li>
          <li>{TICK}<span>New ideas for traditional problems</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section band-alt">
  <div class="wrap">
    <div class="split split-40 reveal">
      <div>
        <p class="eyebrow">Quality management</p>
        <h2 class="h2">What makes EMG one of the leading providers of environmental expertise.</h2>
        <p class="lede" style="margin-top:1.1rem">
          Our goal is the long-term viability of societal development and of the water, land and
          air resources it depends on. That goal is pursued through a defined method.
        </p>
      </div>
      <ol class="steps">
{steps}      </ol>
    </div>
  </div>
</section>

<section class="section band-dark">
  <div class="wrap">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Applications</p>
        <h2 class="h2">Where the practice is applied.</h2>
        <p class="lede" style="margin-top:1.1rem">
          EMG's disciplines are deployed across public and private sectors, from utility
          infrastructure to research programmes.
        </p>
      </div>
      <div><ul class="chips">{apps}</ul></div>
    </div>
  </div>
</section>

<section class="section band-paper">
  <div class="wrap">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Operational excellence</p>
        <h2 class="h2">Health, safety and environment through full utilisation of intelligent field.</h2>
        <p class="prose" style="margin-top:1.1rem">
          Operational excellence is treated as an engineering deliverable — designed in, measured,
          and verified in operation rather than asserted in a policy document.
        </p>
      </div>
      <div class="grid g-2" style="gap:1rem">
        <figure class="figure"><img src="assets/img/photos/hse.jpg" alt="Health, safety and environment" loading="lazy"></figure>
        <figure class="figure"><img src="assets/img/photos/hse-team.jpg" alt="Site health and safety team" loading="lazy"></figure>
      </div>
    </div>
  </div>
</section>

<section class="section band-alt">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">By the numbers</p>
      <h2 class="h2">Twenty-five years of practice.</h2>
    </div>
    <div class="grid g-4 reveal">
      <div class="contact-card"><span class="flag">Disciplines</span><h3>25</h3></div>
      <div class="contact-card"><span class="flag">Countries</span><h3>15</h3></div>
      <div class="contact-card"><span class="flag">Clients</span><h3>60+</h3></div>
      <div class="contact-card"><span class="flag">Ecological labs</span><h3>03</h3></div>
    </div>
  </div>
</section>
'''
        + cta("Want the full company profile?",
              "The reference portfolio documents the projects, partnerships and research behind "
              "these numbers.",
              (PDF, "Download portfolio"),
              ("contact.html", "Contact us")))


# ===========================================================================
#  CONTACT
# ===========================================================================
def contact_page():
    return (
        pagehead("Contact",
                 "Two offices. One engineering practice.",
                 "Tell us the constraint — capacity, compliance, cost or programme — and we will "
                 "tell you what can be demonstrated.",
                 "assets/img/hero/industrial-emissions.jpg",
                 "Industrial emissions above a lake")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="grid g-3 reveal">
      <div class="contact-card">
        <span class="flag">Egypt</span>
        <h3>Giza</h3>
        <dl>
          <div><dt>Address</dt><dd>Pyramids, Giza 12561</dd></div>
          <div><dt>Phone</dt><dd><a href="tel:{TEL_EG_HREF}">{TEL_EG}</a></dd></div>
        </dl>
      </div>
      <div class="contact-card">
        <span class="flag">Saudi Arabia</span>
        <h3>Riyadh</h3>
        <dl>
          <div><dt>Address</dt><dd>Olaya, Riyadh 12212</dd></div>
          <div><dt>Phone</dt><dd><a href="tel:{TEL_SA_HREF}">{TEL_SA}</a></dd></div>
        </dl>
      </div>
      <div class="contact-card">
        <span class="flag">Enquiries</span>
        <h3>Email</h3>
        <dl>
          <div><dt>General</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        </dl>
        <p style="margin-top:1.4rem">
          <a class="btn btn-accent" href="mailto:{EMAIL}?subject=Enquiry%20via%20emg-consulting-group.com">Compose an email {ARROW}</a>
        </p>
      </div>
    </div>

    <div class="split reveal" style="margin-top:clamp(3.5rem,7vw,6rem)">
      <div>
        <p class="eyebrow">What to send</p>
        <h2 class="h2">The more constraints you give us, the faster the answer.</h2>
        <ul class="checks" style="margin-top:1.4rem">
          <li>{TICK}<span>Scheme type and design capacity, if known</span></li>
          <li>{TICK}<span>The standard or consent you must meet</span></li>
          <li>{TICK}<span>Whether this is new build, retrofit or troubleshooting</span></li>
          <li>{TICK}<span>Programme and any lender or regulator deadlines</span></li>
        </ul>
      </div>
      <figure class="figure">
        <img src="assets/img/photos/location-map.jpg" alt="Regional location map" loading="lazy">
        <figcaption>Regional coverage</figcaption>
      </figure>
    </div>
  </div>
</section>
''')


# ===========================================================================
#  REFERENCE PORTFOLIO
#  Entries in data/reference-portfolio.json are transcribed from the slides
#  themselves — nothing is inferred beyond what each page states.
# ===========================================================================
CHAPTERS = [
    ("germany", "European practice &amp; partnerships",
     "EMG's work has been carried out alongside German and Belgian engineering houses since the "
     "early 2000s — agency agreements, joint bids and shared design review."),
    ("partnership", None, None),   # folded into the chapter above
    ("ksa", "Saudi Arabia",
     "Front-end engineering, hydraulic modelling, physical and CFD modelling, value engineering and "
     "capacity assessment for the Kingdom's water authorities and their contractors."),
    ("oman", "Oman",
     "Process design, dynamic simulation and commissioning support for the Sultanate's largest "
     "treatment and reclamation schemes."),
    ("yemen", "Yemen",
     "The Greater Aden water and sanitation utilities development programme — hydraulic modelling, "
     "impact assessment and institutional study."),
    ("egypt", "Egypt",
     "National programmes at home, including the EBRD-financed water pollution control works around "
     "Qarun Lake and the Armed Forces national services projects."),
    ("ecology", "Ecology, marine &amp; biodiversity",
     "Avifaunal baselines, marine habitat mapping and bathymetric survey delivered with Green Plus "
     "and EnviGlobe."),
    ("method", "Method — hazard &amp; operability",
     "How the studies are actually run: nodes, deviations, severity definitions and the worksheets "
     "behind a HAZOP deliverable."),
    ("training", "Training &amp; knowledge transfer",
     "Courses, diplomas and open workshops delivered for utilities, contractors and academies from "
     "1995 onwards."),
    ("teaching", "University teaching",
     "Undergraduate teaching and graduation project supervision in Egypt."),
    ("conference", "Conferences &amp; papers",
     "Invited lectures, accepted papers and conference contributions across the region and in Europe."),
    ("membership", "Professional standing",
     "Memberships held with international engineering and water bodies."),
]


def portfolio_page():
    import json
    data = json.load(open(os.path.join(ROOT, "data", "reference-portfolio.json"),
                          encoding="utf-8"))
    by_ch = {}
    for s in data:
        by_ch.setdefault(s["ch"], []).append(s)
    # the single German Water Partnership page belongs with the European chapter
    if "partnership" in by_ch:
        by_ch["germany"] = sorted(by_ch["germany"] + by_ch.pop("partnership"),
                                  key=lambda s: s["p"])

    nav, body = "", ""
    n = 0
    for key, title, blurb in CHAPTERS:
        if title is None or key not in by_ch:
            continue
        n += 1
        items = by_ch[key]
        nav += (f'        <li><a href="#ch-{key}"><span class="n">{n:02d}</span>'
                f'{title}</a></li>\n')
        entries = ""
        for s in items:
            meta = f'<p class="pf-meta">{s["meta"]}</p>' if s["meta"] else ""
            entries += f'''      <article class="pf-entry">
        <a class="pf-shot" href="assets/img/reference/view/page-{s["p"]:03d}.jpg" data-lb="{s["p"]}">
          <img src="assets/img/reference/thumbs/page-{s["p"]:03d}.jpg" alt="Reference portfolio page {s["p"]}" loading="lazy">
          <span class="pf-pg">P.{s["p"]:03d}</span>
        </a>
        <div>
          <h3>{s["t"]}</h3>
          {meta}
          <p>{s["d"]}</p>
        </div>
      </article>\n'''
        body += f'''    <section class="pf-chapter" id="ch-{key}">
      <header>
        <span class="count">Chapter {n:02d} &middot; {len(items)} page{"s" if len(items) != 1 else ""}</span>
        <h2>{title}</h2>
        {f'<p class="lede" style="margin-top:.8rem">{blurb}</p>' if blurb else ""}
      </header>
{entries}    </section>\n'''

    return (
        pagehead("Reference portfolio",
                 "The record, page by page.",
                 "Every page of EMG's 197-page reference portfolio, described from its own content "
                 "and grouped into chapters. Select any page to read it in full.",
                 "assets/img/hero/engineering-works.jpg",
                 "Engineering works")
        + f'''
<section class="section band-paper">
  <div class="wrap">
    <div class="hero-actions" style="margin-bottom:clamp(2.5rem,5vw,4rem)">
      <a class="btn btn-accent" href="{PDF}" download>{DOWNLOAD} Download the full portfolio (PDF, 20 MB)</a>
      <a class="btn btn-ghost" href="projects.html">Project summaries</a>
    </div>

    <div class="pf">
      <nav class="pf-nav" aria-label="Portfolio chapters">
        <h2>Chapters</h2>
        <ol>
{nav}        </ol>
      </nav>
      <div>
{body}      </div>
    </div>
  </div>
</section>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Portfolio page viewer">
  <button class="lb-close" aria-label="Close">&times;</button>
  <button class="lb-prev" aria-label="Previous page">&#8249;</button>
  <button class="lb-next" aria-label="Next page">&#8250;</button>
  <div style="display:grid; place-items:center">
    <img id="lb-img" src="" alt="">
    <p class="lb-cap" id="lb-cap"></p>
  </div>
</div>
''')


# ===========================================================================
#  BUILD
# ===========================================================================
PAGES = {
    "portfolio.html": (
        portfolio_page,
        "Reference portfolio — EMG Consulting Group",
        "All 197 pages of the EMG reference portfolio, described and grouped into chapters: "
        "projects in Saudi Arabia, Oman, Yemen and Egypt, ecology surveys, training and papers."),
    "services.html": (
        services_page,
        "Services — EMG Consulting Group",
        "Environmental and social impact assessment, remediation, pollution control, waste-to-energy "
        "and modelling, backed by process simulation, CFD, physical modelling and HAZOP study."),
    "projects.html": (
        projects_page,
        "Reference projects — EMG Consulting Group",
        "Reference projects across Egypt and the Gulf, from R&D pilot plants to 250,000 m³/day "
        "infrastructure for national water authorities and international contractors."),
    "expertise.html": (
        expertise_page,
        "Dr. Ahmed El-Zayat — EMG Consulting Group",
        "Founder profile and credentials: environmental sanitation and water resources expert, "
        "PhD in dynamic simulation and modelling for biological phosphorus removal."),
    "alliance.html": (
        alliance_page,
        "Environmental alliance — EMG Consulting Group",
        "EMG works alongside EnviGlobe in Egypt, Knollmann in Germany and the International Water "
        "Technology Association."),
    "about.html": (
        about_page,
        "About — EMG Consulting Group",
        "Founded in Egypt in 1999. Vision, strategy, quality management method and operational "
        "excellence of a specialised environmental engineering consultancy."),
    "contact.html": (
        contact_page,
        "Contact — EMG Consulting Group",
        "EMG Consulting Group offices in Giza, Egypt and Riyadh, Saudi Arabia."),
}


def build():
    os.chdir(ROOT)
    written = []
    for filename, (fn, title, desc) in PAGES.items():
        html = head(title, desc, filename) + header(filename) + fn() + FOOTER
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        written.append((filename, len(html)))

    # keep the hand-written homepage's shared chrome in step with the generator
    sync_home()
    for name, size in written:
        print(f"  {size/1024:6.1f} KB  {name}")


def sync_home():
    """Replace index.html's header block and footer with the generated ones."""
    path = os.path.join(ROOT, "index.html")
    html = open(path, encoding="utf-8").read()
    new_header = header("index.html").rstrip("\n")
    # header() ends by opening <main>; splice between the skip link and the hero
    html = re.sub(r'\n<!-- =+ HEADER =+ -->.*?<main id="main">',
                  "\n" + new_header.split("\n", 1)[1].rstrip(), html, flags=re.S)
    html = re.sub(r'\n</main>.*?</html>\s*$', "\n" + FOOTER.split("\n", 1)[1], html, flags=re.S)
    open(path, "w", encoding="utf-8").write(html)
    print(f"  {len(html)/1024:6.1f} KB  index.html (chrome synced)")


if __name__ == "__main__":
    build()
