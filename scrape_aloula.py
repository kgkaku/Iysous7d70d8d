import requests
import os

# API Endpoint for Aloula Channels
API_URL = "https://aloula.faulio.com/api/v1/channels"

def fetch_channels():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching API: {e}")
        return None

def generate_m3u(data):
    # EXT-X-VLC-OPT format requires specific tagging
    m3u_content = "#EXTM3U\n"
    
    # The API returns a list under a key, usually 'data' or directly as a list
    channels = data if isinstance(data, list) else data.get('data', [])

    for channel in channels:
        title = channel.get('title', 'Unknown Channel')
        # Some APIs use 'logo', 'full', or 'image' for the icon
        logo = channel.get('full') or channel.get('image', '')
        
        # Extracting the stream URL (usually under 'stream_url' or 'hls_url')
        stream_url = channel.get('stream_url')
        
        if stream_url:
            # Build the M3U entry
            m3u_content += f'#EXTINF:-1 tvg-name="{title}" tvg-logo="{logo}", {title}\n'
            # Adding VLC specific options (User-Agent is often required to avoid 403 errors)
            m3u_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n"
            m3u_content += f"{stream_url}\n\n"

    return m3u_content

if __name__ == "__main__":
    channel_data = fetch_channels()
    if channel_data:
        m3u_result = generate_m3u(channel_data)
        with open("aloula_live.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_result)
        print("Success: aloula_live.m3u has been generated.")
