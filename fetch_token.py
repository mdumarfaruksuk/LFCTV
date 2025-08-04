import requests
import json

# Step 1: Define MUX API endpoint and headers
url = "https://streaming-api.mux.com/video/token"
headers = {
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json"
}

# Step 2: Define POST data (you can customize these values)
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

# Step 3: Send POST request
response = requests.post(url, headers=headers, json=payload)

# Step 4: Parse token from response
try:
    token = response.json()["data"]["attributes"]["token"]
except KeyError:
    print("❌ Token fetch failed. Response was:", response.text)
    exit(1)

# Step 5: Create stream URL
base_url = "https://stream.mux.com/LkTxt4ttN5M0189t99NDaie1pXN9LBFqsickK5XHO15Q"
stream_url = f"{base_url}?token={token}"

# Step 6: Write stream URL to stream_url.txt
with open("stream_url.txt", "w") as f:
    f.write(stream_url)

# Step 7: Write M3U8 format to mux_stream.m3u8
with open("mux_stream.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write("#EXT-X-STREAM-INF:BANDWIDTH=2500000\n")
    f.write(stream_url + "\n")

print("✅ Token fetched and files created successfully.")
