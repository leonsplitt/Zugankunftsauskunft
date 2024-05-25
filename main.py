from datetime import datetime
from typing import Any
import requests


def show_stop(stop_id: int):
    r = requests.get(
        f"https://v6.bvg.transport.rest/stops/{stop_id}/departures",
        params={"results": 5, "duration": 240},
    )
    departures: list[dict[str, Any]] = r.json()["departures"]

    current_time = datetime.now()
    for d in departures:
        show_departure(d, current_time)


def show_departure(departure: dict[str, Any], current_time: datetime):
    when = format_time(departure["when"], current_time)

    direction: str = departure["destination"]["name"]
    direction = direction.split("(Berlin)")[0].strip()

    name: str = departure["line"]["name"]

    print(f"Hello! The {name} to {direction} is coming {when}")


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


def main():
    stops = [
        900078201,  # S Neukölln
        900110521,  # Hufeland
        900110520,  # Bötzowstr.
    ]
    for stop_id in stops:
        show_stop(stop_id)
        print()


main()
