#!/usr/bin/env python3
"""Daily TikTok engagement snapshot for @vita_press.

Pulls user stats + per-video stats + new comments and:
1. Appends a row per video to engagement.csv (in /private/tmp/VitaPress/marketing/)
2. Appends new comments (with 🧃 / pre-order / postcode flags) to comments.csv
3. Prints a digest suitable for Telegram delivery
"""
import asyncio, csv, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

from TikTokApi import TikTokApi

USERNAME = "vita_press"
COOKIE_PATH = Path.home() / ".vita-press-marketing/tiktok_cookies.json"
REPO_DIR = Path("/private/tmp/VitaPress/marketing")
REPO_DIR.mkdir(parents=True, exist_ok=True)
ENGAGEMENT_CSV = REPO_DIR / "engagement.csv"
COMMENTS_CSV = REPO_DIR / "comments.csv"
SEEN_COMMENTS = REPO_DIR / ".seen_comments.json"

# Pre-order signal regex
PREORDER_RE = re.compile(r"🧃|pre.?order|preorder|deliver|sunday|pickup|how (do|can) i (get|order|buy)|where can i", re.IGNORECASE)
POSTCODE_RE = re.compile(r"\b([A-Z]{1,2}\d{1,2}[A-Z]?)\s*\d[A-Z]{2}\b")

ENG_HEADERS = ["snapshot_at", "video_id", "posted_at", "views", "likes", "comments", "shares", "saves", "desc"]
CMT_HEADERS = ["snapshot_at", "video_id", "comment_id", "author", "text", "likes", "preorder_signal", "postcode"]


def load_ms_token():
    cookies = json.loads(COOKIE_PATH.read_text())
    return next(c["value"] for c in cookies if c["name"] == "msToken")


def ensure_csv(path, headers):
    if not path.exists():
        with path.open("w", newline="") as f:
            csv.writer(f).writerow(headers)


def load_seen():
    return set(json.loads(SEEN_COMMENTS.read_text())) if SEEN_COMMENTS.exists() else set()


def save_seen(seen):
    SEEN_COMMENTS.write_text(json.dumps(sorted(seen)))


async def main():
    ms_token = load_ms_token()
    now = datetime.now(timezone.utc).isoformat()
    ensure_csv(ENGAGEMENT_CSV, ENG_HEADERS)
    ensure_csv(COMMENTS_CSV, CMT_HEADERS)
    seen = load_seen()

    digest_lines = [f"📊 *@{USERNAME} engagement* — {datetime.now().strftime('%Y-%m-%d %H:%M')}"]
    new_preorders = []

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=True)
        user = api.user(USERNAME)
        info = await user.info()
        u = info.get("userInfo", {}).get("user", {})
        s = info.get("userInfo", {}).get("stats", {})
        digest_lines.append(
            f"👥 {s.get('followerCount',0)} followers · ❤️ {s.get('heartCount',0)} hearts · 🎬 {s.get('videoCount',0)} videos"
        )
        digest_lines.append("")

        eng_rows, cmt_rows = [], []
        async for v in user.videos(count=30):
            d = v.as_dict
            vs = d.get("stats", {})
            vid = d["id"]
            posted = datetime.fromtimestamp(d.get("createTime", 0), tz=timezone.utc).isoformat() if d.get("createTime") else ""
            eng_rows.append([
                now, vid, posted,
                vs.get("playCount", 0), vs.get("diggCount", 0), vs.get("commentCount", 0),
                vs.get("shareCount", 0), vs.get("collectCount", 0), (d.get("desc") or "")[:200],
            ])
            digest_lines.append(
                f"• {vid[-6:]} · 👁 {vs.get('playCount',0):,} · ❤️ {vs.get('diggCount',0)} · 💬 {vs.get('commentCount',0)} · 🔁 {vs.get('shareCount',0)}"
            )
            digest_lines.append(f"  _{(d.get('desc') or '')[:80]}_")

            # Comments — only fetch if there are any new ones likely
            if vs.get("commentCount", 0) > 0:
                try:
                    async for c in v.comments(count=50):
                        cd = c.as_dict
                        cid = cd.get("cid") or cd.get("id")
                        if not cid or cid in seen:
                            continue
                        seen.add(cid)
                        text = cd.get("text", "")
                        author = cd.get("user", {}).get("unique_id") or cd.get("user", {}).get("uniqueId", "")
                        signal = bool(PREORDER_RE.search(text))
                        pc_match = POSTCODE_RE.search(text.upper())
                        postcode = pc_match.group(0) if pc_match else ""
                        cmt_rows.append([now, vid, cid, author, text, cd.get("digg_count", 0), int(signal), postcode])
                        if signal:
                            new_preorders.append(f"  🧃 @{author}: _{text[:120]}_" + (f"  ({postcode})" if postcode else ""))
                except Exception as e:
                    digest_lines.append(f"  ⚠️ comment fetch failed: {e}")

    with ENGAGEMENT_CSV.open("a", newline="") as f:
        csv.writer(f).writerows(eng_rows)
    if cmt_rows:
        with COMMENTS_CSV.open("a", newline="") as f:
            csv.writer(f).writerows(cmt_rows)
    save_seen(seen)

    digest_lines.append("")
    if new_preorders:
        digest_lines.append(f"🚨 *{len(new_preorders)} new pre-order signal(s):*")
        digest_lines.extend(new_preorders)
    else:
        digest_lines.append("_No new pre-order signals this run._")

    digest_lines.append("")
    digest_lines.append(f"📁 `engagement.csv` (+{len(eng_rows)} rows) · `comments.csv` (+{len(cmt_rows)} rows)")

    print("\n".join(digest_lines))


if __name__ == "__main__":
    asyncio.run(main())
