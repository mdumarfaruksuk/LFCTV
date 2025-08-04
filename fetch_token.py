import requests
import json

API_URL = "https://streamline.webapi.gc.lfc-services.co.uk/v2/session/check"
MUX_BASE = "https://stream.mux.com/LkTxt4ttN5M0189t99NDaie1pXN9LBFqsickK5XHO15Q"

# Direct payload
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

# Make POST request
try:
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ Request failed: {e}")
    exit(1)

# Parse response
try:
    data = response.json()
except json.JSONDecodeError:
    print("❌ Could not parse JSON response.")
    print(response.text)
    exit(1)

# Extract token
try:
    token = data["data"]["attributes"]["token"]
except KeyError:
    print("❌ Token not found in response:")
    print(json.dumps(data, indent=2))
    exit(1)

# Final streaming URL
mux_url = f"{MUX_BASE}?token={token}"

# Save plain URL
with open("stream_url.txt", "w") as f:
    f.write(mux_url)

# Save M3U8 formatted file
with open("mux_stream.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write("#EXT-X-STREAM-INF:BANDWIDTH=2500000\n")
    f.write(mux_url + "\n")

print("✅ Stream URL written to:")
print(" - stream_url.txt")
print(" - mux_stream.m3u8")
