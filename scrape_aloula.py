import requests
import json

# The API Endpoint
API_URL = "https://aloula.faulio.com/api/v1/channels"

# Headers are CRITICAL. Without these, the server returns 403 or empty data.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://aloula.sa/",
    "Origin": "https://aloula.sa",
    "Accept": "application/json"
}

def get_channel_list():
    try:
        print(f"Connecting to {API_URL}...")
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"Failed! Status Code: {response.status_code}")
            return []

        data = response.json()
        
        # The API usually wraps channels in a 'data' key
        if isinstance(data, dict):
            channels = data.get('data', [])
        else:
            channels = data
            
        print(f"Found {len(channels)} channels.")
        return channels

    except Exception as e:
        print(f"Error during API request: {e}")
        return []

def create_m3u(channels):
    m3u_lines = ["#EXTM3U"]
    
    for ch in channels:
        # Extract metadata with fallbacks
        name = ch.get('title') or ch.get('name', 'Unknown')
        # Logos are often in 'full' inside 'image' or just 'full'
        logo = ch.get('full') or (ch.get('image', {}).get('full') if isinstance(ch.get('image'), dict) else "")
        
        # Get the stream URL - Check multiple common keys
        stream = ch.get('stream_url') or ch.get('hls_url') or ch.get('url')
        
        if stream:
            m3u_lines.append(f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" tvg-logo="{logo}", {name}')
            # Add VLC specific user-agent option to the stream itself
            m3u_lines.append('#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"')
            m3u_lines.append(stream)
    
    return "\n".join(m3u_lines)

if __name__ == "__main__":
    channels = get_channel_list()
    if channels:
        content = create_m3u(channels)
        with open("aloula_live.m3u", "w", encoding="utf-8") as f:
            f.write(content)
        print("M3U file generated successfully!")
    else:
        print("No channels found. Check if the API URL or Headers need updating.")
