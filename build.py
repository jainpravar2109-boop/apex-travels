#!/usr/bin/env python3
"""Apex Travels static site generator.
Edit the CONFIG block, then run:  python3 build.py   (outputs to ./site)
Drag the generated ./site folder into Netlify to deploy."""
import os, sys, json, shutil
from html import escape as esc

# ======================= CONFIG: single source of truth =======================
# Edit ONLY this block, then run:  python3 build.py   (add --strict to fail while blockers remain).
# Values still in [BRACKETS] or empty are LAUNCH BLOCKERS: they show visibly on the page and are listed by the build.
SITE = "https://www.apextravels.co.in"                   # canonical origin (canonical tags, sitemap, schema)
PORTAL_URL = "https://www.apextravelonline.com/login"    # existing B2B agent portal (separate system, linked only)
PHONE = "+91 88000 26112"            # display text (supplied by client)
PHONE_TEL = "+918800026112"          # DERIVED from PHONE as supplied (same digits, no spaces). Confirm.
EMAIL = "apextravels212@gmail.com"  # supplied by client. Confirm a Gmail address is the intended public email.
WA = "+91 88000 26112"                # display text (supplied by client)
WA_DIGITS = "918800026112"           # DERIVED from WA as supplied (digits only). Confirm this number is on WhatsApp.
ADDR = "1st Floor, PP TOWER, 113-118, Netaji Subhash Place, Pitampura, 110034, Delhi, India"   # supplied by client
HOURS = "10AM- 7PM"                   # supplied verbatim by client. Days of the week not stated: confirm.
POLICY_DATE = "[POLICY EFFECTIVE DATE]"      # shown on Privacy Policy and Terms
PRIVACY_CONTACT = "[PRIVACY CONTACT NAME]"   # responsible person named in the Privacy Policy
INSTAGRAM_URL = "https://www.instagram.com/apextravels.official/"   # exact URL supplied; empty = link hidden
LINKEDIN_URL = ""   # NOT SET. The URL supplied was a private admin dashboard. Paste the PUBLIC company page URL here; empty = link hidden
IATA_AGENT_CODE = ""   # NOT SET. Your numeric IATA agent code. The IATA credential in the footer appears ONLY when this is set. Optional: put the official IATA artwork you were issued at assets/iata-logo.svg or .png
IATA_LABEL = "IATA Accredited Agent"   # confirm the exact wording you are entitled to use (accredited vs certified)
OFFER_CRUISES = True   # NEEDS CONFIRMATION: set False if Apex does not arrange cruises (hides the sea-journeys band and video)
DISC = ("Charter flights are operated by duly authorised operators. Apex Travels acts as a travel "
        "coordination and facilitation desk and does not own or operate aircraft.")
# ===============================================================================
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
shutil.rmtree(OUT, ignore_errors=True)   # site/ is fully regenerated on every build
PH = {}

WA_ON = WA_DIGITS.strip().isdigit()
WA_URL = f"https://wa.me/{WA_DIGITS}?text=Hello%20Apex%20Travels%2C%20I%20would%20like%20to%20make%20an%20enquiry." if WA_ON else ""
UNSET = [n for n, v in [("PHONE", PHONE), ("EMAIL", EMAIL), ("WA", WA), ("ADDR", ADDR), ("HOURS", HOURS),
         ("POLICY_DATE", POLICY_DATE), ("PRIVACY_CONTACT", PRIVACY_CONTACT)] if "[" in v]
if "/admin" in LINKEDIN_URL:   # never publish a private admin URL
    print("WARNING: LINKEDIN_URL is an admin URL; ignored."); LINKEDIN_URL = ""
UNSET += (["PHONE_TEL"] if not PHONE_TEL.strip() else []) + (["WA_DIGITS"] if not WA_ON else [])
UNSET += (["INSTAGRAM_URL"] if not INSTAGRAM_URL.strip() else []) + (["LINKEDIN_URL"] if not LINKEDIN_URL.strip() else []) + (["IATA_AGENT_CODE"] if not IATA_AGENT_CODE.strip() else [])
def tel_html(): return f'<a href="tel:{esc(PHONE_TEL)}">{esc(PHONE)}</a>' if PHONE_TEL.strip() else esc(PHONE)
def mail_html(): return f'<a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a>' if "@" in EMAIL else esc(EMAIL)
def wa_html(t): return f'<a href="{WA_URL}">{esc(t)}</a>' if WA_ON else esc(t)
def wa_btn(label, cls="btn btn-line"): return f'<a class="{cls}" href="{WA_URL}">{label}</a>' if WA_ON else ""
def wa_float(): return f'<a class="wa" href="{WA_URL}" aria-label="Chat with Apex Travels on WhatsApp">WhatsApp</a>' if WA_ON else ""
def portal_btn(label, cls="btn"): return f'<a class="{cls}" href="{PORTAL_URL}" rel="noopener">{label}</a>'
SOCIALS = [("Instagram", INSTAGRAM_URL), ("LinkedIn", LINKEDIN_URL)]
def _soc(name, url, cls): return f'<a{(" class=%s" % chr(34) + cls + chr(34)) if cls else ""} href="{esc(url)}" target="_blank" rel="noopener noreferrer" aria-label="Apex Travels on {name} (opens in a new tab)">{name}</a>'
def social_links(cls="btn btn-line"): return "".join(_soc(n, u, cls) for n, u in SOCIALS if u.strip())
def social_footer():
    li = "".join(f"<li>{_soc(n, u, '')}</li>" for n, u in SOCIALS if u.strip())
    return f'<h2 class="fh">Follow us</h2><ul class="soc">{li}</ul>' if li else ""
def social_row(): return [("Follow us", " &middot; ".join(_soc(n, u, "") for n, u in SOCIALS if u.strip()))] if social_links() else []
def social_section():
    l = social_links("btn btn-line")
    return (f'<section class="sec alt tight"><div class="wrap social-band"><div><h2>Follow Apex Travels</h2><p class="lead">Find us on our official pages.</p></div><div class="cta-row">{l}</div></div></section>') if l else ""
AV_NOTE = '<p class="img-note">Illustrative image. Apex Travels does not own or operate aircraft.</p>'
def iata_strip():
    if not IATA_AGENT_CODE.strip(): return ""
    lg = next((f for f in ("iata-logo.svg", "iata-logo.png") if os.path.exists(os.path.join(ROOT, "assets", f))), None)
    im = f'<img src="images/{lg}" alt="IATA" height="44">' if lg else ""
    return f'<div class="wrap iata">{im}<p><strong>{esc(IATA_LABEL)}</strong> &middot; IATA agent code {esc(IATA_AGENT_CODE)}</p></div>'
def fill(t): return t.replace("{{EMAIL}}", esc(EMAIL)).replace("{{PHONE}}", esc(PHONE)).replace("{{PRIVACY_CONTACT}}", esc(PRIVACY_CONTACT))
def fallback():
    c = (["call " + PHONE] if PHONE_TEL.strip() else []) + (["message us on WhatsApp (" + WA + ")"] if WA_ON else []) + (["email " + EMAIL] if "@" in EMAIL else [])
    return "We could not send your request. Please try again" + (", or " + ", ".join(c) if c else " in a few minutes") + "."
def ld():
    d = {"@context": "https://schema.org", "@type": ["LocalBusiness", "TravelAgency"], "name": "Apex Travels", "url": SITE + "/",
         "logo": SITE + "/images/apex-logo.png", "image": SITE + "/images/og-image.png",
         "description": "Delhi-based travel company established in 2004 offering corporate and leisure travel, visa assistance, holiday packages, B2B travel services and private-aviation charter coordination.",
         "foundingDate": "2004", "address": {"@type": "PostalAddress", "addressLocality": "Delhi", "addressCountry": "IN"}, "areaServed": "IN"}
    if PHONE_TEL.strip(): d["telephone"] = PHONE_TEL
    if "@" in EMAIL: d["email"] = EMAIL
    sa = [u for u in (INSTAGRAM_URL, LINKEDIN_URL) if u.strip()]
    if sa: d["sameAs"] = sa
    return json.dumps(d, indent=1)
IMG_SPECS = {  # name: (width, height, brief). All slots are 2:3 portrait (arch frames). Recommended supply: the stated size or larger.
 "hero-home": (1600, 2400, "Home hero, centre arch. Skyline or landmark city at golden hour; no close-up people."),
 "leisure-travel": (1600, 2400, "Home hero, left arch; Corporate page. Overwater villas, lagoon or beach at sunset."),
 "hotels": (1600, 2400, "Home hero, right arch; Hotels page. Luxury resort or villa at dusk. Property release if identifiable."),
 "corporate-travel": (1600, 2400, "Home corporate section; Corporate page. Premium city skyline, rooftop or lounge at dusk."),
 "holiday-packages": (1600, 2400, "Home corporate section (small); Hotels page. Destination dining or waterfront at dusk."),
 "hero-aviation": (1600, 2400, "Home aviation feature; Private Aviation hero. Generic business jet. No Apex livery, no visible registration."),
}
IMG_WHERE = {"hero-home": "index.html hero (centre arch, eager)", "leisure-travel": "index.html hero (left arch); corporate-travel.html", "hotels": "index.html hero (right arch); hotels-packages.html",
 "corporate-travel": "index.html corporate section; corporate-travel.html", "holiday-packages": "index.html corporate section (small); hotels-packages.html", "hero-aviation": "index.html aviation feature; private-aviation.html hero (eager)"}
# Permission record. Add one line per supplied photo, e.g. "hero-home": "Photographer: A. Name; licence: Adobe Stock #123; model release: n/a"
_RX = "Supplied by client (received as '{}'). Source, photographer, licence and AI-generation status: NOT PROVIDED."
IMG_RIGHTS = {"hero-home": _RX.format("portofolio.jpeg"), "leisure-travel": _RX.format("Bora_Bora_Islands.jpeg"), "hotels": _RX.format("download__1_.jpeg"),
 "corporate-travel": _RX.format("download.jpeg"), "holiday-packages": _RX.format("download__2_.jpeg"), "hero-aviation": _RX.format("Private_Jet_Over_Tropical_Island_Chain.jpeg")}
GRADE = {"saturation": 0.92, "contrast": 1.03}          # one consistent, natural grade applied to every photo at build time
GRADE_OVERRIDE = {"hero-home": {"saturation": 0.90}, "corporate-travel": {"saturation": 0.86}, "holiday-packages": {"saturation": 0.84}}
FOCUS = {}   # optional crop focus per image, (x, y) from 0 to 1, e.g. {"hero-home": (0.7, 0.5)}; default centre
SRC_DIR = os.path.join(ROOT, "assets", "source-photos")   # your ORIGINALS; never copied to site/
WIDTHS = (480, 800, 1200, 1600)
def src_photo(n):
    for e in ("jpg", "jpeg", "png", "webp"):
        q = os.path.join(SRC_DIR, f"{n}.{e}")
        if os.path.exists(q): return q
def src_size(n):
    from PIL import Image
    with Image.open(src_photo(n)) as im: return im.size
def status_md(n):
    if not has_photo(n): return "**PLACEHOLDER**"
    w = src_size(n)[0]
    return f"supplied ({w}px wide" + (", **below the 1200px minimum for sharp results**)" if w < 1200 else ")")
def has_photo(n): return src_photo(n) is not None
UNLICENSED = [n for n in IMG_SPECS if has_photo(n) and "NOT PROVIDED" in IMG_RIGHTS.get(n, "NOT PROVIDED")]
_PLAN = {}
def plan(n):
    if n not in _PLAN:
        try: from PIL import Image, ImageOps, features
        except ImportError: sys.exit("Photos found in assets/source-photos but Pillow is missing. Run: pip install pillow")
        w, h, _ = IMG_SPECS[n]
        with Image.open(src_photo(n)) as im: sw, sh = ImageOps.exif_transpose(im).size
        cw = min(sw, int(sh * w / h)); ws = sorted({t for t in WIDTHS if t < cw} | {cw})
        _PLAN[n] = (ws, (["avif"] if features.check("avif") else []) + ["webp", "jpg"])
    return _PLAN[n]
def make_photos():
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
    for n, (w, h, _) in IMG_SPECS.items():
        if not has_photo(n): continue
        ws, exts = plan(n)
        im = ImageOps.exif_transpose(Image.open(src_photo(n))).convert("RGB")
        cw = min(im.width, int(im.height * w / h)); ch = int(cw * h / w)
        fx, fy = FOCUS.get(n, (.5, .5)); x = int((im.width - cw) * fx); y = int((im.height - ch) * fy)
        im = im.crop((x, y, x + cw, y + ch))
        g = {**GRADE, **GRADE_OVERRIDE.get(n, {})}
        im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(g["saturation"])).enhance(g["contrast"])
        os.makedirs(os.path.join(OUT, "images", "photos"), exist_ok=True)
        for t in ws:
            v = im.resize((t, round(t * h / w)), Image.LANCZOS) if t < im.width else im
            v = v.filter(ImageFilter.UnsharpMask(radius=0.8, percent=35, threshold=2))
            for e in exts:
                kw = {"avif": ("AVIF", {"quality": 55}), "webp": ("WEBP", {"quality": 78, "method": 6}), "jpg": ("JPEG", {"quality": 80, "optimize": True, "progressive": True})}[e]
                v.save(os.path.join(OUT, "images", "photos", f"{n}-{t}.{e}"), kw[0], **kw[1])

def W(path, text, base=OUT):
    p = os.path.join(base, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)

NAV = [("about.html", "About"), ("corporate-travel.html", "Corporate &amp; Leisure"),
       ("visa-assistance.html", "Visa"), ("hotels-packages.html", "Hotels &amp; Packages"),
       ("private-aviation.html", "Private Aviation"), ("b2b-corporate-travel.html", "B2B Desk")]
ALL = ["index.html"] + [n[0] for n in NAV] + ["contact.html", "privacy-policy.html", "terms-of-service.html"]

def img(n, alt, eager=False, sizes="(min-width:900px) 540px, 100vw"):
    PH[n] = alt
    w, h, _ = IMG_SPECS[n]
    at = 'decoding="async"' if eager == "normal" else ('fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"')
    if not has_photo(n):
        return f'<img src="images/{n}.svg" alt="{esc(alt)}" width="{w}" height="{h}" {at}>'
    ws, exts = plan(n)
    ss = lambda e: ", ".join(f"images/photos/{n}-{t}.{e} {t}w" for t in ws)
    srcs = "".join(f'<source type="image/{e}" srcset="{ss(e)}" sizes="{sizes}">' for e in exts if e != "jpg")
    return f'<picture>{srcs}<img src="images/photos/{n}-{ws[-1]}.jpg" srcset="{ss("jpg")}" sizes="{sizes}" alt="{esc(alt)}" width="{w}" height="{h}" {at}></picture>'

def btn(href, label, cls="btn"):
    return f'<a class="{cls}" href="{href}">{label}</a>'

def ul(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def sec(title, inner, intro="", cls="", id=""):
    i = f' id="{id}"' if id else ""
    p = f'<p class="lead">{intro}</p>' if intro else ""
    return f'<section class="sec {cls}"{i}><div class="wrap"><div class="sec-h"><h2>{title}</h2>{p}</div>{inner}</div></section>'

def cols(items, n=3, link=True):
    out = f'<div class="grid g{n}">'
    for it in items:
        h, p = it[0], it[1]
        l = f'<a class="more" href="{it[2]}">Learn more about {esc(h)}</a>' if len(it) > 2 else ""
        out += f'<article class="col"><h3>{h}</h3><p>{p}</p>{l}</article>'
    return out + "</div>"

def rows(items):
    return '<dl class="rows">' + "".join(f"<div><dt>{h}</dt><dd>{p}</dd></div>" for h, p in items) + "</dl>"

def hero(h1, sub, ctas, name, alt, dark=False, note=""):
    return (f'<section class="hero{" on-dark" if dark else ""}"><div class="wrap hero-g"><div><h1>{h1}</h1><p class="sub">{sub}</p>'
            f'<div class="cta-row">{ctas}</div></div><div class="hero-img">{img(name, alt, True, "(min-width:900px) 520px, 100vw")}{note}</div></div></section>')

def disclaimer():
    return f'<div class="wrap"><aside class="disclaimer" role="note"><strong>Important:</strong> {DISC}</aside></div>'

def cta_band(title="Plan your next journey with Apex.", text="Tell us where you are going. We will come back with clear, written options."):
    return (f'<section class="sec cta"><div class="wrap"><h2>{title}</h2><p class="lead">{text}</p>'
            f'<div class="cta-row">{btn("contact.html","Request a Quote","btn btn-acc")}{wa_btn("Chat on WhatsApp")}</div></div></section>')

def page(f, title, desc, body, schema=False, noindex=False):
    url = SITE + ("/" if f == "index.html" else "/" + f)
    robots = "noindex, follow" if noindex else "index, follow"
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == f else ""}>{l}</a></li>' for h, l in NAV)
    sc = f'<script type="application/ld+json">{ld()}</script>' if schema else ""
    foot_s = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    html = f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#B22D2D">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Apex Travels">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/images/og-image.png">
<script>try{{if(!sessionStorage.getItem("apexPre")&&!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("pre-on")}}catch(e){{}}</script>
<link rel="stylesheet" href="css/style.css">
<script src="js/main.js" defer></script>
{sc}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="pre" aria-hidden="true"><img src="images/apex-logo.png" alt="" width="150" height="150"></div>
<div class="util"><div class="wrap util-in"><p><span class="hide-s">Delhi &middot; Since 2004 &nbsp;&middot;&nbsp; </span>{tel_html()} &nbsp;&middot;&nbsp; {wa_html("WhatsApp")}</p><a href="{PORTAL_URL}" rel="noopener">B2B Agent Login</a></div></div>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="index.html" aria-label="Apex Travels home"><img src="images/apex-logo-128.png" alt="Apex Travels" width="56" height="56"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span></button>
<nav id="nav" class="nav" aria-label="Primary"><ul>{nav}</ul><div class="nav-actions"><a class="btn btn-line btn-sm" href="{PORTAL_URL}" rel="noopener">B2B Agent Login</a>{btn("contact.html","Request a Quote","btn btn-sm")}</div></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap fgrid">
<div><a class="brand" href="index.html" aria-label="Apex Travels home"><img src="images/apex-logo.png" alt="Apex Travels" width="96" height="96" loading="lazy"></a><p>Delhi-based travel company serving corporate, leisure and private-aviation clients since 2004.</p>{social_footer()}</div>
<div><h2>Services</h2><ul>{foot_s}</ul></div>
<div><h2>Contact</h2><ul><li>{tel_html()}</li><li>WhatsApp: {wa_html(WA)}</li><li>{mail_html()}</li><li>{ADDR}</li></ul></div>
<div><h2>Company</h2><ul><li><a href="{PORTAL_URL}" rel="noopener"><strong>B2B Agent Login</strong></a></li><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy-policy.html">Privacy Policy</a></li><li><a href="terms-of-service.html">Terms of Service</a></li></ul></div>
</div>
{iata_strip()}<div class="wrap fbase"><p>&copy; Apex Travels, Delhi. Established 2004.</p><p>{DISC}</p></div></footer>
{wa_float()}
</body>
</html>
'''
    W(f, html)

# ---------- forms ----------
def fld(label, name, typ="text", req=True, extra="", cls=""):
    opt = "" if req else " (optional)"
    r = " required" if req else ""
    return (f'<div class="field {cls}"><label for="{name}">{label}{opt}</label>'
            f'<input id="{name}" name="{name}" type="{typ}"{r} {extra}><span class="err"></span></div>')

def sel(label, name, opts, req=True):
    o = "".join(f'<option value="{v}">{t}</option>' for v, t in opts)
    r = " required" if req else ""
    return (f'<div class="field"><label for="{name}">{label}{"" if req else " (optional)"}</label>'
            f'<select id="{name}" name="{name}"{r}>{o}</select><span class="err"></span></div>')

def area(label, name, req=False, ph=""):
    r = " required" if req else ""
    o = "" if req else " (optional)"
    return (f'<div class="field"><label for="{name}">{label}{o}</label>'
            f'<textarea id="{name}" name="{name}" rows="4" placeholder="{ph}"{r}></textarea><span class="err"></span></div>')

def consent(extra=""):
    return ('<div class="field"><label class="inline"><input type="checkbox" name="consent" value="yes" required> '
            'I have read the <a href="privacy-policy.html">Privacy Policy</a> and agree to Apex Travels contacting me about this enquiry.</label>'
            '<span class="err"></span></div>')

PHONE_X = 'pattern="\\+?[0-9 ]{8,16}" data-msg="Enter a valid phone number, digits only (country code optional)." autocomplete="tel"'

def success(msg):
    return f'<div class="form-success" tabindex="-1" role="status"><h3>Thank you. Your request has been received.</h3><p>{msg}</p></div>'

def aviation_form():
    trip = "".join(f'<label class="inline"><input type="radio" name="trip-type" value="{v}"{" required" if i == 0 else ""}> {v}</label>'
                   for i, v in enumerate(["One-way", "Return", "Multi-city"]))
    budget = sel("Budget range", "budget", [("", "Prefer to discuss"), ("up-to-5-lakh", "Up to ₹5 lakh"), ("5-15-lakh", "₹5–15 lakh"),
                 ("15-40-lakh", "₹15–40 lakh"), ("40-lakh-plus", "Above ₹40 lakh")], False)
    return f'''<div class="form-wrap" id="quote"><form class="form" name="private-aviation-quote" method="POST" action="/thank-you.html" data-netlify="true" data-netlify-honeypot="bot-field" data-validate data-fallback="{esc(fallback())}">
<input type="hidden" name="form-name" value="private-aviation-quote">
<p hidden><label>Leave this field empty: <input name="bot-field"></label></p>
<div class="row two">{fld("Full name","full-name",extra='autocomplete="name"')}{fld("Company name","company",extra='autocomplete="organization"')}</div>
<div class="row two">{fld("Phone / WhatsApp","phone","tel",extra=PHONE_X)}{fld("Email","email","email",extra='autocomplete="email"')}</div>
<div class="row two">{fld("Route: from","route-from",extra='placeholder="e.g. Delhi"')}{fld("Route: to","route-to",extra='placeholder="e.g. Mumbai"')}</div>
<div class="row three">{fld("Travel date","travel-date","date")}{fld("Preferred departure time","departure-time","time")}{fld("Number of passengers","passengers","number",extra='min="1" max="50"')}</div>
<div class="row two">{fld("Luggage","luggage",extra='placeholder="e.g. 4 cabin bags, 2 checked"')}
<fieldset class="field"><legend>Trip type</legend><div class="radios">{trip}</div><span class="err"></span></fieldset></div>
{budget}
{area("Special requirements","requirements",ph="Multi-city legs, pets, medical needs, ground transport, hotel or visa support")}
{consent()}
<button class="btn btn-acc" type="submit">Request a charter quote</button>
<p class="note">We aim to respond to charter enquiries within 30 minutes during business hours.</p>
</form>{success("A member of the Apex team will review your request and get back to you.")}</div>'''

def contact_form():
    topics = sel("Enquiry type", "topic", [("general", "General travel enquiry"), ("b2b", "Corporate / B2B travel proposal"),
             ("visa", "Visa assistance"), ("holidays", "Hotels and holiday packages"), ("aviation", "Private aviation")])
    return f'''<div class="form-wrap" id="enquiry"><form class="form" name="contact-enquiry" method="POST" action="/thank-you.html" data-netlify="true" data-netlify-honeypot="bot-field" data-validate data-fallback="{esc(fallback())}">
<input type="hidden" name="form-name" value="contact-enquiry">
<p hidden><label>Leave this field empty: <input name="bot-field"></label></p>
<div class="row two">{fld("Full name","full-name",extra='autocomplete="name"')}{fld("Company name","company",req=False,extra='autocomplete="organization"')}</div>
<div class="row two">{fld("Phone / WhatsApp","phone","tel",extra=PHONE_X)}{fld("Email","email","email",extra='autocomplete="email"')}</div>
{topics}
{area("How can we help?","message",True,"Destinations, dates, number of travellers, or the proposal you need")}
{consent()}
<button class="btn btn-acc" type="submit">Send enquiry</button>
</form>{success("A member of the Apex team will review your enquiry and get back to you.")}</div>'''

# ---------- page bodies ----------
SERV = ["air ticketing", "hotels", "holiday packages", "visa assistance", "travel insurance", "corporate travel", "B2B travel services"]

def HL(*w): return " ".join(f'<span class="ln"><span>{t}</span></span>' for t in w)
ALT_H = "Skyline at sunset above a lit riverside promenade with a passenger ferry on the water"
ALT_L = "Thatched overwater villas on a turquoise lagoon at sunset"
ALT_R = "Beachfront resort with thatched cabanas and a curved pool at dusk"
ALT_C = "Rooftop infinity pool and lounge above a city skyline at dusk"
ALT_P = "Waterfront dining terrace at dusk with a traditional wooden boat on turquoise water"
ALT_A = "Business jet flying over a chain of tropical islands"
_S = "(min-width:960px) 20vw, 30vw"
home = f'''<section class="lh"><svg class="path" viewBox="0 0 1200 500" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M-20 450C250 400 430 130 760 210S1100 70 1240 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="1 10" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>
<div class="wrap lh-g"><div class="lh-copy"><p class="label">Delhi &middot; Established 2004</p>
<h1>{HL("Travel,", "managed with", "<em>precision.</em>")}</h1>
<p class="sub">Apex Travels is a Delhi-based travel company serving corporate, leisure, and private-aviation clients since 2004.</p>
<div class="cta-row">{btn("contact.html", "Request a Quote", "btn btn-acc")}{btn("private-aviation.html", "Explore Private Aviation", "btn btn-line")}</div></div>
<div class="arches">
<figure class="arch a1 m" style="--r:1.667" data-parallax=".05">{img("leisure-travel", ALT_L, "normal", _S)}{img("holiday-packages", ALT_P, "normal", _S)}</figure>
<figure class="arch a2 m" style="--r:1.967;--ph:6s" data-parallax="-.035">{img("hero-home", ALT_H, True, "(min-width:960px) 24vw, 36vw")}{img("corporate-travel", ALT_C, "normal", "(min-width:960px) 24vw, 36vw")}</figure>
<figure class="arch a3" data-parallax=".07">{img("hotels", ALT_R, "normal", _S)}</figure>
</div></div></section>'''
_tg = "".join(f"<span>{t}</span>" for t in ["Air ticketing", "Hotels", "Holiday packages", "Visa assistance", "Travel insurance", "Corporate travel", "B2B travel services", "Private aviation coordination"])
home += f'<div class="ticker" aria-hidden="true"><div class="tk"><div class="tg">{_tg}</div><div class="tg">{_tg}</div></div></div>'
home += '''<nav class="h-desks" aria-label="Our services"><ol class="wrap">
<li data-r><a href="corporate-travel.html"><span class="n">01</span><strong>Corporate &amp; Leisure Travel</strong><span>Flights, stays, visas and insurance, arranged by one team.</span></a></li>
<li data-r="1"><a href="private-aviation.html"><span class="n">02</span><strong>Apex Private Aviation</strong><span>Charter coordination and premium executive travel support.</span></a></li>
<li data-r="2"><a href="b2b-corporate-travel.html"><span class="n">03</span><strong>B2B Travel Desk</strong><span>Managed corporate travel, MICE and partner services.</span></a></li>
</ol></nav>'''
JOURNEYS = [
 ("island", "leisure-travel", ALT_L, "Island escapes", "Overwater villas, lagoons and private beaches", "holidays", "hotels-packages.html",
  "Quiet, well-planned escapes to island destinations, with flights, transfers and stays arranged around your dates.",
  ["Destination and property shortlist matched to your preferences", "Flights, boat or seaplane transfers and baggage planning", "Visa and travel insurance coordination", "One itinerary and one point of contact"]),
 ("resort", "hotels", ALT_R, "Resort retreats", "Beachfront resorts and private villas", "holidays", "hotels-packages.html",
  "Unhurried stays at resorts chosen for the setting, the service and how well they suit the people travelling.",
  ["Hotel options compared in writing before you decide", "Room category, inclusions and transfers confirmed for you", "Group and family room arrangements", "Support while you are away if plans change"]),
 ("city", "corporate-travel", ALT_C, "City and business stays", "Premium hotels and well-timed itineraries", "general", "corporate-travel.html",
  "Business travel that runs to time: the right hotel, sensible flights and transfers that match your schedule.",
  ["Air tickets with changes and re-issues handled", "Hotels matched to meeting locations and company policy", "Airport and city transfers", "Visa assistance for business trips"]),
 ("holiday", "holiday-packages", ALT_P, "Holiday packages", "Tailor-made itineraries for families and groups", "holidays", "hotels-packages.html",
  "Domestic and international holidays planned around your pace and budget, with every cost itemised.",
  ["Itineraries built to your dates and interests", "Flights, stays, transfers and sightseeing combined", "Family, honeymoon and group arrangements", "Visa and insurance handled alongside"]),
]
from urllib.parse import quote as _q
_cards = ""
for i, (k, slot, alt, title, tag, topic, page_, desc, det) in enumerate(JOURNEYS):
    href = f"contact.html?topic={topic}&amp;interest={_q(title)}#enquiry"
    lis = "".join(f"<li>{d}</li>" for d in det)
    _cards += (f'<li class="jc-li" data-r="{i}"><a class="jc" href="{href}" data-j="{k}" data-title="{esc(title)}" data-page="{page_}">'
               f'<span class="jc-frame">{img(slot, alt, False, "(min-width:1080px) 22vw, (min-width:760px) 44vw, 74vw")}</span>'
               f'<span class="jc-body"><strong>{title}</strong><span class="jc-tag">{tag}</span><span class="jc-more">View details</span></span></a>'
               f'<template id="j-{k}"><p class="jd-tag">{tag}</p><p>{desc}</p><h3>How we arrange it</h3><ul class="ticks">{lis}</ul><p class="small">Pricing is tailored to your dates and requirements. Enquire for a written quote.</p></template></li>')
home += f'''<section class="h-show"><div class="wrap"><div class="sec-h"><p class="label" data-r>Journeys we arrange</p><h2 data-r="1">Curated around how you <em>travel</em>.</h2>
<p class="lead" data-r="2">Select a journey to see how we arrange it, then enquire for a written quote.</p></div>
<ul class="jc-list">{_cards}</ul></div>
<dialog class="jd" aria-labelledby="jd-t"><div class="jd-in"><button class="jd-x" type="button" aria-label="Close details">&times;</button><figure class="jd-fig"></figure>
<div class="jd-tx"><h2 id="jd-t"></h2><div class="jd-body"></div><div class="cta-row"><a class="btn jd-enq" href="contact.html#enquiry">Enquire</a><a class="btn btn-line jd-more" href="contact.html">Service details</a></div></div></div></dialog></section>'''
if OFFER_CRUISES:
    home += f'''<section class="sea" aria-label="Sea journeys"><video class="sea-v" muted loop playsinline preload="none" poster="media/cruise-poster.jpg" data-mp4="media/cruise.mp4" data-webm="media/cruise.webm" aria-hidden="true" tabindex="-1"></video><div class="sea-shade"></div>
<div class="wrap"><div class="sea-in"><p class="label" data-r>Sea journeys</p><h2 data-r="1">Ocean voyages, <em>arranged</em> end to end.</h2>
<p class="lead" data-r="2">From choosing the right sailing to the flights, hotels, visas and transfers around it, we coordinate the whole journey. Tell us your dates and ports of interest and we will come back with clear options.</p>
<div class="cta-row" data-r="3">{btn("contact.html?topic=holidays&amp;interest=Sea%20journeys#enquiry", "Enquire about sea journeys", "btn btn-acc")}</div></div></div>
<button class="sea-btn" type="button" aria-label="Pause background video" hidden>Pause</button></section>'''
home += f'''<section class="h-av"><div class="wrap h-av-g"><div>
<p class="label" data-r>Apex Private Aviation</p><h2 data-r="1">Private aviation, <em>coordinated</em> with discretion.</h2>
<p class="lead" data-r="2">Apex Private Aviation helps businesses, promoters, and families arrange on-demand charter options and premium travel support through one point of contact.</p>
<ul class="cats" data-r="2"><li>Turboprop</li><li>Light jet</li><li>Midsize jet</li><li>Heavy jet</li></ul>
<p class="disc" data-r="3"><strong>Important:</strong> {DISC}</p>
<div class="cta-row" data-r="3">{btn("private-aviation.html#quote", "Request a charter quote", "btn btn-acc")}{btn("private-aviation.html", "How it works", "btn btn-ghost")}</div></div>
<div><figure class="h-avfig zoom" data-mask data-parallax=".05">{img("hero-aviation", ALT_A)}</figure>{AV_NOTE}</div>
</div></section>
<section class="h-how"><div class="wrap"><p class="label" data-r>How we work</p><h2 data-r="1">Clear options, then <em>precise</em> execution.</h2>
<ol class="h-steps">
<li data-r><span class="n">1</span><strong>Brief</strong><span>Tell us the route, dates, travellers and any special requirements.</span></li>
<li data-r="1"><span class="n">2</span><strong>Options</strong><span>We come back with clear, written options to compare.</span></li>
<li data-r="2"><span class="n">3</span><strong>Confirm</strong><span>We book, collect documents and send one consolidated itinerary.</span></li>
<li data-r="3"><span class="n">4</span><strong>Travel</strong><span>We stay reachable throughout, for changes and support.</span></li>
</ol></div></section>
<section class="h-aud"><div class="wrap h-aud-g">
<article data-r><h2>For companies</h2><p>Managed corporate travel, group and MICE movements, conferences and incentives, with reporting agreed with your finance team.</p>{btn("contact.html?topic=b2b#enquiry", "Request a corporate travel proposal", "btn btn-line")}</article>
<article data-r="1"><h2>For partner agencies</h2><p>Existing Apex partners book through our separate B2B portal. New to Apex? Our B2B desk can explain how partnership works.</p><div class="cta-row">{btn("b2b-corporate-travel.html", "About the B2B desk", "btn btn-line")}<a class="textlink" href="{PORTAL_URL}" rel="noopener">B2B Agent Login</a></div></article>
</div></section>'''
home += social_section()
home += cta_band("Plan your next journey with Apex.", "Air tickets, hotels, holiday packages, visas and insurance, all from one team. Tell us where you are going and we will come back with clear options.")

about = sec("About Apex Travels", rows([
    ("Who we are", "Apex Travels is a Delhi-based travel company established in 2004. We arrange air tickets, hotels, holiday packages, visas and travel insurance for individuals, families and companies."),
    ("How we work", "We keep the process simple: understand the requirement, present clear written options, confirm details accurately, and stay reachable until the traveller is home."),
    ("Corporate and B2B focus", "A large part of our work is for businesses and partner agencies that need dependable booking, consistent service and clear reporting."),
    ("Apex Private Aviation", "Our newest desk coordinates private-jet charters with authorised operators and adds premium ground and travel support. Apex Travels does not own or operate aircraft.")]),
    "A travel company built on accuracy and follow-through.")
about = f'<div class="pagehead"><div class="wrap"><h1>About Apex Travels</h1><p class="sub">Delhi-based. Established 2004. Built around dependable service.</p></div></div>' + about.replace("<h2>About Apex Travels</h2>", "<h2>Who we serve and how</h2>")
about += sec("Our Delhi base", '<p class="lead">Apex Travels has operated from Delhi since 2004, serving individuals, companies and partner agencies.</p><div class="cta-row">' + btn("contact.html", "Contact the team") + '</div>')
about += sec("Services", cols([("Travel essentials", "Air ticketing, hotels, holiday packages, visa assistance and travel insurance."), ("Corporate and B2B", "Managed travel for companies, MICE support and services for partner agencies."), ("Private aviation", "Charter coordination, aircraft-category guidance and premium executive travel support.")]), cls="alt")
about += cta_band()

corp = f'<div class="pagehead"><div class="wrap"><h1>Corporate &amp; Leisure Travel</h1><p class="sub">Flights, stays, visas and insurance, arranged for business and for time off.</p><div class="cta-row">{btn("contact.html?topic=general#enquiry","Request a Quote","btn btn-acc")}</div></div></div>'
corp += sec("Corporate travel", f'<div class="split"><div>{ul(["Domestic and international air ticketing, including changes and re-issues","Hotels matched to meeting locations, budgets and company policy","Airport and city transfers","Visa assistance for business trips","Travel insurance guidance","Support when plans change mid-trip"])}</div><div>{img("corporate-travel","Rooftop infinity pool and lounge above a city skyline at dusk")}</div></div>',
    "Business travel works when bookings are accurate, changes are handled quickly and someone is reachable. We act as that someone.")
corp += sec("Leisure and family travel", f'<div class="split"><div>{img("leisure-travel","Thatched overwater villas on a turquoise lagoon at sunset")}</div><div>{ul(["Domestic and international holiday planning","Family, honeymoon and milestone trips","Flights, hotels and transfers booked together","Visa and insurance handled alongside the itinerary"])}<p><a href="hotels-packages.html">See hotels and holiday packages</a></p></div></div>', cls="alt")
corp += sec("How it works", '<ol class="steps"><li><strong>Tell us the plan.</strong> Destinations, dates, travellers and budget.</li><li><strong>Review options.</strong> Itemised choices in writing.</li><li><strong>Confirm.</strong> We book and send consolidated documents.</li><li><strong>Travel with support.</strong> We stay reachable for changes.</li></ol>')
corp += cta_band()

visa = f'<div class="pagehead"><div class="wrap"><h1>Visa Assistance</h1><p class="sub">Accurate documentation and clear guidance, so your application is complete the first time.</p><div class="cta-row">{btn("contact.html?topic=visa#enquiry","Ask about a visa","btn btn-acc")}</div></div></div>'
visa += sec("What we help with", cols([("Document checklist", "A destination-specific list of what you need, tailored to your travel purpose."), ("Form guidance", "Help completing application forms accurately and consistently with your documents."), ("Appointments and submission", "Coordination of appointment slots and submission with the relevant visa centre or embassy."), ("Review and tracking", "A check of your file before submission and updates on progress as they are available.")], 4))
visa += sec("Before you apply", f'<p>Visa decisions are made solely by the relevant embassy, consulate or immigration authority. Apex Travels provides assistance with preparation and submission and cannot guarantee approval, processing times or fees set by authorities. Please apply well ahead of your travel date and avoid booking non-refundable travel before the visa is issued.</p>', cls="alt")
visa += cta_band("Need a visa for an upcoming trip?", "Share your destination and travel dates and we will outline the requirements.")

hotels = f'<div class="pagehead"><div class="wrap"><h1>Hotels &amp; Holiday Packages</h1><p class="sub">Stays and itineraries planned around how you actually travel.</p><div class="cta-row">{btn("contact.html?topic=holidays#enquiry","Request a Quote","btn btn-acc")}</div></div></div>'
hotels += sec("Hotels", f'<div class="split"><div>{ul(["Business and leisure hotels in India and abroad","Locations chosen against your meeting or sightseeing plans","Corporate rates and inclusions, where available","Group blocks for teams, events and weddings"])}</div><div>{img("hotels","Beachfront resort with thatched cabanas and a curved pool at dusk")}</div></div>')
hotels += sec("Holiday packages", '<div class="split"><div>' + img("holiday-packages", "Waterfront dining terrace at dusk with a traditional wooden boat on turquoise water") + '</div><div>' + cols([("Domestic", "Itineraries across India, from short breaks to extended family holidays."), ("International", "Flights, stays, transfers and sightseeing combined, with visa and insurance support."), ("Groups and customised trips", "Family reunions, corporate incentives and tailor-made plans.")], 1) + '</div></div>', "Every package is built to your dates, pace and budget, with all costs itemised.", cls="alt")
hotels += cta_band()

AV_SERV = [("Charter coordination", "We request options from authorised operators and present them side by side for your decision."),
    ("Aircraft-category guidance", "We match passenger count, baggage, sector length and airports to the right aircraft category."),
    ("Multi-city executive itineraries", "Sectors, timings and ground legs planned together for tight business schedules."),
    ("Empty-leg availability updates", "We notify you when positioning flights on your routes become available. Availability is not guaranteed and can change at short notice."),
    ("Airport meet-and-assist", "Arrival and departure assistance coordinated at the airport, where available."),
    ("Premium ground transport", "Chauffeured transfers timed to your flight."),
    ("Visa, hotel and itinerary support", "The wider trip around the flight, handled by the same desk."),
    ("Confidentiality", "Passenger and itinerary details are shared only with the parties needed to fulfil your request.")]
TBL = [("Turboprop", "6–9", "1,500–2,500 km", "Short regional sectors and shorter airfields", "Slower than jets; compact cabin"),
    ("Light jet", "4–8", "2,000–3,000 km", "Short to medium sectors between major cities", "Limited baggage space and cabin height"),
    ("Midsize jet", "7–9", "4,000–5,500 km", "Cross-country and regional international sectors", "Balance of cabin comfort, range and cost"),
    ("Heavy jet", "10–16", "6,500–11,000+ km", "Long-haul, larger groups, multi-sector international trips", "Highest cost; needs suitable airports and permissions")]
table = ('<div class="tbl-wrap" tabindex="0" role="region" aria-label="Aircraft category comparison"><table><caption>Indicative aircraft categories. Actual seats, range and cabin vary by aircraft type and operator.</caption>'
    '<thead><tr><th scope="col">Category</th><th scope="col">Typical seats</th><th scope="col">Indicative range (non-stop)</th><th scope="col">Best suited for</th><th scope="col">Considerations</th></tr></thead><tbody>'
    + "".join(f'<tr><th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in TBL) + "</tbody></table></div>")
av = hero("Private aviation, coordinated with discretion.",
    "Apex Private Aviation helps businesses, promoters, and families arrange on-demand charter options and premium travel support through one point of contact.",
    btn("#quote", "Request a charter quote", "btn btn-acc") + wa_btn("Chat on WhatsApp"),
    "hero-aviation", "Business jet flying over a chain of tropical islands", dark=True, note=AV_NOTE)
av += f'<div class="gap">{disclaimer()}</div>'
av += sec("What the desk handles", cols(AV_SERV, 4), "One point of contact for the flight and everything around it.")
av += sec("Choosing an aircraft category", table, "A practical starting point. We confirm exact aircraft, seats and range with the operator for your route.", cls="alt")
av += sec("How it works", '<ol class="steps"><li><strong>Share your requirement.</strong> Use the form, WhatsApp or phone.</li><li><strong>Receive options.</strong> We source from authorised operators and recommend a category.</li><li><strong>Review the quote.</strong> Written pricing, aircraft and operator details, and terms.</li><li><strong>Confirm.</strong> Payment and documentation as per the operator\'s terms.</li><li><strong>Fly.</strong> Ground and airport support coordinated; we remain your contact.</li></ol>')
av += (f'<section class="sec alt" id="quote-sec"><div class="wrap narrow"><div class="sec-h"><h2>Request a charter quote</h2><p class="lead">Share the details you have. We will ask for anything missing.</p></div>'
       f'{disclaimer().replace("<div class=\"wrap\">","<div>",1)}{aviation_form()}'
       f'<p class="alt-contact">Prefer to talk? {wa_btn("Message us on WhatsApp")} Call {tel_html()}.</p></div></section>')

b2b = f'<div class="pagehead"><div class="wrap"><h1>B2B &amp; Corporate Travel Desk</h1><p class="sub">Managed travel for HR heads, admin and travel managers, CFOs and partner agencies.</p><div class="cta-row">{btn("contact.html?topic=b2b#enquiry","Request a corporate travel proposal","btn btn-acc")}{portal_btn("B2B Agent Login","btn btn-line")}</div></div></div>'
b2b += sec("Existing partners: use the B2B booking portal", f'<p>Registered Apex partners and agents book through our separate B2B portal at apextravelonline.com. Sign-in happens on the portal itself; this website does not handle agent logins or passwords. Not a partner yet? Request a corporate travel proposal below.</p><div class="cta-row">{portal_btn("B2B Agent Login","btn")}</div>', cls="alt tight")
b2b += sec("What the desk covers", cols([
    ("Corporate travel management", "A single desk for bookings, changes, approvals and support across your travel programme."),
    ("Employee travel", "Flights, hotels and transfers for staff and leadership, aligned to your travel policy."),
    ("Group travel", "Block bookings and coordinated movement for teams of any size."),
    ("MICE", "Meetings, incentives, conferences and events, with logistics managed end to end."),
    ("Conference and incentive travel", "Delegate travel, accommodation and on-ground arrangements."),
    ("Visa support", "Documentation guidance and submission coordination for business travellers."),
    ("Hotel and ground transport", "Hotel selection and chauffeured transfers matched to schedules."),
    ("Travel reporting", "Periodic reports by employee, department, route or supplier, in formats agreed with your finance team."),
    ("Partner collaboration", "Fulfilment support for travel agencies and partners who need a reliable Delhi desk.")]))
b2b += sec("Who the desk is for", cols([("HR and admin", "Predictable service for employee travel and relocation."), ("CFOs and finance", "Travel reporting agreed with your finance team to support reconciliation."), ("Travel managers and partner agencies", "A dependable fulfilment desk with clear communication.")]), cls="alt")
b2b += cta_band("Request a corporate travel proposal", "Tell us your travel volumes and requirements. We will respond with a structured proposal.")

contact = f'<div class="pagehead"><div class="wrap"><h1>Contact Apex Travels</h1><p class="sub">Tell us what you need. We respond during business hours.</p></div></div>'
contact += (f'<section class="sec"><div class="wrap split"><div><h2>Get in touch</h2>{rows([("Phone",tel_html()),("WhatsApp",wa_html(WA)),("Email",mail_html()),("Address",ADDR),("Business hours",HOURS)]+social_row())}'
    f'<p class="small">For private-jet charter, use the <a href="private-aviation.html#quote">charter quote form</a>.</p></div><div><h2>Send an enquiry</h2>{contact_form()}</div></div></section>')

def legal(f, title, desc, h1, secs):
    body = f'<div class="pagehead"><div class="wrap"><h1>{h1}</h1><p class="sub">Effective date: {POLICY_DATE}</p></div></div><section class="sec"><div class="wrap narrow prose">'
    body += "<!-- Draft text. Have it reviewed by qualified legal counsel before publication. -->"
    for h, ps in secs:
        body += f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps)
    page(f, title, desc, fill(body + "</div></section>"))

# ---------- write pages ----------
page("index.html", "Apex Travels Delhi | Corporate Travel & Private Aviation Desk",
     "Delhi-based travel company since 2004. Corporate and leisure travel, visas, holiday packages, B2B travel desk and Apex Private Aviation charter coordination.", home, True)
page("about.html", "About Apex Travels | Delhi Travel Company Since 2004",
     "Apex Travels is a Delhi-based travel company established in 2004, serving corporate, leisure, B2B and private-aviation clients with accurate, accountable service.", about)
page("corporate-travel.html", "Corporate & Leisure Travel Services in Delhi | Apex Travels",
     "Corporate travel management and premium leisure travel from Delhi: air tickets, hotels, visas, insurance and ground transport handled by one team.", corp)
page("visa-assistance.html", "Visa Assistance Services in Delhi | Apex Travels",
     "Visa assistance from Delhi: document checklists, form guidance, appointment coordination and file review for business and leisure travellers.", visa)
page("hotels-packages.html", "Hotels & Holiday Packages from Delhi | Apex Travels",
     "Hotel bookings and domestic and international holiday packages from Delhi, planned around your dates and budget with itemised pricing.", hotels)
page("private-aviation.html", "Private Jet Charter Coordination India | Apex Private Aviation",
     "Apex Private Aviation coordinates private-jet charter options from authorised operators for businesses, promoters and families. Request a quote.", av)
page("b2b-corporate-travel.html", "B2B & Corporate Travel Desk India | Apex Travels",
     "Corporate travel management, MICE, group travel, visa support and travel reporting for HR, admin, finance teams and partner agencies in India.", b2b)
page("contact.html", "Contact Apex Travels | Request a Travel Quote in Delhi",
     "Contact Apex Travels in Delhi for corporate travel, visas, holiday packages, B2B proposals and private-aviation charter enquiries.", contact, True)

legal("privacy-policy.html", "Privacy Policy | Apex Travels", "How Apex Travels collects, uses and protects personal information submitted through apextravels.co.in.", "Privacy Policy", [
 ("Who we are", ["Apex Travels (&ldquo;we&rdquo;, &ldquo;us&rdquo;), based in Delhi, India, operates apextravels.co.in. This policy explains how we handle personal data you give us through this website, email, phone or WhatsApp."]),
 ("Information we collect", ["Details you submit through our forms or send to us: name, company, phone number, email, and travel details such as routes, dates, passenger numbers, luggage and special requirements.", "For bookings and visa work we may also need identity and passport details. We collect these only when needed and through the channel we specify.", "Our hosting and form providers may record technical data such as IP address and browser type in server logs."]),
 ("How we use it", ["To respond to enquiries, prepare quotes, make and manage bookings, assist with visas and insurance, meet legal, tax and accounting obligations, and send service communications about your enquiry. We do not sell personal data."]),
 ("Who we share it with", ["Only as needed to deliver your request: airlines, hotels, charter operators, ground handlers, embassies and visa centres, insurers, payment providers, and technology providers that host this site and process forms. We may disclose data where required by law or by a competent authority."]),
 ("Retention", ["We keep personal data for as long as needed for the purposes above and to meet legal and accounting obligations, then delete or anonymise it."]),
 ("Your rights", ["Under the Digital Personal Data Protection Act, 2023 and applicable rules, you may request access to, correction or erasure of your personal data, withdraw consent, and seek grievance redressal. Write to {{EMAIL}}."]),
 ("Security", ["We use reasonable safeguards to protect personal data. No method of transmission or storage is completely secure."]),
 ("Cookies", ["This website does not currently set advertising or tracking cookies. If analytics tools are added, this policy will be updated."]),
 ("Children", ["Our services are directed at adults. Travel for minors is arranged through a parent or guardian."]),
 ("Grievance contact and changes", ["Grievance contact: {{PRIVACY_CONTACT}}, {{EMAIL}}, {{PHONE}}. We may update this policy and will revise the date above when we do."])])

legal("terms-of-service.html", "Terms of Service | Apex Travels", "Terms governing use of the Apex Travels website and the travel, visa and private-aviation coordination services offered by Apex Travels.", "Terms of Service", [
 ("Acceptance", ["By using this website or our services you agree to these terms. If you do not agree, please do not use them."]),
 ("Our role", ["Apex Travels acts as an agent and coordinator between you and independent suppliers such as airlines, hotels, ground operators, insurers and charter operators. Each supplier&rsquo;s own terms, fare rules and cancellation policies apply to the services it provides."]),
 ("Private aviation", [DISC, "Aircraft availability, pricing, permissions, airport slots, crew, weather and regulatory requirements are determined by the operator and authorities. Quotes are indicative until confirmed in writing by the operator and accepted by you. The operator is responsible for operating the flight, and its terms, including cancellation and refund terms, govern the charter."]),
 ("Quotes and bookings", ["Prices and availability are subject to change until booking is confirmed and payment is received. Taxes, airport charges and supplier fees are as stated in the written quote."]),
 ("Payments, cancellations and refunds", ["Cancellations and refunds follow the applicable supplier rules. Any Apex Travels service fee will be communicated to you in writing before booking."]),
 ("Visa assistance", ["Visa decisions rest solely with the relevant authorities. We do not guarantee approval, timelines or fees. You are responsible for the accuracy and completeness of the documents and information you provide."]),
 ("Travel insurance", ["Insurance is issued by the insurer on the terms of its policy. Please read the policy wording for cover, exclusions and claims procedures."]),
 ("Traveller responsibilities", ["You are responsible for valid travel documents, visas, health and entry requirements, and for arriving on time."]),
 ("Limitation of liability", ["To the extent permitted by law, Apex Travels is not liable for acts or omissions of independent suppliers, for events beyond reasonable control, or for indirect or consequential loss. Nothing in these terms excludes liability that cannot be excluded under applicable law."]),
 ("Website use", ["Content on this website is owned by or licensed to Apex Travels and may not be copied or reused without permission."]),
 ("Governing law", ["These terms are governed by the laws of India. Courts at Delhi have exclusive jurisdiction, subject to applicable law."]),
 ("Contact", ["{{EMAIL}} &middot; {{PHONE}}"])])

# ---------- assets ----------
# Brand colours live ONLY here, as CSS custom properties. Brand red #C41210 was sampled from the
# "Sign In" button in the B2B portal screenshot (pixel value rgb(196,18,16)).
CSS = r""":root{--red:#B22D2D;--red-d:#8F2323;--red-l:#FF9C97;--char:#1F2328;--ink:#262B31;--mut:#555D66;--grey:#F7F5F2;--line:#E3DED7;--white:#FFFFFF;--serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:5.5rem}
body{margin:0;font:1rem/1.65 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--white)}
img{max-width:100%;height:auto;display:block;background:var(--grey)}picture{display:block}a{color:var(--red)}
.wrap{width:min(1120px,100% - 2.5rem);margin-inline:auto}.narrow{max-width:780px}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem 1rem;z-index:100}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}.on-dark :focus-visible{outline-color:#fff}
h1,h2,h3{color:var(--char);line-height:1.18;letter-spacing:-.015em;margin:0 0 .6em}
h1{font-size:clamp(2.2rem,5.5vw,3.7rem);font-weight:700}h2{font-size:clamp(1.55rem,3.2vw,2.2rem)}h3{font-size:1.1rem}
.on-dark{color:#d5d9de}.on-dark h1,.on-dark h2,.on-dark h3{color:#fff}.on-dark a:not(.btn){color:#fff}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:.6rem 1.35rem;border-radius:4px;font:600 1rem/1.2 inherit;text-decoration:none;border:2px solid var(--red);background:var(--red);color:#fff;cursor:pointer;transition:background-color .2s,color .2s,border-color .2s,transform .2s,box-shadow .2s}
.btn:hover{background:var(--red-d);border-color:var(--red-d);transform:translateY(-2px);box-shadow:0 6px 16px rgba(31,35,40,.18)}.btn:active{transform:none;box-shadow:none}.btn-sm{padding:.55rem 1rem;font-size:.92rem}
.btn-line{background:transparent;color:var(--red)}.btn-line:hover{background:var(--red);border-color:var(--red);color:#fff}
.on-dark .btn-line{color:#fff;border-color:#fff}.on-dark .btn-line:hover{background:#fff;border-color:#fff;color:var(--char)}
.btn[disabled]{opacity:.6;cursor:progress;transform:none;box-shadow:none}
.cta-row{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.5rem}
.site-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.97);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;min-height:4.75rem}
.brand{display:inline-block;line-height:0}.brand img{height:56px;width:56px;border-radius:3px;background:none}
.menu-btn{background:none;border:0;padding:.85rem;cursor:pointer}
.menu-btn span,.menu-btn span::before,.menu-btn span::after{display:block;width:24px;height:2px;background:var(--char);position:relative;content:"";transition:transform .25s,top .25s,background-color .25s}
.menu-btn span::before{top:-7px;position:absolute}.menu-btn span::after{top:7px;position:absolute}
.menu-btn[aria-expanded=true] span{background:transparent}.menu-btn[aria-expanded=true] span::before{top:0;transform:rotate(45deg)}.menu-btn[aria-expanded=true] span::after{top:0;transform:rotate(-45deg)}
.nav{position:absolute;left:0;right:0;top:100%;background:#fff;padding:1rem 1.25rem 1.5rem;border-bottom:1px solid var(--line);box-shadow:0 14px 24px rgba(0,0,0,.07);max-height:calc(100vh - 4.25rem);overflow:auto;visibility:hidden;opacity:0;transform:translateY(-8px);transition:opacity .25s ease,transform .25s ease,visibility 0s linear .25s}
.nav.open{visibility:visible;opacity:1;transform:none;transition-delay:0s}
.nav ul{list-style:none;margin:0 0 1rem;padding:0}.nav li a{display:block;padding:.75rem 0;color:var(--ink);text-decoration:none;font-weight:500;border-bottom:1px solid var(--line)}
.nav li a[aria-current=page]{color:var(--red);font-weight:700}.nav-actions{display:grid;gap:.6rem}.nav-actions .btn:not(.btn-line){order:-1}
@media(min-width:1160px){.menu-btn{display:none}.nav{position:static;display:flex;align-items:center;gap:1.2rem;padding:0;border:0;box-shadow:none;background:none;max-height:none;overflow:visible;visibility:visible;opacity:1;transform:none}.nav ul{display:flex;gap:1.1rem;margin:0}.nav li a{border:0;padding:.3rem 0;font-size:.9rem}.nav li a:hover{color:var(--red)}.nav-actions{display:flex;gap:.6rem}.nav-actions .btn:not(.btn-line){order:0}}
.hero{background:linear-gradient(180deg,#fff,#f6f6f7);padding:clamp(3rem,8vw,6rem) 0}.hero.on-dark{background:var(--char)}.hero-g{display:grid;gap:2.5rem;align-items:center}
.sub{font-size:1.15rem;max-width:36rem;margin:0;color:var(--mut)}.on-dark .sub{color:#d5d9de}.hero h1{max-width:14ch}.hero-img img{border-radius:4px;aspect-ratio:3/2;object-fit:cover;width:100%}
@media(min-width:900px){.hero-g{grid-template-columns:1.1fr .9fr}}
.pagehead{background:var(--grey);border-bottom:1px solid var(--line);padding:clamp(2.5rem,6vw,4.5rem) 0}.pagehead h1{font-size:clamp(2rem,4.5vw,3rem);max-width:none}.pagehead h1::after{content:"";display:block;width:3rem;height:3px;background:var(--red);margin-top:.8rem}
.sec{padding:clamp(3rem,7vw,5.5rem) 0}.alt{background:var(--grey)}.dark{background:var(--char)}.tight{padding:2.5rem 0}.gap{padding-top:2rem}
.sec-h{max-width:44rem;margin-bottom:2rem}.lead{font-size:1.1rem;color:var(--mut);margin:0}.on-dark .lead{color:#d5d9de}
.cta{background:var(--red);color:#fff}.cta h2{color:#fff}.cta .lead{color:#fff}.cta .btn{background:#fff;border-color:#fff;color:var(--red)}.cta .btn:hover{background:var(--char);border-color:var(--char);color:#fff}.cta .btn-line{background:transparent;border-color:#fff;color:#fff}.cta .btn-line:hover{background:#fff;color:var(--red)}.cta :focus-visible{outline-color:#fff}
.grid{display:grid;gap:2rem 1.75rem}@media(min-width:700px){.g2,.g3,.g4{grid-template-columns:repeat(2,1fr)}}@media(min-width:1000px){.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}}
.col{border-top:3px solid var(--red);padding-top:1rem}.col p{margin:0 0 .8rem;color:var(--mut)}.more{font-weight:600}
.rows{margin:0;display:grid;gap:0 3rem}@media(min-width:800px){.rows{grid-template-columns:1fr 1fr}}
.rows div{border-top:1px solid var(--line);padding:1.1rem 0}.rows dt{font-weight:700;color:var(--char)}.rows dd{margin:.25rem 0 0;color:var(--mut)}
.split{display:grid;gap:2.5rem;align-items:center}@media(min-width:900px){.split{grid-template-columns:1fr 1fr}}.split img{border-radius:4px;aspect-ratio:3/2;object-fit:cover;width:100%}
.ticks{list-style:none;padding:0;margin:1.25rem 0}.ticks li{padding:.35rem 0 .35rem 1.5rem;position:relative}.ticks li::before{content:"";position:absolute;left:0;top:.95rem;width:.65rem;height:2px;background:var(--red)}.on-dark .ticks li::before{background:var(--red-l)}
.small{font-size:.92rem}.steps{padding-left:1.25rem;display:grid;gap:1rem;max-width:44rem}.steps li::marker{font-weight:700;color:var(--red)}
.disclaimer{border-left:4px solid var(--red);background:#fdf3f2;padding:1rem 1.25rem;color:var(--ink);font-size:1.02rem;margin-bottom:1rem}
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);background:#fff}table{border-collapse:collapse;width:100%;min-width:720px}caption{caption-side:bottom;text-align:left;padding:.8rem 1rem;font-size:.9rem;color:var(--mut)}
th,td{padding:.9rem 1rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}thead th{background:var(--char);color:#fff}tbody th{color:var(--char)}
.form{display:grid;gap:1.1rem;margin-top:1rem}.row{display:grid;gap:1.1rem}@media(min-width:700px){.row.two{grid-template-columns:1fr 1fr}.row.three{grid-template-columns:repeat(3,1fr)}}
.field{border:0;padding:0;margin:0;min-width:0}label,legend{display:block;font-weight:600;margin-bottom:.35rem;padding:0}
input,select,textarea{width:100%;padding:.75rem .85rem;border:1px solid #8e98a3;border-radius:4px;font:inherit;background:#fff;color:var(--ink)}
input[type=checkbox],input[type=radio]{width:auto;margin-right:.5rem}.inline{display:flex;align-items:flex-start;font-weight:400}.radios{display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;padding-top:.5rem}
[aria-invalid=true]{border-color:#b3261e}.err{display:block;color:#b3261e;font-size:.88rem}.note{color:var(--mut);font-size:.95rem;margin:0}
.form-error{background:#fdf3f2;border:1px solid var(--red);border-radius:4px;padding:1rem}.form-success{display:none;background:#eef7f0;border:1px solid #8fc19d;padding:1.5rem;border-radius:4px}.form-success.show{display:block}.form-wrap form[hidden]{display:none}
.alt-contact{margin-top:2rem}.prose h2{font-size:1.3rem;margin-top:2rem}
.site-footer{background:var(--grey);border-top:3px solid var(--red);padding-top:3.5rem}.fgrid{display:grid;gap:2rem}@media(min-width:560px){.fgrid{grid-template-columns:1fr 1fr}}@media(min-width:960px){.fgrid{grid-template-columns:1.4fr 1fr 1fr 1.3fr}}
.site-footer .brand img{height:96px;width:96px;border-radius:3px;margin-bottom:1rem}.site-footer h2{font-size:1rem}.site-footer ul{list-style:none;padding:0;margin:0}.site-footer li{padding:.2rem 0}.site-footer a{color:var(--ink)}.site-footer a:hover{color:var(--red)}
.fbase{border-top:1px solid var(--line);margin-top:2.5rem;padding:1.5rem 0 5rem;font-size:.9rem;color:var(--mut)}.fbase p{margin:.3rem 0}
.wa{position:fixed;right:1rem;bottom:1rem;z-index:60;background:#0f7a43;color:#fff;padding:.75rem 1.2rem;border-radius:999px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:transform .2s,background-color .2s}.wa:hover{background:#0b6236;transform:translateY(-2px)}
.img-note{font-size:.85rem;color:var(--mut);margin:.5rem 0 0}.on-dark .img-note{color:#d5d9de}
.social-band{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem 2rem}.social-band h2{font-size:1.4rem;margin:0 0 .3rem}.social-band .cta-row{margin:0}
.soc{display:flex;flex-wrap:wrap;gap:.2rem 1.2rem}.site-footer .fh{margin-top:1.25rem}
@media(prefers-reduced-motion:no-preference){
@keyframes rise{from{opacity:0;transform:translateY(14px)}}
.hero-g>div:first-child>*,.pagehead .wrap>*{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
.hero-g>div:first-child>.sub,.pagehead .wrap>.sub{animation-delay:.08s}.hero-g>div:first-child>.cta-row,.pagehead .wrap>.cta-row{animation-delay:.16s}
.js-ready .reveal{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}.js-ready .reveal.in{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}"""

JS = r"""(()=>{
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const b=document.querySelector('.menu-btn'),n=document.getElementById('nav');
const setOpen=o=>{n.classList.toggle('open',o);b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Close menu':'Open menu')};
b.addEventListener('click',()=>setOpen(!n.classList.contains('open')));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&n.classList.contains('open')){setOpen(false);b.focus()}});
n.addEventListener('click',e=>{if(e.target.closest('a'))setOpen(false)});
/* Scroll reveal: progressive enhancement. The js-ready class is added only after setup succeeds,
   so content is always visible if this script fails, is blocked, or motion is reduced. */
if(!reduce&&'IntersectionObserver' in window){
 const els=[...document.querySelectorAll('.sec-h,.col,.rows>div,.split>*,.tbl-wrap,.steps li,.disclaimer,.form-wrap,.cta .wrap>*')];
 els.forEach(el=>{el.classList.add('reveal');el.style.transitionDelay=Math.min([...el.parentNode.children].indexOf(el),4)*70+'ms';if(el.getBoundingClientRect().top<innerHeight*.92)el.classList.add('in')});
 document.documentElement.classList.add('js-ready');
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
 els.forEach(el=>{if(!el.classList.contains('in'))io.observe(el)});
}
const today=new Date().toISOString().slice(0,10);
document.querySelectorAll('input[type=date]').forEach(i=>i.min=today);
const q=new URLSearchParams(location.search),topic=document.querySelector('select[name=topic]');
if(topic&&q.get('topic'))topic.value=q.get('topic');
document.querySelectorAll('form[data-validate]').forEach(f=>{
 f.noValidate=true;
 const ok=f.parentElement.querySelector('.form-success');
 const msg=el=>{const v=el.validity;return v.valueMissing?(el.type==='checkbox'?'Please tick this box to continue.':'This field is required.'):v.patternMismatch?(el.dataset.msg||'Please check this value.'):v.typeMismatch?'Please enter a valid value.':(v.rangeUnderflow||v.rangeOverflow)?'Please enter a number within the allowed range.':v.badInput?'Please enter a valid value.':''};
 const show=el=>{const s=el.closest('.field')?.querySelector('.err');if(s)s.textContent=el.validity.valid?'':msg(el);el.setAttribute('aria-invalid',String(!el.validity.valid))};
 const clearErr=()=>f.querySelector('.form-error')?.remove();
 const showErr=t=>{clearErr();const d=document.createElement('div');d.className='form-error';d.setAttribute('role','alert');d.tabIndex=-1;d.textContent=t;f.querySelector('[type=submit]').before(d);d.focus()};
 f.addEventListener('focusout',e=>{if(e.target.willValidate)show(e.target)});
 f.addEventListener('input',e=>{if(e.target.willValidate&&e.target.getAttribute('aria-invalid')==='true')show(e.target)});
 f.addEventListener('submit',async e=>{
  e.preventDefault();clearErr();
  const els=[...f.elements].filter(el=>el.willValidate);
  els.forEach(show);
  const bad=els.find(el=>!el.validity.valid);
  if(bad){bad.focus();return}
  const btn=f.querySelector('[type=submit]'),label=btn.textContent;
  btn.disabled=true;btn.textContent='Sending…';
  const ctl=new AbortController(),t=setTimeout(()=>ctl.abort(),20000);
  try{
   const r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString(),signal:ctl.signal});
   clearTimeout(t);
   if(!r.ok)throw new Error('HTTP '+r.status);
   f.hidden=true;ok.classList.add('show');ok.focus();   /* success is shown ONLY after a successful response */
  }catch(_){
   clearTimeout(t);btn.disabled=false;btn.textContent=label;
   showErr(f.dataset.fallback||'We could not send your request. Please try again.');
  }
 });
});
})();"""

CSS += r"""/* ===== Luxury layer: editorial type, photo frames, restrained motion ===== */
h1,h2,h3{font-family:var(--serif);font-weight:500}h1 em,h2 em{font-style:italic;color:var(--red)}
.label{display:flex;align-items:center;gap:.75rem;margin:0 0 1.25rem;font-size:.9rem;font-weight:600;color:var(--mut)}.label::before{content:"";width:2rem;height:2px;background:var(--red)}
.btn{border-radius:2px;position:relative;overflow:hidden}.btn::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.3) 50%,transparent 70%);transform:translateX(-130%);transition:transform .8s ease}.btn:hover::after{transform:translateX(130%)}
.util{background:var(--char);color:#e6e8eb;font-size:.85rem}.util-in{display:flex;justify-content:space-between;align-items:center;gap:1rem;min-height:2.25rem}.util p{margin:0}.util a{color:#fff;text-decoration:none}.util a:hover{text-decoration:underline}.util :focus-visible{outline-color:#fff}
@media(max-width:600px){.hide-s{display:none}}
.site-header{transition:box-shadow .3s}.site-header.scrolled{box-shadow:0 6px 24px rgba(21,24,28,.09)}.brand img{transition:width .3s,height .3s}.site-header.scrolled .brand img{width:46px;height:46px}
.hero-img img,.split img{aspect-ratio:4/5}.img-note{font-size:.85rem;color:var(--mut);margin:.5rem 0 0}.on-dark .img-note{color:#d5d9de}
.pre{display:none}.pre-on{overflow:hidden}.pre-on .pre{display:grid;place-items:center;position:fixed;inset:0;z-index:200;background:#B22D2D;animation:preout .9s cubic-bezier(.7,0,.2,1) 2.6s forwards}
.pre img{width:150px;height:150px;opacity:0;transform:scale(.94);animation:prein 1s ease .15s forwards;background:none}.pre-on.pre-go .pre{animation:preout2 .9s cubic-bezier(.7,0,.2,1) forwards}
@keyframes prein{to{opacity:1;transform:none}}@keyframes preout{to{transform:translateY(-100%);visibility:hidden}}@keyframes preout2{to{transform:translateY(-100%);visibility:hidden}}
.lh{position:relative;background:var(--grey);padding:clamp(2.5rem,6vw,4.5rem) 0 clamp(3.5rem,7vw,6rem);overflow:hidden}.lh-g{position:relative;display:grid;gap:3rem;align-items:center}@media(min-width:960px){.lh-g{grid-template-columns:.85fr 1.15fr}}
.lh h1{font-size:clamp(2.8rem,7vw,5.2rem);line-height:1.03;max-width:none;margin-bottom:.45em;letter-spacing:-.025em}.ln{display:block;overflow:hidden;padding-bottom:.1em}.ln>span{display:block}.lh .sub{max-width:30rem}
.path{position:absolute;left:0;bottom:0;width:100%;height:65%;color:var(--red);opacity:.45;pointer-events:none}
.arches{display:grid;grid-template-columns:1fr 1.2fr 1fr;gap:clamp(.5rem,1.6vw,1.1rem);align-items:end}.arch{margin:0;overflow:hidden;border-radius:999px 999px 3px 3px;background:#e9e5df}.a1{aspect-ratio:3/5}.a2{aspect-ratio:3/5.9}.a3{aspect-ratio:3/4.6}
.arch picture{height:100%}.arch img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}
[data-parallax] img{transform:translate3d(0,var(--py,0px),0);scale:1.14;will-change:transform}
.zoom img{transition:scale 1.6s cubic-bezier(.2,.7,.2,1)}.zoom:hover img{scale:1.2}
.ticker{overflow:hidden;border-block:1px solid var(--line);background:#fff;padding:1.15rem 0}.tk{display:flex;width:max-content;animation:tick 55s linear infinite}.tg{display:flex}
.tk span{font:italic 400 clamp(1.3rem,2.6vw,2rem) var(--serif);color:var(--ink);padding-right:2.2rem;white-space:nowrap}.tk span::after{content:"\2022";color:var(--red);margin-left:2.2rem;font-style:normal}@keyframes tick{to{transform:translateX(-50%)}}
.h-desks{border-bottom:1px solid var(--line);background:#fff}.h-desks ol{list-style:none;margin-inline:auto;padding:0;display:grid}.h-desks a{display:grid;gap:.35rem;padding:1.6rem .25rem;text-decoration:none;border-top:1px solid var(--line);position:relative}.h-desks li:first-child a{border-top:0}
.h-desks .n{font:500 1rem var(--serif);color:var(--red)}.h-desks strong{font:500 1.4rem/1.2 var(--serif);color:var(--ink)}.h-desks a span:last-child{color:var(--mut);font-size:.98rem}
.h-desks a::after{content:"";position:absolute;left:0;bottom:-1px;height:2px;width:100%;background:var(--red);transform:scaleX(0);transform-origin:left;transition:transform .6s cubic-bezier(.2,.7,.2,1)}.h-desks a:hover::after,.h-desks a:focus-visible::after{transform:scaleX(1)}
@media(min-width:800px){.h-desks ol{grid-template-columns:repeat(3,1fr)}.h-desks li+li a{border-left:1px solid var(--line)}.h-desks a{padding:2rem 1.75rem;border-top:0}.h-desks li:first-child a{padding-left:0}}
.h-facts{padding:2.75rem 0;background:#fff}.h-facts dl{margin-inline:auto;display:grid;gap:1.5rem 2rem}.h-facts div{border-top:2px solid var(--char);padding-top:.9rem}.h-facts dt{font:500 1.6rem var(--serif);color:var(--ink)}.h-facts dd{margin:.2rem 0 0;color:var(--mut);font-size:.98rem}
@media(min-width:560px){.h-facts dl{grid-template-columns:1fr 1fr}}@media(min-width:960px){.h-facts dl{grid-template-columns:repeat(4,1fr)}}
.h-sec{padding:clamp(4rem,9vw,7rem) 0}.h-split{display:grid;gap:3rem;align-items:center}@media(min-width:900px){.h-split{grid-template-columns:1.05fr .95fr;gap:5rem}}
.h-duo{position:relative;padding-bottom:3.5rem}.h-duo figure{margin:0;overflow:hidden;border-radius:999px 999px 3px 3px;background:#e9e5df}.h-duo picture{height:100%}.h-duo img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}
.h-duo .big{width:78%;aspect-ratio:4/5}.h-duo .small{position:absolute;right:0;bottom:0;width:44%;aspect-ratio:3/4;border:6px solid #fff;box-sizing:content-box;border-radius:999px 999px 3px 3px}
.h-idx{list-style:none;margin:0;padding:0}.h-idx a{display:flex;justify-content:space-between;align-items:center;padding:1rem 0;border-top:1px solid var(--line);text-decoration:none;font-weight:600;color:var(--ink);transition:color .2s,padding .3s}.h-idx li:last-child a{border-bottom:1px solid var(--line)}
.h-idx a::after{content:"";width:.6rem;height:.6rem;border-top:2px solid var(--red);border-right:2px solid var(--red);transform:rotate(45deg)}.h-idx a:hover{color:var(--red);padding-left:.5rem}
.h-av{background:#15181C;color:#d9dde2;padding:clamp(4rem,9vw,7rem) 0}.h-av h2{color:#fff}.h-av h2 em{color:var(--red-l)}.h-av .label{color:#c9ced4}.h-av .label::before{background:var(--red-l)}.h-av .lead{color:#d9dde2}.h-av :focus-visible{outline-color:#fff}
.h-av-g{display:grid;gap:3rem;align-items:center}@media(min-width:900px){.h-av-g{grid-template-columns:1.1fr .9fr;gap:5rem}}.h-avfig{margin:0;overflow:hidden;border-radius:999px 999px 3px 3px;aspect-ratio:4/5}.h-avfig picture{height:100%}.h-avfig img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}
.cats{list-style:none;display:flex;flex-wrap:wrap;margin:0 0 1.5rem;padding:0}.cats li{padding:.15rem 1rem .15rem 0;margin-right:1rem;border-right:1px solid #4a5059;font-weight:600;color:#fff}.cats li:last-child{border:0}
.disc{border-left:3px solid var(--red-l);background:rgba(255,255,255,.07);padding:1rem 1.25rem;margin:0;color:#fff}.h-av .btn-ghost{background:transparent;color:#fff;border:2px solid #fff}.h-av .btn-ghost:hover{background:#fff;color:#15181C}
.h-how{background:var(--grey);padding:clamp(4rem,9vw,7rem) 0}.h-steps{list-style:none;margin:2.5rem 0 0;padding:0;display:grid;gap:2rem}.h-steps li{display:grid;gap:.4rem;border-top:2px solid var(--char);padding-top:1rem}
.h-steps .n{font:500 1.6rem var(--serif);color:var(--red)}.h-steps strong{font:500 1.3rem var(--serif);color:var(--ink)}.h-steps span:last-child{color:var(--mut)}@media(min-width:560px){.h-steps{grid-template-columns:1fr 1fr}}@media(min-width:960px){.h-steps{grid-template-columns:repeat(4,1fr)}}
.h-aud{padding:clamp(4rem,9vw,7rem) 0}.h-aud-g{display:grid;gap:3rem}@media(min-width:900px){.h-aud-g{grid-template-columns:1fr 1fr;gap:5rem}}.h-aud article{border-top:1px solid var(--line);padding-top:1.75rem}.h-aud h2{font-size:clamp(1.6rem,3vw,2.2rem)}.h-aud p{color:var(--mut);max-width:30rem}.textlink{font-weight:600;color:var(--ink)}.textlink:hover{color:var(--red)}
@media(prefers-reduced-motion:no-preference){
@keyframes rise{from{opacity:0;transform:translateY(16px)}}@keyframes lnup{from{transform:translateY(108%)}}@keyframes archin{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0)}}@keyframes kb{from{scale:1.3}}@keyframes draw{from{clip-path:inset(0 100% 0 0)}}
.pre-on{--b:1.7s}.lh .label,.lh .sub,.lh .cta-row{animation:rise .9s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--b,0s) + .05s)}.lh .sub{animation-delay:calc(var(--b,0s) + .45s)}.lh .cta-row{animation-delay:calc(var(--b,0s) + .6s)}
.ln>span{animation:lnup 1.1s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--b,0s)}.ln:nth-child(2)>span{animation-delay:calc(var(--b,0s) + .12s)}.ln:nth-child(3)>span{animation-delay:calc(var(--b,0s) + .24s)}
.arch{animation:archin 1.5s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--b,0s) + .15s)}.a2{animation-delay:calc(var(--b,0s) + .3s)}.a3{animation-delay:calc(var(--b,0s) + .45s)}.arch img{animation:kb 2.8s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--b,0s)}.path{animation:draw 3s ease-out both;animation-delay:calc(var(--b,0s) + .5s)}
.js-ready [data-r]{opacity:0;transform:translateY(26px);transition:opacity 1s cubic-bezier(.2,.7,.2,1),transform 1s cubic-bezier(.2,.7,.2,1)}.js-ready [data-r].in{opacity:1;transform:none}
.js-ready [data-mask]{clip-path:inset(0 0 100% 0);transition:clip-path 1.5s cubic-bezier(.2,.7,.2,1)}.js-ready [data-mask].in{clip-path:inset(0)}}
@media(prefers-reduced-motion:reduce){.tk{width:auto;flex-wrap:wrap;justify-content:center}.tg+.tg{display:none}}
"""
JS += r"""(()=>{
const R=matchMedia('(prefers-reduced-motion: reduce)').matches,de=document.documentElement;
/* Preloader: first visit per session only; never set when motion is reduced. CSS also auto-dismisses it if this script fails. */
if(de.classList.contains('pre-on')){
 setTimeout(()=>de.classList.add('pre-go'),1500);
 setTimeout(()=>de.classList.remove('pre-on','pre-go'),2500);
 try{sessionStorage.setItem('apexPre','1')}catch(_){}
}
const hd=document.querySelector('.site-header');
const onScroll=()=>hd&&hd.classList.toggle('scrolled',scrollY>12);
addEventListener('scroll',onScroll,{passive:true});onScroll();
if(R||!('IntersectionObserver' in window))return;
/* Scroll reveals (js-ready is set by the script above only when this is safe). Elements already in view start visible. */
const els=[...document.querySelectorAll('[data-r],[data-mask]')];
els.forEach(el=>{el.style.transitionDelay=(+el.dataset.r||0)*110+'ms';if(el.getBoundingClientRect().top<innerHeight*.9)el.classList.add('in')});
/* Position-based check (an IntersectionObserver ignores fully clipped elements, which would leave masked photos hidden). */
let pend=els.filter(el=>!el.classList.contains('in'));
const reveal=()=>{const vh=innerHeight;pend=pend.filter(el=>{const r=el.getBoundingClientRect();if(r.top<vh*.88&&r.bottom>0){el.classList.add('in');return false}return true})};
addEventListener('scroll',()=>requestAnimationFrame(reveal),{passive:true});addEventListener('resize',reveal);reveal();
/* Gentle parallax on photo frames, capped at 40px. */
const px=[...document.querySelectorAll('[data-parallax]')].map(f=>({f,i:[...f.querySelectorAll('img')],k:parseFloat(f.dataset.parallax)||.05}));
let busy=false;
const upd=()=>{busy=false;const vh=innerHeight;px.forEach(o=>{const r=o.f.getBoundingClientRect();if(r.bottom<-60||r.top>vh+60)return;const d=r.top+r.height/2-vh/2;{const y=Math.max(-40,Math.min(40,-d*o.k))+'px';o.i.forEach(i=>i.style.setProperty('--py',y))}})};
addEventListener('scroll',()=>{if(!busy){busy=true;requestAnimationFrame(upd)}},{passive:true});addEventListener('resize',upd);upd();
})();
"""
CSS += r"""/* ===== Layer 2: morphing frames, journeys, dialog, sea band, credentials ===== */
.arch{position:relative}.arch.m{border-radius:50% 50% 3px 3px/calc(50%/var(--r)) calc(50%/var(--r)) 3px 3px}.arch.m>:nth-child(2){position:absolute;inset:0;opacity:0}
.lh::before{content:"";position:absolute;inset:-25%;background:radial-gradient(38% 38% at 28% 32%,rgba(178,45,45,.10),transparent 70%),radial-gradient(34% 34% at 78% 62%,rgba(31,35,40,.07),transparent 70%);pointer-events:none}
.h-show{padding:clamp(4rem,9vw,7rem) 0;background:#fff}.h-show .sec-h{max-width:40rem;margin-bottom:2.5rem}
.jc-list{list-style:none;margin:0;padding:0 0 1rem;display:flex;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}.jc-list::-webkit-scrollbar{display:none}.jc-li{flex:0 0 74%;scroll-snap-align:start}
@media(min-width:760px){.jc-list{display:grid;grid-template-columns:repeat(2,1fr);overflow:visible;gap:2.5rem 1.5rem}.jc-li{flex:none}}@media(min-width:1080px){.jc-list{grid-template-columns:repeat(4,1fr)}}
.jc{display:block;text-decoration:none;color:inherit;transition:transform .6s cubic-bezier(.2,.7,.2,1)}.jc:hover,.jc:focus-visible{transform:translateY(-8px)}
.jc-frame{display:block;aspect-ratio:4/5.4;overflow:hidden;border-radius:50% 50% 3px 3px/37% 37% 3px 3px;background:#e9e5df;transition:border-radius .9s cubic-bezier(.2,.7,.2,1),box-shadow .6s}
.jc:hover .jc-frame,.jc:focus-visible .jc-frame{border-radius:18px;box-shadow:0 24px 40px -20px rgba(21,24,28,.4)}
.jc-frame picture{height:100%}.jc-frame img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto;transition:scale 1.8s cubic-bezier(.2,.7,.2,1)}.jc:hover img,.jc:focus-visible img{scale:1.08}
.jc-body{display:grid;gap:.3rem;padding-top:1.1rem}.jc-body strong{font:500 1.35rem/1.2 var(--serif);color:var(--ink)}.jc-tag{color:var(--mut);font-size:.98rem}
.jc-more{font-weight:600;font-size:.92rem;color:var(--red);display:inline-flex;gap:.5rem;align-items:center;margin-top:.3rem}.jc-more::after{content:"";width:.5rem;height:.5rem;border-top:2px solid currentColor;border-right:2px solid currentColor;transform:rotate(45deg);transition:transform .4s}.jc:hover .jc-more::after{transform:translateX(5px) rotate(45deg)}
.jd{border:0;padding:0;width:min(960px,94vw);max-height:92vh;background:#fff;color:var(--char);overflow:auto;border-radius:6px}.jd::backdrop{background:rgba(15,17,20,.74)}
.jd[open]{animation:jdin .6s cubic-bezier(.2,.7,.2,1)}@keyframes jdin{from{opacity:0;transform:translateY(24px) scale(.98)}}
.jd-in{display:grid;position:relative}@media(min-width:760px){.jd-in{grid-template-columns:.9fr 1.1fr}}
.jd-x{position:absolute;top:.7rem;right:.7rem;z-index:2;width:44px;height:44px;border:0;border-radius:50%;background:rgba(255,255,255,.94);color:var(--char);font-size:1.7rem;line-height:1;cursor:pointer}.jd-x:hover{background:var(--char);color:#fff}
.jd-fig{margin:0;overflow:hidden;min-height:280px;background:#e9e5df}.jd-fig picture{height:100%}.jd-fig img{width:100%;height:100%;min-height:280px;object-fit:cover;aspect-ratio:auto}
.jd[open] .jd-fig{animation:figmorph 1.2s cubic-bezier(.2,.7,.2,1) both}@keyframes figmorph{from{clip-path:inset(7% 12% 7% 12% round 42% 42% 8px 8px)}to{clip-path:inset(0 round 0)}}
.jd-tx{padding:2.25rem clamp(1.25rem,3vw,2.5rem)}.jd-tx h2{font-size:clamp(1.7rem,3vw,2.3rem)}.jd-tag{color:var(--red);font-weight:600;margin:0 0 .75rem}.jd-tx h3{font:700 .95rem var(--sans);margin:1.4rem 0 .2rem;color:var(--ink)}.jd-tx .ticks{margin:.4rem 0 1rem}
html.jd-open{overflow:hidden}@media(max-width:759px){.jd{margin:auto 0 0;width:100vw;max-width:100vw;max-height:94vh;border-radius:14px 14px 0 0}.jd-fig{min-height:240px;max-height:300px}}
.sea{position:relative;min-height:min(78vh,640px);display:grid;align-items:center;color:#fff;overflow:hidden;background:#0b1a2b}.sea-v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:none}
.sea-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,14,18,.82),rgba(11,14,18,.5) 55%,rgba(11,14,18,.15))}@media(max-width:759px){.sea-shade{background:rgba(11,14,18,.64)}}
.sea .wrap{position:relative}.sea-in{max-width:620px;padding:clamp(4rem,9vw,7rem) 0}.sea h2{color:#fff}.sea h2 em{color:var(--red-l)}.sea .label{color:#e6e8eb}.sea .label::before{background:var(--red-l)}.sea .lead{color:#e6e8eb}.sea :focus-visible{outline-color:#fff}
.sea-btn{position:absolute;right:1rem;bottom:1rem;min-height:44px;padding:.5rem 1.1rem;border:1px solid rgba(255,255,255,.75);background:rgba(15,17,20,.55);color:#fff;border-radius:2px;font:600 .9rem var(--sans);cursor:pointer}.sea-btn:hover{background:#fff;color:var(--char)}.sea-btn[hidden]{display:none}
@media(min-width:1160px){.nav-actions .btn-line{display:none}}.h-sec .lead{margin-bottom:1.75rem}
.iata{display:flex;align-items:center;gap:1rem;flex-wrap:wrap;padding:1.5rem 0 0;margin-top:2.5rem;border-top:1px solid var(--line)}.iata img{height:44px;width:auto;background:none}.iata p{margin:0;font-size:.95rem;color:var(--ink)}
@media(prefers-reduced-motion:no-preference){
@keyframes shape{0%,35%,100%{border-radius:50% 50% 3px 3px/calc(50%/var(--r)) calc(50%/var(--r)) 3px 3px}50%,85%{border-radius:50% 50% 3px 3px/calc(26%/var(--r)) calc(26%/var(--r)) 3px 3px}}
@keyframes xfade{0%,35%,100%{opacity:0}50%,85%{opacity:1}}@keyframes drift{from{transform:translate3d(-3%,-2%,0) rotate(0deg)}to{transform:translate3d(3%,2%,0) rotate(6deg)}}
.arch.m{animation:archin 1.5s cubic-bezier(.2,.7,.2,1) both,shape 16s ease-in-out infinite;animation-delay:calc(var(--b,0s) + .15s),calc(var(--b,0s) + var(--ph,3s))}.a2.m{animation-delay:calc(var(--b,0s) + .3s),calc(var(--b,0s) + var(--ph,3s))}
.arch.m>:nth-child(2){animation:xfade 16s ease-in-out infinite;animation-delay:calc(var(--b,0s) + var(--ph,3s))}.lh::before{animation:drift 28s ease-in-out infinite alternate}}
"""
JS += r"""(()=>{
const R=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* Enquiry prefill from ?interest= (plain text only, capped). */
const q=new URLSearchParams(location.search),msg=document.querySelector('textarea[name=message]'),it=q.get('interest');
if(msg&&it&&!msg.value)msg.value='I would like to enquire about: '+it.slice(0,80);
/* Journey detail dialog. Without JS or <dialog> support, each card is simply a link to the enquiry form. */
const dlg=document.querySelector('.jd');
if(dlg&&typeof dlg.showModal==='function'){
 const fig=dlg.querySelector('.jd-fig'),body=dlg.querySelector('.jd-body'),h=dlg.querySelector('#jd-t'),enq=dlg.querySelector('.jd-enq'),more=dlg.querySelector('.jd-more');
 document.querySelectorAll('.jc').forEach(a=>a.addEventListener('click',e=>{
  e.preventDefault();
  h.textContent=a.dataset.title;
  body.replaceChildren(document.getElementById('j-'+a.dataset.j).content.cloneNode(true));
  const pic=a.querySelector('picture,img').cloneNode(true);
  [pic,...pic.querySelectorAll('img,source')].forEach(n=>{if(n.matches('img,source')){n.setAttribute('sizes','(min-width:760px) 430px, 94vw');if(n.matches('img'))n.loading='eager'}});
  fig.replaceChildren(pic);enq.href=a.href;more.href=a.dataset.page;
  dlg.showModal();document.documentElement.classList.add('jd-open');
 }));
 dlg.addEventListener('close',()=>document.documentElement.classList.remove('jd-open'));
 dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close()});
 dlg.querySelector('.jd-x').addEventListener('click',()=>dlg.close());
}
/* Sea video: loads only when near the viewport, never with reduced motion, Save-Data or 2G; paused off-screen; user pause control. */
const v=document.querySelector('.sea-v'),pb=document.querySelector('.sea-btn');
if(v&&pb){
 const c=navigator.connection||{};
 if(!R&&!c.saveData&&!/2g$/.test(c.effectiveType||'')&&'IntersectionObserver' in window){
  let on=false,user=false;
  new IntersectionObserver(es=>es.forEach(e=>{
   if(e.isIntersecting){if(!on){on=true;['mp4','webm'].forEach(x=>{const s=document.createElement('source');s.src=v.dataset[x];s.type='video/'+x;v.appendChild(s)});v.load()}if(!user)v.play().catch(()=>{})}else v.pause();
  }),{rootMargin:'200px'}).observe(v.parentElement);
  pb.hidden=false;
  pb.addEventListener('click',()=>{
   if(v.paused){user=false;v.play().catch(()=>{});pb.textContent='Pause';pb.setAttribute('aria-label','Pause background video')}
   else{user=true;v.pause();pb.textContent='Play';pb.setAttribute('aria-label','Play background video')}
  });
 }
}
})();
"""
W("css/style.css", CSS)
W("js/main.js", JS)

def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)

for fn in os.listdir(os.path.join(ROOT, "assets")):          # logo, favicons, OG image
    p = os.path.join(ROOT, "assets", fn)
    if os.path.isfile(p):
        cp(p, os.path.join(OUT, "images", fn))
for fn in os.listdir(os.path.join(ROOT, "assets", "media")):      # optimised video + poster
    cp(os.path.join(ROOT, "assets", "media", fn), os.path.join(OUT, "media", fn))
make_photos()                                                 # optimised variants from assets/source-photos
for name, alt in PH.items():                                  # placeholders only where no photo exists
    if has_photo(name):
        continue
    w, h, _ = IMG_SPECS[name]
    W(f"images/{name}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Placeholder image"><rect width="{w}" height="{h}" fill="#e9eaec"/><path d="M0 {h*.8:.0f} {w*.3:.0f} {h*.55:.0f} {w*.55:.0f} {h*.7:.0f} {w*.8:.0f} {h*.45:.0f} {w} {h*.6:.0f}V{h}H0Z" fill="#d4d6d9"/><text x="{w/2:.0f}" y="{h/2:.0f}" fill="#1F2328" font-family="Arial,sans-serif" font-size="{w//34}" text-anchor="middle">PLACEHOLDER: {name}</text><text x="{w/2:.0f}" y="{h/2+w//22:.0f}" fill="#C41210" font-family="Arial,sans-serif" font-size="{w//52}" text-anchor="middle">Replace with licensed photo: assets/photos/{name}.webp ({w}x{h})</text></svg>')

page("thank-you.html", "Thank you | Apex Travels", "Thank you for contacting Apex Travels.",
     '<div class="pagehead"><div class="wrap"><h1>Thank you</h1><p class="sub">If you submitted an enquiry, our team will review it and get back to you.</p></div></div>'
     f'<section class="sec"><div class="wrap narrow"><p>You can return to the homepage or browse our services.</p><div class="cta-row">{btn("index.html","Back to home")}</div></div></section>', noindex=True)

# ---------- SEO + Netlify files ----------
W("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
W("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f'  <url><loc>{SITE}{"/" if p == "index.html" else "/" + p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p == "index.html" else "0.8" if p in ("private-aviation.html", "contact.html") else "0.6"}</priority></url>\n' for p in ALL) + "</urlset>\n")
W("_headers", "/*\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n/css/*\n  Cache-Control: public, max-age=3600\n/js/*\n  Cache-Control: public, max-age=3600\n/images/*\n  Cache-Control: public, max-age=86400\n/media/*\n  Cache-Control: public, max-age=86400\n")
W("netlify.toml", '[build]\n  publish = "site"\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Content-Type-Options = "nosniff"\n    X-Frame-Options = "DENY"\n    Referrer-Policy = "strict-origin-when-cross-origin"\n\n[[headers]]\n  for = "/css/*"\n  [headers.values]\n    Cache-Control = "public, max-age=3600"\n\n[[headers]]\n  for = "/js/*"\n  [headers.values]\n    Cache-Control = "public, max-age=3600"\n', ROOT)

# ---------- docs ----------
from math import gcd
def _ar(w, h): g = gcd(w, h); return f"{w // g}:{h // g}"
rows_md = "\n".join(f"| `{n}` | {IMG_WHERE[n]} | {w}x{h} ({_ar(w, h)}) | `assets/source-photos/{n}.jpg` | {status_md(n)} | {IMG_RIGHTS.get(n) or '**NOT RECORDED**'} | {b} |" for n, (w, h, b) in IMG_SPECS.items())
W("IMAGES.md", f"""# Image slots, briefs and permission record

This file is generated by `build.py`. Record permissions in `IMG_RIGHTS` in `build.py`, not here.

## How to add a photo
1. Save your ORIGINAL (largest, uncropped) photo as `assets/source-photos/<name>.jpg` (or `.png` / `.webp`). Originals are never copied to `site/`.
2. `pip install pillow`, then `python3 build.py`. The build centre-crops to 2:3 portrait (adjust with `FOCUS`), applies the colour grade (`GRADE`, `GRADE_OVERRIDE`), never upscales, and writes 480/800/1200/1600 px AVIF, WebP and JPG files to `site/images/photos/`. Pages use `<picture>` with `srcset`/`sizes` and explicit width/height. Heroes load eagerly; every other image is lazy-loaded.
3. Add a line to `IMG_RIGHTS` (photographer or source, licence/ID, model or property release).
4. Check the alt text in `build.py` still describes what the photo shows.

| Name | Appears on | Size / ratio | Source file expected | Status | Permission record | Brief |
|---|---|---|---|---|---|---|
{rows_md}

Aircraft images: generic aircraft only, no visible registration, no Apex livery, logo or tail branding. Aviation images carry the caption "Illustrative image. Apex Travels does not own or operate aircraft." Never describe aircraft as "our jet" or "our fleet".

## Brand assets and other items
| Asset | Source | Rights | Status |
|---|---|---|---|
| `apex-logo.png`, `apex-logo-128.png`, `favicon-32.png`, `apple-touch-icon.png`, `og-image.png` | Derived from `Apex_logo.png` (3375x3375) supplied by client. Original kept in `assets/source/Apex_logo-original.png`. The OG image also uses the graded `hero-home` photo. | Apex brand asset; owner confirmation needed | Supplied; rebuild the OG image if the hero photo changes |
| Collage screenshot `1793951586380_image.png` | Supplied by client | Unknown; low resolution composite | **Not used** |
| Cruise video `0_Cruise_Ship_Ship_1280x720.mp4` | Supplied by client. Original in `assets/source-video/` (not published). Published copies: `assets/media/cruise.mp4` and `cruise.webm` (960px, no audio) and `cruise-poster.jpg` (frame at 3.5s). | Source, licence and permission: **NOT PROVIDED** | Used only in the "Sea journeys" band |
| Beach photo in the portal screenshot | Portal screenshot only | Unknown licence | **Not used** |
""", ROOT)

W("README.md", """# Apex Travels website

`build.py` is the single source of truth. It writes the complete static site to `site/` (wiped and rebuilt on every run).

## Structure
```
build.py               CONFIG block at top (contact, portal, social, dates), content, CSS, JS
assets/                logo, favicons, og-image (copied to site/images)
assets/source-photos/  your ORIGINAL photos (never copied to site/)
assets/source/         original logo crop
site/                  generated output: drag THIS folder into Netlify
IMAGES.md              image slots, briefs, permission record (generated)
```

## Regenerate
```
python3 build.py            # Python 3.9+; Pillow required now that photos are present (pip install pillow)
python3 build.py --strict   # fails while launch blockers or placeholder images remain
```
Edit values ONLY in the CONFIG block. Hand edits in `site/` are overwritten.

## Preview locally
`python3 -m http.server 8000 -d site`, then open http://localhost:8000. Double-clicking the HTML files also works for browsing, but forms cannot submit locally: you will see the failure message, which is expected.

## Test on a temporary Netlify address
1. app.netlify.com/drop, drag `site/`. Do not attach the live domain or change DNS.
2. Site configuration > Forms: confirm `private-aviation-quote` and `contact-enquiry` appear.
3. Submit each form once. Success must appear only after Netlify accepts it; confirm the entry in the Forms tab. Repeat with the network off: you must see the error message.
4. Check keyboard navigation, reduced motion, the B2B Agent Login link, and the social links.
5. Canonical tags and sitemap point at the production domain: keep the temporary address out of Search Console.

## Launch blockers
Run `python3 build.py` and read the "LAUNCH BLOCKERS" line. Currently: IATA agent code and official IATA artwork, confirmation that cruises are offered, public LinkedIn URL, policy date and privacy contact, photo source/licence records, higher-resolution photos, legal review, and your own browser and form tests.
""", ROOT)

# ---------- report ----------
print(f"Built {len(ALL) + 1} pages; {len(PH)} image slots ({sum(has_photo(n) for n in PH)} with real photos)")
if UNSET:
    print("LAUNCH BLOCKERS (unset CONFIG values): " + ", ".join(UNSET))
if UNLICENSED:
    print("LAUNCH BLOCKERS (photo source/licence not recorded): " + ", ".join(UNLICENSED))
for n in IMG_SPECS:
    if has_photo(n) and src_size(n)[0] < 1200:
        print(f"WARNING: {n} source is {src_size(n)[0]}px wide (below 1200px): will look soft on large or high-density screens")
if "--strict" in sys.argv and (UNSET or UNLICENSED or any(not has_photo(n) for n in PH)):
    print("--strict: blockers remain (unset CONFIG values and/or placeholder images)")
    sys.exit(1)
