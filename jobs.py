import requests
import pandas as pd
from bs4 import BeautifulSoup


# URL address to be scraped
base_url = "https://www.jobs.cz/prace/plzensky-kraj/is-it-vyvoj-aplikaci-a-systemu/?q%5B%5D=python"
page = requests.get(base_url)

# Check if get request is successful
if page.status_code == requests.codes.ok:
    # Get the whole webpage in beautiful soup format
    bs = BeautifulSoup(page.text, "lxml")

# Dictionary for scraped data
data = {
    "position": [],
    "company": [],
    "address": [],
    "updated": [],
    "link": []
}
# List of all job postings
all_jobs = bs.find_all("div", class_="standalone search-list__item")
# Iterate through all postings
for job in all_jobs:
    # If the required information is found, store it to data dictionary
    position = job.find(class_="search-list__main-info__title__link")
    if position:
        data["position"].append(position.text)
    else:
        data["position"].append("none")

    company = job.find(class_="search-list__main-info__company")
    if company:
        data["company"].append(company.text.strip())
    else:
        data["company"].append("none")

    address = job.find(class_="search-list__main-info__address")
    if address:
        data["address"].append(address.find("span").next_sibling.text.strip())
    else:
        data["address"].append("none")

    updated = job.find(class_="label-added")
    if updated:
        data["updated"].append(updated.text)
    else:
        data["updated"].append("none")
    
    link = job.find("a")
    if link:
        data["link"].append(link["href"])
    else:
        data["link"].append("none")
    
table = pd.DataFrame.from_dict(data)
table = table[table.position != "none"]
print(table)
table.to_csv("job_cz.csv", index=False)

