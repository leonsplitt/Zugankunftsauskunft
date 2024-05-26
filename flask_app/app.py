from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

def get_departures(stop_id: int):
    r = requests.get(
        f"https://v6.bvg.transport.rest/stops/{stop_id}/departures",
        params={"results": 5, "duration": 240},
    )
    departures = r.json()["departures"]
    current_time = datetime.now()
    return [(format_time(d["when"], current_time), d["destination"]["name"].split("(Berlin)")[0].strip(), d["line"]["name"]) for d in departures]

def format_time(iso_time: str, current_time: datetime) -> str:
    time = datetime.fromisoformat(iso_time)
    current_time = current_time.astimezone(time.tzinfo)
    deltatime = time - current_time
    deltaminutes = int(deltatime.total_seconds() / 60)
    if deltaminutes <= 0:
        return "now"
    elif deltaminutes < 15:
        return f"in {deltaminutes} minutes"
    else:
        return f"at {time.hour:02}:{time.minute:02}"

@app.route('/')
def index():
    stops = [
        # 900078201,  # S Neukölln
        # 900110521,  # Hufeland
        900110520,  # Bötzowstr.
        900170004,  # S Ahrensfelde
        900153500,  # Am Gehrensee

    ]
    stop_departures = {name: get_departures(stop_id) for stop_id, name in stops}
    return render_template('index.html', stop_departures=stop_departures)

if __name__ == '__main__':
    app.run(debug=True)
