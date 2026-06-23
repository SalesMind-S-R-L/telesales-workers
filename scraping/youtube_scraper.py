#!/usr/bin/env python3
"""
Scraper YouTube — estrae tutti i video di un canale con metadati completi.
Uso: python3 youtube_scraper.py <url_canale> [--limit N] [--out file.csv]

Esempi:
  python3 youtube_scraper.py https://www.youtube.com/@nateherk
  python3 youtube_scraper.py https://www.youtube.com/@nateherk --limit 50 --out nateherk.csv
"""
import sys, subprocess, json, csv, argparse
from datetime import datetime

def scrape(channel_url, limit=None, out_path=None):
    cmd = [sys.executable, '-m', 'yt_dlp',
           '--skip-download', '--print-json']
    if limit:
        cmd += ['--playlist-items', f'1-{limit}']
    cmd.append(channel_url + '/videos')

    print(f"Scraping: {channel_url} (limit={limit or 'tutti'})...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    videos = []
    for line in result.stdout.strip().split('\n'):
        if not line.strip(): continue
        try:
            v = json.loads(line)
            date_raw = v.get('upload_date', '')
            date_fmt = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:]}" if date_raw else ''
            videos.append({
                'id':          v.get('id', ''),
                'url':         f"https://youtube.com/watch?v={v.get('id','')}",
                'title':       v.get('title', ''),
                'views':       v.get('view_count') or 0,
                'likes':       v.get('like_count') or 0,
                'comments':    v.get('comment_count') or 0,
                'date':        date_fmt,
                'duration':    v.get('duration_string', ''),
                'description': (v.get('description') or '')[:300],
                'tags':        ', '.join(v.get('tags') or []),
            })
        except: pass

    videos.sort(key=lambda x: x['views'], reverse=True)
    print(f"Video trovati: {len(videos)}")

    if out_path:
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(videos[0].keys()) if videos else [])
            w.writeheader()
            w.writerows(videos)
        print(f"Salvato: {out_path}")
    else:
        print(f"\n{'Views':>10} | {'Data':>10} | {'Dur':>7} | Titolo")
        print('-' * 80)
        for v in videos:
            print(f"{v['views']:>10,} | {v['date']:>10} | {v['duration']:>7} | {v['title'][:50]}")

    return videos

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('url')
    p.add_argument('--limit', type=int, default=None)
    p.add_argument('--out', default=None)
    args = p.parse_args()
    scrape(args.url, args.limit, args.out)
