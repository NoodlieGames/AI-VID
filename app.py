from flask import Flask, render_template, request
import requests, os, time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("PIXVERSE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/", methods=["GET", "POST"])
def index():
    video_url = None

    if request.method == "POST":
        prompt = request.form["prompt"]

        # STEP 1: Generate video
        gen_response = requests.post(
            "https://api.pixverse.ai/v1/video/generate",
            headers=HEADERS,
            json={
                "prompt": prompt,
                "duration": 5,
                "resolution": "720p",
                "style": "cinematic"
            }
        ).json()

        task_id = gen_response.get("task_id")

        # STEP 2: Poll status
        if task_id:
            while True:
                status = requests.get(
                    f"https://api.pixverse.ai/v1/video/status/{task_id}",
                    headers=HEADERS
                ).json()

                if status["status"] == "completed":
                    video_url = status["video_url"]
                    break

                if status["status"] == "failed":
                    break

                time.sleep(3)

    return render_template("index.html", video_url=video_url)

if __name__ == "__main__":
    app.run(debug=True)
