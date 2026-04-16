import random
import requests

def fetch_live_insight():
    try:
        # 1. Quran + Translation (AlQuran Cloud)
        verse_id = random.randint(1, 6236)
        q_url = f"https://api.alquran.cloud/v1/ayah/{verse_id}/editions/quran-uthmani,en.sahih"
        q_res = requests.get(q_url, timeout=10).json()
        if q_res.get("code") != 200: return None
        
        verse_formatted = f"{q_res['data'][0]['text']}\n{q_res['data'][1]['text']}\n(Surah {q_res['data'][0]['surah']['englishName']} {q_res['data'][0]['numberInSurah']})"
        
        # 2. Tafsir/Explanation (QuranEnc) - This provides the actual explanation
        t_url = f"https://quranenc.com/api/v1/translation/aya/english_saheeh/{verse_id}"
        t_res = requests.get(t_url, timeout=10).json()
        tafsir_text = "No commentary available for this verse."
        if "result" in t_res:
            tafsir_text = t_res["result"].get("footnotes", "This verse focuses on the guidance and wisdom of Allah.")
        
        # 3. Hadith (Hadith API)
        h_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/eng-bukhari.json"
        h_res = requests.get(h_url, timeout=10).json()
        hadith_item = random.choice(h_res["hadiths"])
        hadith_formatted = f"{hadith_item['text']}\n(Sahih Bukhari {hadith_item['hadithnumber']})"
        
        return {
            "verse": verse_formatted,
            "tafsir": tafsir_text,
            "hadith": hadith_formatted
        }
    except Exception:
        return None

def get_islamic_insight():
    insight = fetch_live_insight()
    if not insight:
        return "Daily Islamic Insight: (Live data service is currently unavailable. Please check back later for updates.)"
    return f"Daily Islamic Insight:\n\n[Quran]\n{insight['verse']}\n\n[Tafsir (Explanation)]\n{insight['tafsir']}\n\n[Hadith]\n{insight['hadith']}"

if __name__ == "__main__":
    print(get_islamic_insight())
