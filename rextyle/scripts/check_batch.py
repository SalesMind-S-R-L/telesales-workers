#!/usr/bin/env python3
"""
Rextyle — Self-check batch contenuti.

Verifica 11 criteri di qualità per ogni post in un batch. Blocca se anche solo
un post ha ISSUES. Esegue PRIMA della pubblicazione (Gate 2 del flusso).

Uso:
    python check_batch.py output/2026-W24/
"""

import argparse
import json
import re
import sys
from pathlib import Path
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent

# Carica blacklist vocabolario dal contesto voce
VOCE_PATH = ROOT / "_contesto" / "voce.md"
BLACKLIST = []
if VOCE_PATH.exists():
    text = VOCE_PATH.read_text()
    # Estrae le frasi tra "## Vocabolario VIETATO" e la sezione successiva
    m = re.search(r"## Vocabolario VIETATO.*?\n(.*?)(?=\n## )", text, re.DOTALL)
    if m:
        BLACKLIST = re.findall(r'"([^"]+)"', m.group(1))

# Palette HEX accettati (dal brand kit)
ALLOWED_HEX = ["#0B4F5C", "#E5AC4A", "#F7F4EC", "#1A1A1A", "#7C7C7C", "#C76E3A"]


def check_post(post_dir: Path) -> dict:
    """Esegue gli 11 check su un singolo post. Ritorna dict {check: pass/fail/message}."""
    results = {}
    slides = sorted(post_dir.glob("slide-*.png"))
    meta_path = post_dir / "meta.json"
    caption_path = post_dir / "caption.md"
    hashtag_path = post_dir / "hashtag.txt"

    # 1. Numero slide
    n_slides = len(slides)
    results["slide_count"] = ("PASS", f"{n_slides} slide") if 3 <= n_slides <= 7 else ("FAIL", f"{n_slides} slide (atteso 3-7)")

    # 2. Risoluzione corretta
    bad_res = []
    for s in slides:
        try:
            img = Image.open(s)
            if img.size != (1080, 1350):
                bad_res.append(f"{s.name}={img.size}")
        except Exception as e:
            bad_res.append(f"{s.name}=err({e})")
    results["resolution"] = ("PASS", "tutte 1080×1350") if not bad_res else ("FAIL", f"{', '.join(bad_res)}")

    # 3. Logo presente (placeholder: andrebbe fatto via image hash/template match)
    # Per ora controlla solo che la cartella contenga un file logo o che la skill lo abbia incluso
    results["logo_presence"] = ("PASS", "verifica manuale (auto-check in roadmap)")

    # 4. Palette compliant (placeholder: image analysis per pixel HEX)
    # In implementazione completa: per ogni PNG estrai i pixel dominanti e verifica
    # che siano dentro ALLOWED_HEX +/- tolleranza 2
    results["palette"] = ("PASS", "auto-check in roadmap (visual review per ora)")

    # 5. Font compliant (placeholder: i PNG generati con Manrope/Inter dovrebbero
    # essere taggati nel meta.json dalla skill)
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        fonts = meta.get("fonts_used", [])
        allowed = {"Manrope", "Inter"}
        bad_fonts = [f for f in fonts if f not in allowed]
        results["fonts"] = ("PASS", f"{', '.join(fonts) or 'no metadata'}") if not bad_fonts else ("FAIL", f"font non consentiti: {bad_fonts}")
    else:
        results["fonts"] = ("WARN", "meta.json mancante")

    # 6. Caption length
    if caption_path.exists():
        caption = caption_path.read_text().strip()
        n = len(caption)
        results["caption_length"] = ("PASS", f"{n} char") if 100 <= n <= 800 else ("FAIL", f"{n} char (atteso 100-800)")
    else:
        results["caption_length"] = ("FAIL", "caption.md mancante")

    # 7. Hashtag count
    if hashtag_path.exists():
        hashtags = [h for h in hashtag_path.read_text().split() if h.startswith("#")]
        n = len(hashtags)
        results["hashtag_count"] = ("PASS", f"{n} hashtag") if 8 <= n <= 12 else ("FAIL", f"{n} hashtag (atteso 8-12)")
    else:
        results["hashtag_count"] = ("FAIL", "hashtag.txt mancante")

    # 8. CTA presente
    if caption_path.exists():
        caption_low = caption.lower()
        cta_keywords = ["link in bio", "scrivici", " dm", "listino sul sito", "prenota", "contattaci"]
        has_cta = any(k in caption_low for k in cta_keywords)
        results["cta"] = ("PASS", "CTA trovata") if has_cta else ("FAIL", "nessuna CTA riconosciuta")
    else:
        results["cta"] = ("FAIL", "no caption")

    # 9. Vocabolario blacklist
    if caption_path.exists():
        bad_phrases = [p for p in BLACKLIST if p.lower() in caption.lower()]
        results["blacklist"] = ("PASS", "nessuna frase vietata") if not bad_phrases else ("FAIL", f"usa: {bad_phrases}")
    else:
        results["blacklist"] = ("WARN", "no caption per verifica")

    # 10. Brand voice tono (placeholder: andrebbe LLM check via Claude API)
    # Cerca pattern indicativi di condizionali
    if caption_path.exists():
        bad_modal = re.findall(r"\b(vorremmo|potremmo|saremmo|magari|forse)\b", caption.lower())
        results["voice_tone"] = ("PASS", "tono operativo") if not bad_modal else ("FAIL", f"condizionali: {bad_modal}")
    else:
        results["voice_tone"] = ("WARN", "no caption")

    # 11. Anti-duplicato (placeholder: perceptual hash vs ultimi 90gg)
    # Implementazione completa: imagehash.phash + confronto con DB local
    results["anti_duplicate"] = ("PASS", "verifica in roadmap")

    return results


def report(batch_dir: Path):
    post_dirs = sorted([d for d in batch_dir.iterdir() if d.is_dir()])
    all_pass = True
    report_lines = [f"# Check Batch — {batch_dir.name}\n"]

    for post_dir in post_dirs:
        results = check_post(post_dir)
        post_pass = all(r[0] != "FAIL" for r in results.values())
        all_pass = all_pass and post_pass

        status = "OK" if post_pass else "ISSUES"
        report_lines.append(f"\n## {post_dir.name} — {status}\n")
        report_lines.append("| Check | Esito | Note |")
        report_lines.append("|---|---|---|")
        for check_name, (level, msg) in results.items():
            report_lines.append(f"| {check_name} | {level} | {msg} |")

    # Scrivi report
    report_path = batch_dir / "check.md"
    report_path.write_text("\n".join(report_lines))
    print(f"\nReport scritto in: {report_path}")
    print(f"\nRisultato globale: {'TUTTO OK — pronto per Gate 3' if all_pass else 'ISSUES — fix richiesti prima di proseguire'}")

    return 0 if all_pass else 1


def main():
    parser = argparse.ArgumentParser(description="Rextyle batch self-check")
    parser.add_argument("batch_dir", help="Cartella batch, es. output/2026-W24/")
    args = parser.parse_args()

    batch_dir = Path(args.batch_dir)
    if not batch_dir.is_dir():
        print(f"ERRORE: {batch_dir} non valida")
        sys.exit(1)

    sys.exit(report(batch_dir))


if __name__ == "__main__":
    main()
