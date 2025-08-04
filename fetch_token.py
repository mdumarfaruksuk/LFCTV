import requests, os, json

user_email = os.getenv("USER_EMAIL")
user_id = os.getenv("USER_ID")
video_id = os.getenv("VIDEO_ID")

url = "https://streamline.webapi.gc.lfc-services.co.uk/v2/session/check"
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
headers = {"Content-Type": "application/json"}
r = requests.post(url, json=payload, headers=headers)
token = r.json()["data"]["attributes"]["token"]
stream_url = f"https://stream.mux.com/LkTxt4ttN5M0189t99NDaie1pXN9LBFqsickK5XHO15Q?token={token}"

with open("stream_url.txt", "w") as f:
    f.write(stream_url)

print("✅ Stream URL updated")
