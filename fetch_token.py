import requests
import json

API_URL = "https://streamline.webapi.gc.lfc-services.co.uk/v2/session/check"
MUX_BASE = "https://stream.mux.com/LkTxt4ttN5M0189t99NDaie1pXN9LBFqsickK5XHO15Q"

# Payload to POST
payload = {
    "data": {
        "attributes": {
            "videoID": "8a25b396-f7d7-47d7-aa0b-4adb131ddfc5",
            "mediaType": "live-stream",
            "userID": "9131324",
            "userEmail": "mdumarfaruksuk0@gmail.com"
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

# Step 1: Get token from API
try:
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    token = response.json()["data"]["attributes"]["token"]
except Exception as e:
    print("❌ Failed to fetch token:", e)
    exit(1)

# Step 2: Generate full MUX URL
mux_url = f"{MUX_BASE}?token={token}"

# Step 3: Save MUX URL in a .txt file
with open("stream_url.txt", "w") as f:
    f.write(mux_url)

print("✅ mux_url saved to stream_url.txt")

# Step 4: Fetch M3U8 data from mux_url
try:
    m3u8_response = requests.get(mux_url)
    m3u8_response.raise_for_status()
    m3u8_content = m3u8_response.text
except Exception as e:
    print("❌ Failed to fetch M3U8 content:", e)
    exit(1)

# Step 5: Save M3U8 content in a separate .m3u8 file
with open("live.m3u8", "w") as f:
    f.write(m3u8_content)

print("✅ M3U8 content saved to live.m3u8")
