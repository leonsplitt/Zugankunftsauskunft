from datetime import datetime
import requests
from typing import Any


def show_stop(stop_id: int):
    r = requests.get(
        f"https://v6.bvg.transport.rest/stops/{stop_id}/departures",
        params= { "results": 5, "duration": 60 }
    )
    departures: list[dict[str, Any]] = r.json()["departures"]
    for d in departures:
        show_departure(d)

def show_departure(departure): 
    when = datetime.fromisoformat(departure["when"])
    direction = departure["destination"]["name"].removesuffix(" (Berlin)")
    name = departure["line"]["name"]
    print(f"Hello! The {name} to {direction} is coming at {when.hour:02}:{when.minute:02}")

def main():
    stops = [
        900078201, # S Neukölln
        900110521, # Hufeland
        900110520, # Bötzowstr.
    ]
    for i in stops:
        show_stop(stop_id=i)
        print()

main()