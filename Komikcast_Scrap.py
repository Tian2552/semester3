import requests
from bs4 import BeautifulSoup
import csv

def get_komik_details(komik_url):
    response = requests.get(komik_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    komik_details = {
        'Status': 'N/A',
        'Type': 'N/A',
        'Released': 'N/A',
        'Author': 'N/A',
        'Description': 'N/A',
        'Rating': 'N/A'
    }
    
    info_table = soup.find('table', class_='infotable')
    if info_table:
        rows = info_table.find_all('tr')
        for row in rows:
            key = row.find('td').text.strip()
            value = row.find_all('td')[1].text.strip()
            if key == 'Status':
                komik_details['Status'] = value
            elif key == 'Type':
                komik_details['Type'] = value
            elif key == 'Released':
                komik_details['Released'] = value
            elif key == 'Author':
                komik_details['Author'] = value

    description = soup.find('div', class_='entry-content').find('p').text if soup.find('div', class_='entry-content') and soup.find('div', class_='entry-content').find('p') else 'N/A'
    komik_details['Description'] = description

    rating = soup.find('div', class_='num')
    if rating:
        komik_details['Rating'] = rating.get('content', 'N/A') 
    
    return komik_details

def scrap_komik_page(page_number):
    url = f'https://komiku.com/komikcast/page/{page_number}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data_list = []
    
    komik_items = soup.find_all('div', class_='bs')
    
    for komik in komik_items:
        title = komik.find('div', class_='tt').text if komik.find('div', class_='tt') else 'N/A'
        chapter = komik.find('div', class_='adds').text if komik.find('div', class_='adds') else 'N/A'
        
        warna = 'Yes' if komik.find('span', class_='colored') else 'No'
        
        link_gambar = komik.find('img')['src'] if komik.find('img') else 'N/A'
        link_komik = komik.find('a')['href'] if komik.find('a') else 'N/A'
        
        komik_details = get_komik_details(link_komik)
        
        data_list.append([
            title, 
            chapter, 
            warna,
            komik_details['Rating'],
            komik_details['Status'],
            komik_details['Type'],
            komik_details['Released'],
            komik_details['Author'],
            komik_details['Description'],
            link_gambar, 
            link_komik
            
        ])
    
    return data_list

all_data = []

for page in range(1, 3):
    all_data.extend(scrap_komik_page(page))

with open('komik_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Title', 
        'Chapter', 
        'Berwarna', 
        'Rating', 
        'Status',
        'Type',
        'Released',
        'Author',
        'Description',
        'link_gambar',
        'link_komik'
    ])
    writer.writerows(all_data)

print("Data berhasil disimpan ke komik_data.csv")
