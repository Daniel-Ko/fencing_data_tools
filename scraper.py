import json
import os

import requests
import click
from dotenv import load_dotenv

def get_tournaments_with_token(grt_token, state="CA"):
    """
    Get tournaments using a manually obtained reCAPTCHA token
    
    Here is the order of API filters:
        "filter" > "country" 

    Args:
        grt_token: The reCAPTCHA token from browser DevTools
        state: US state code
    
    Returns:
        List of tournaments
    """
    url = "https://www.fencingtimelive.com/tournaments/search/data"
    
    params = {
        "filter": "Country", # "All", "FIE", "Country" (default=All)
        "usa": "Loc", # "Nat", "Reg", "Loc" (default=Loc)
        "country": "AUS", # (default=USA)
        "region": 0, # 1 to 6 (default=0)
        "local": "State", 
        "state": state,
        "date": 0,
        "today": "2025-10-05",  # Update this to current date
        "grt": grt_token
    }
    
    print(f"Fetching tournaments for {state}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []


def print_tournaments(tournaments):
    """Print tournament details"""
    if not tournaments:
        print("No tournaments found!")
        return
    
    print(f"\nFound {len(tournaments)} tournaments!\n")
    print("="*60)
    
    for i, t in enumerate(tournaments[:10], 1):
        print(f"\n{i}. {t['name']}")
        print(f"   Location: {t['location']}")
        print(f"   Dates: {t['dates']}")
        print(f"   ID: {t['id']}")
    
    if len(tournaments) > 10:
        print(f"\n...and {len(tournaments) - 10} more")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    load_dotenv()    

    GRT_TOKEN = os.getenv("GRT_TOKEN")
    tournaments = get_tournaments_with_token(GRT_TOKEN, state="CA")
    print_tournaments(tournaments)
        
    if tournaments:
        with open("tournaments.json", "w") as f:
            json.dump(tournaments, f, indent=2)
            print("\n✓ Saved to tournaments.json")
