import requests
import os

API_URL = "https://aloula.faulio.com/api/v1/channels"
# We must mimic the browser headers you used in Mises
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://aloula.sa/",
    "Origin": "https://aloula.sa"
}

def fetch_data():
    try:
        r = requests.get(API_URL, headers=HEADERS, timeout=15)
        return r.json().get('data', [])
    except:
        return []

def main():
    channels = fetch_data()
    if not channels:
        print("API Error: No data received.")
        return

    m3u_output = "#EXTM3U\n"
    
    for ch in channels:
        name = ch.get('title', 'Unknown')
        logo = ch.get('full', '')
        # Kwikmotion URLs are usually in the 'stream_url' or 'stream' object
        stream = ch.get('stream_url') or ch.get('stream', {}).get('url')

        if stream:
            # Add metadata
            m3u_output += f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" tvg-logo="{logo}", {name}\n'
            
            # CRITICAL: This line tells VLC/IPTV apps to fake the headers
            # Note the | separating the URL from the Header string (standard for many players)
            m3u_output += f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}\n'
            m3u_output += f'#EXTVLCOPT:http-referrer=https://aloula.sa/\n'
            m3u_output += f"{stream}\n\n"

    with open("aloula_live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
    print(f"Successfully scraped {len(channels)} channels.")

if __name__ == "__main__":
    main()
