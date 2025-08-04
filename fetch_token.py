import os
import sys
import requests
import json

API_URL = "https://streamline.webapi.gc.lfc-services.co.uk/v2/session/check"
MUX_BASE = "https://stream.mux.com/LkTxt4ttN5M0189t99NDaie1pXN9LBFqsickK5XHO15Q"

# Get environment variables
user_email = os.getenv("USER_EMAIL")
user_id = os.getenv("USER_ID")
video_id = os.getenv("VIDEO_ID")

# Validate inputs
if not all([user_email, user_id, video_id]):
    print("❌ Error: One or more environment variables (USER_EMAIL, USER_ID, VIDEO_ID) are missing.")
    sys.exit(1)

# Prepare payload for POST request
payload = {
    "data": {
        "attributes": {
            "videoID": video_id,
            "mediaType": "live-stream",
            "userID": user_id,
            "userEmail": user_email
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise HTTP error if not 200
except requests.RequestException as e:
    print(f"❌ POST request failed: {e}")
    sys.exit(1)

try:
    data = response.json()
except json.JSONDecodeError:
    print(f"❌ Failed to parse JSON response:\n{response.text}")
    sys.exit(1)

# Check if 'data' exists in response
if "data" not in data:
    print("❌ API response does not contain 'data' key. Full response:")
    print(json.dumps(data, indent=2))
    sys.exit(1)

# Extract token
try:
    token = data["data"]["attributes"]["token"]
except KeyError:
    print("❌ Token not found in API response. Full response:")
    print(json.dumps(data, indent=2))
    sys.exit(1)

# Construct full MUX URL with token
mux_url = f"{MUX_BASE}?token={token}"

# Save to file
with open("stream_url.txt", "w") as f:
    f.write(mux_url)

print(f"✅ Token fetched and saved to stream_url.txt:\n{mux_url}")
