import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import html


urls = [
    'https://moodle.technikum-wien.at/user/view.php?id=35966&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35977&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36495&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36488&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35971&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32823&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32911&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32559&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35964&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35980&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35982&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36496&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35968&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33172&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35981&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36497&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36498&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36500&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36499&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35976&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35967&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35974&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36501&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35978&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36489&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32560&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33745&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36502&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36149&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35983&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=34368&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33710&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33173&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32562&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32912&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33483&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33591&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32563&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32824&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36084&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32564&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33174&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33175&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33711&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35970&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33724&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33498&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32916&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36503&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35973&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32825&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32826&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=30332&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=34280&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36504&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35972&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=34338&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35969&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36505&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33176&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32827&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35979&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36506&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32565&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36507&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35975&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33626&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=34890&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32566&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=32913&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33177&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=33091&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36508&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36148&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=35965&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36509&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=34282&course=25851',
    'https://moodle.technikum-wien.at/user/view.php?id=36510&course=25851'
]


def decode_email(encoded_string):
    """Decode email from obfuscated format."""
    pattern = re.compile(r'mailto:([^\"]+)')
    match = pattern.search(encoded_string)
    if match:
        email = match.group(1)
        return bytes(email, 'utf-8').decode('unicode_escape')
    return None


def extract_emails_from_url(url):
    response = requests.get(url, headers={'Cookie': 'MoodleSession=???'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        dt_elements = soup.find_all('dt')
        emails = []
        for dt in dt_elements:
            if dt.text.strip() == 'E-Mail-Adresse':
                dd = dt.find_next('dd')
                if dd:
                    encoded_email = dd.find('a')['href']
                    decoded_email = decode_email(encoded_email)
        return decoded_email
    return []


def decode_email(encoded_email):
    decoded_html_entities = html.unescape(encoded_email)
    decoded_email = decoded_html_entities.split(':')[1]
    decoded_email = unquote(decoded_email)
    return decoded_email


all_emails = []
for url in urls:
    email = extract_emails_from_url(url)
    all_emails.append(email)

print(all_emails)
