"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Pavel Nováček
email: gippel@seznam.cz
"""

import argparse
import sys
import requests
from bs4 import BeautifulSoup as bs
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--district_ref", type=str, required=True)
parser.add_argument("--file_name", type=str, required=True)

def get_data(adress: str):
    """
    Gets html from url.
    """
    try:
        data = requests.get(adress, timeout=5)
        data.raise_for_status()
        return data
    except requests.RequestException:
        print("Error while gitting the data.")

def data_to_soup(data) -> bs:
    """
    Transforms data to BeautifulSoup file.
    """
    soup = bs(data.text, features="html.parser")
    return soup

def find_all_references(soup: bs) -> list[list[str]]:
    """
    Filters all references from a district url under 
    which there are references for villages names and voting results.
    """
    all_references = []
    references_tag_a = soup.find_all("td",
                              {"class": "cislo"},
                              {"headers": "t1sa1 t1sb1"})
    for line in references_tag_a:
        reference = (line.find("a"))
        all_references.append([reference["href"], reference.string])
    return all_references

def find_name(soup: bs) -> str:
    """
    Finds the name of the village.
    """
    code_filter = soup.find("div", {"id": "publikace"}).find_all("h3")
    code = code_filter[2].string[7:].strip()
    return code

def find_all_rows_in_table(soup: bs, index: int) -> list:
    """
    Finds a "table" tag according to index with class: table in a soup file.
    Then finds all "tr" tags.
    """
    tables = soup.find_all("table", {"class": "table"})
    select_table = tables[index]
    all_rows = select_table.find_all("tr")
    return all_rows

def find_all_columns(all_rows: list) -> list[list[str]]:
    """
    Finds all "td" tags in a soup file
    with filtered "tr" tags.
    """
    all_columns = []
    for row in all_rows:
        tds = row.find_all("td")
        if tds:
            all_columns.append([td.text for td in tds])
    return all_columns

def table_1_filter(data: list) -> list[str]:
    """
    Filters numbers from the first table.
    """
    indexes = [3, 4, 7]
    result = [data[i] for i in indexes]
    return result

def add_parties(data: list[list[str]], data_output: list[str]):
    """
    Adds names of political parties from tables. 
    """
    for line in data:
        data_output.append(line[1])

def add_votes(data: list[list[str]]) -> list[str]:
    """
    Adds votes from a table.
    """
    votes = []
    for line in data:
        votes.append(line[2])
    return votes

def save_to_csv(data: list[list[str]], name_of_file: str):
    """
    Creates a csv file and saves data into it.
    """
    with open(name_of_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(data)

def main(list_of_references: list[str]) -> list[list[str]]:
    result_list = []
    for e, reference in enumerate(list_of_references):
        
        web_address = (f"https://www.volby.cz/pls/ps2017nss/{reference[0]}")
        code = [reference[1]]

        village_html = get_data(web_address)
        village_soup = data_to_soup(village_html)
        name = [find_name(village_soup)]

        table_1_rows = find_all_rows_in_table(village_soup, 0)
        table_1_columns = find_all_columns(table_1_rows)
        table_1_result = table_1_filter(table_1_columns[0])

        table_2_rows = find_all_rows_in_table(village_soup, 1)
        table_2_columns = find_all_columns(table_2_rows)
        table_2_votes = add_votes(table_2_columns)

        table_3_rows = find_all_rows_in_table(village_soup, 2)
        table_3_columns = find_all_columns(table_3_rows)
        table_3_votes = add_votes(table_3_columns)
        
        if e == 0:
            headers = ["Code", "Name", "Voters on the list",
                       "Issued envelopes", "Valid votes"]
            add_parties(table_2_columns, headers)
            add_parties(table_3_columns, headers)
            result_list.append(headers)
            
        merged = code + name + table_1_result + table_2_votes + table_3_votes

        result_list.append(merged)
    return result_list

args = parser.parse_args()

district = args.district_ref
file_name = args.file_name

if not district.startswith("http"):
    print("Invalid URL.")
    sys.exit(1)

if not file_name.endswith(".csv"):
    print("--file_name arguments must end with .csv")
    sys.exit(1)

references_html = get_data(district)
references_soup = data_to_soup(references_html)
references_list = find_all_references(references_soup)

if __name__ == "__main__":
    save_to_csv(main(references_list), file_name)












