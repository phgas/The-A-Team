import requests
import json


emails = ['amzabogdan15@gmail.com', 'roybachynskyi@gmail.com', 'mb23x005@technikum-wien.at', 'mb23x502@technikum-wien.at', 'jawharb3@gmail.com', 'mb23m009@technikum-wien.at', 'mb23m015@technikum-wien.at', 'mb23m001@technikum-wien.at', 'chams.eddine.bersali@gmail.com', 'kitdinu12@gmail.com', 'ncojocaru92@gmail.com', 'mb23x006@technikum-wien.at', 'amadoudian232@gmail.com', 'mb23m020@technikum-wien.at', 'andreeadinica41@yahoo.com', 'mb23x007@technikum-wien.at', 'mb23x008@technikum-wien.at', 'mb23x010@technikum-wien.at', 'mb23x009@technikum-wien.at', 'robert.dumitru2002@gmail.com', 'vladandrei03@yahoo.com', 'oussemahawat20@gmail.com', 'mb23x011@technikum-wien.at', 'nferturk@gmail.com', 'mb23x503@technikum-wien.at', 'mb23m002@technikum-wien.at', 'mb23m033@technikum-wien.at', 'mb23x012@technikum-wien.at', 'darya.gladkyh@gmail.com', 'grigoras.sebastian17@gmail.com', 'mb23m038@technikum-wien.at', 'mb23m030@technikum-wien.at', 'mb23m021@technikum-wien.at', 'mb23m004@technikum-wien.at', 'mb23m016@technikum-wien.at', 'mb23m027@technikum-wien.at', 'mb23m028@technikum-wien.at', 'mb23m005@technikum-wien.at', 'mb23m010@technikum-wien.at', 'mb23m006@technikum-wien.at', 'mb23m022@technikum-wien.at', 'mb23m023@technikum-wien.at', 'mb23m031@technikum-wien.at', 'kenza.gaaia@gmail.com', 'mb23m032@technikum-wien.at', 'ma0506@technikum-wien.at', 'mb23m018@technikum-wien.at', 'mb23x013@technikum-wien.at', 'mb23m011@technikum-wien.at', 'mb23m012@technikum-wien.at', 'mb22m034@technikum-wien.at', 'mb23m035@technikum-wien.at', 'mb23x014@technikum-wien.at', 'cristianaprecup65@gmail.com', 'mb23m037@technikum-wien.at', 'mihaiprodann@gmail.com', 'mb23x015@technikum-wien.at', 'mb23m024@technikum-wien.at', 'mb23m013@technikum-wien.at', 'antorotaru@gmail.com', 'mb23x016@technikum-wien.at', 'mb23m007@technikum-wien.at', 'mb23x017@technikum-wien.at', 'vlad1rusu@yahoo.com', 'mb23m029@technikum-wien.at', 'mb23m039@technikum-wien.at', 'mb23m008@technikum-wien.at', 'mb23m017@technikum-wien.at', 'mb23m025@technikum-wien.at', 'mb23m019@technikum-wien.at', 'mb23x018@technikum-wien.at', 'kaanmeister.ro@gmail.com', 'mb23x019@technikum-wien.at', 'mb23m036@technikum-wien.at']


for email in emails:

    url = "http://127.0.0.1:8000/generate_key"

    payload = json.dumps({
        "email": email,
        "subscription_type": "premium"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'SUPER_SECRET'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        print(f"[{email}]: Successfully generated key {response.json()['api_key']}")
