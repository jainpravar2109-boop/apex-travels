# Apex Travels website

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
