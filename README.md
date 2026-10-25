# bahadari.de

Bilingual (DE/EN) static website for Hashmat Bahadari – IT systems, Microsoft 365 & automation (v3).
Plain HTML/CSS/JS, no framework, no build step needed on GitHub. All internal links are relative.

## Deploy to GitHub Pages
1. Upload the contents of this folder to the root of your repository (e.g. `bahadari1361/bahadari.de`), branch `main`.
2. Repository → Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`.
3. Custom domain: `bahadari.de` (already set in the `CNAME` file). Tick **Enforce HTTPS** once the certificate is issued.

## DNS at your domain provider
| Type  | Name | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| AAAA  | @    | 2606:50c0:8000::153 |
| AAAA  | @    | 2606:50c0:8001::153 |
| AAAA  | @    | 2606:50c0:8002::153 |
| AAAA  | @    | 2606:50c0:8003::153 |
| CNAME | www  | bahadari1361.github.io |

Remove any old A/AAAA records for `@` first. Keep your MX/TXT records for email untouched.

## Structure
- `/` German pages, `/en/` English pages, clean folder URLs
- `assets/` CSS, JS, self-hosted fonts (no Google Fonts request → GDPR-friendly), logo
- `404.html`, `sitemap.xml`, `robots.txt`, `CNAME`, `.nojekyll`
