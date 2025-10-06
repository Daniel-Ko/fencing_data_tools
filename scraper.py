import json
import os
from datetime import datetime

import requests
import click
from dotenv import load_dotenv

def get_tournaments_with_token(params):
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
    
    print(params)
    print(f"Fetching {params['filter']}")
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



@click.command()
@click.option("--filter", "-f", type=click.Choice(["All", "FIE",
"Country"], case_sensitive=False), default="All")
@click.option("--country", "-c", default="NZL")
@click.option("--usa", type=click.Choice(["Nat", "Reg", "Loc"],
case_sensitive=False), default="Loc")
@click.option("--region", "-r", default=0)
@click.option('--state', '-s', default='CA')
@click.option("--local", "-l")
@click.option("--date", "-d")
def main(filter, country, usa, region, state, local, date):
    params = locals()
    if country:
        params["filter"] = "Country"
        params["country"] = country.upper()
    params["filter"] = params["filter"].title()
    params["usa"] = params["usa"].title()

    params["today"] = datetime.today().strftime("%Y-%m-%d")
    params["grt"] = os.getenv("GRT_TOKEN")
    tournaments = get_tournaments_with_token(params)
    print_tournaments(tournaments)
        
    if tournaments:
        with open("tournaments.json", "w") as f:
            json.dump(tournaments, f, indent=2)
            print("\n✓ Saved to tournaments.json")

if __name__ == "__main__":
    load_dotenv()    
    main()    

