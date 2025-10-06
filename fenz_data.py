from dotenv import load_dotenv

import click
import requests


def fetch(endpoint):
    print(endpoint)
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []

def search_exact_name(endpoint, target_name) -> list[int]:
    name_list = fetch(endpoint)["items"]
    target_name = target_name.lower()

    name_ids = []
    for data in name_list:
        if data["name"].lower() == target_name:
            name_ids.append(data["uid"])

    return name_ids

def reverse_name(name):
    curr_name = name.lower().split(" ")
    curr_name[0], curr_name[-1] = curr_name[-1], curr_name[0]
    return " ".join(curr_name)
    

@click.command()
# surname search. If full name is passed, then it goes SURNAME&ETC
@click.option("--name", "-n")
# Assume exact name is passed if a space is found in name
@click.option("--exact_name", "-e", is_flag=True)
@click.option("--weapon", "-w", default="sabre")
@click.option("--category", "-c", default="open")
def main(name, exact_name, weapon, category):
    url = "https://api.fencing.org.nz/public/"
    if name:    
        query_params, name_query = "", name

        if " " in name:
            name_query = name.replace(" ", "&")

            if exact_name:
                search_res = search_exact_name(
                    f"{url}name?name={name_query}",
                    reverse_name(name))
                if len(search_res) == 1:
                    query_params = f"fencer?uid={search_res[0]}"
                
        # just a general search for surname/firstname
        if not query_params:
            query_params = f"name?name={name_query}"
        url += query_params
    else:
        url += f"ranking?weapon={weapon}&cat={category}"
    res = fetch(url)
    print(res)

if __name__ == "__main__":
    load_dotenv()
    main()
