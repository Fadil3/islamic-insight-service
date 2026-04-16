import random
import sqlite3
import requests

DB_PATH = "/home/fadil/.hermes/islamic_insights.db"

def fetch_live_insight():
    try:
        # Try fetching from API
        verse_id = random.randint(1, 6236)
        q_url = f"https://api.alquran.cloud/v1/ayah/{verse_id}/editions/quran-uthmani,en.sahih"
        q_res = requests.get(q_url, timeout=10).json()
        if q_res.get("code") != 200: return None
        
        t_url = f"https://quranenc.com/api/v1/translation/aya/english_saheeh/{verse_id}"
        t_res = requests.get(t_url, timeout=10).json()
        if "result" not in t_res: return None
        
        h_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/eng-bukhari.json"
        h_res = requests.get(h_url, timeout=10).json()
        hadith_item = random.choice(h_res["hadiths"])
        
        return {
            "verse": f"{q_res['data'][0]['text']}\n{q_res['data'][1]['text']}\n(Surah {q_res['data'][0]['surah']['englishName']} {q_res['data'][0]['numberInSurah']})",
            "tafsir": t_res["result"]["translation"],
            "hadith": f"{hadith_item['text']}\n(Sahih Bukhari {hadith_item['hadithnumber']})"
        }
    except Exception:
        return None

def get_db_insight():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT verse_arabic, verse_translation, surah_info, tafsir, hadith_text, hadith_citation FROM insights ORDER BY RANDOM() LIMIT 1;")
    row = cursor.fetchone()
    conn.close()
    if not row: return None
    return {
        "verse": f"{row[0]}\n{row[1]}\n({row[2]})",
        "tafsir": row[3],
        "hadith": f"{row[4]}\n({row[5]})"
    }

def get_islamic_insight():
    # Try live, then fallback to DB
    insight = fetch_live_insight()
    if not insight:
        insight = get_db_insight()
        prefix = "Daily Islamic Insight (DB Backup Mode):"
    else:
        prefix = "Daily Islamic Insight:"
    
    return f"{prefix}\n\n[Quran]\n{insight['verse']}\n\n[Tafsir]\n{insight['tafsir']}\n\n[Hadith]\n{insight['hadith']}"

if __name__ == "__main__":
    print(get_islamic_insight())
