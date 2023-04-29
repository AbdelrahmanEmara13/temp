
import os
import requests
import json
import pandas as pd
import random


user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 525) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) QuickLook/5.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'
]


def read_json(file_path):
    f = open(file_path, "r")
    data = json.loads(f.read())
    f.close()
    return data


def valid_url(url):
    non_html = ['JPG', 'PNG', ' aac', 'abw', 'arc', 'avif', 'avi', 'azw', 'bin', 'bmp', 'bz', 'bz2', 'cda', 'csh', 'css', 'csv', 'doc', 'docx', 'eot', 'epub', 'gz', 'gif',  'ico', 'ics', 'jar', 'jpeg', 'jpg', 'js', 'jsonld', 'mid', 'midi', 'mjs', 'mp3',
                'mp4', 'mpeg', 'mpkg', 'odp', 'ods', 'odt', 'oga', 'ogv', 'ogx', 'opus', 'otf', 'png', 'pdf',  'ppt', 'pptx', 'rar', 'rtf', 'sh', 'svg', 'tar', 'tif', 'tiff', 'ts', 'ttf', 'vsd', 'wav', 'weba', 'webm', 'webp', 'woff', 'woff2',  'xls', 'xlsx',  'xul', 'zip', '3gp', '3g2', '7z']
    if url.split('.')[-1] not in non_html:
        return True


def list_dir(directory_path):
    return os.listdir(directory_path)


def read_history(txt_file):
    return open(txt_file, "r").read().split()


def save_csv(df, site):
    path = f'./csv_files/{site.split(".json")[0]}.csv'
    with open(path, 'w', encoding='utf-8-sig') as f:
        df.to_csv(f)


def get_snapshots(records):
    headers = {'User-Agent': random.choice(user_agent_list)}
    url = f'http://web.archive.org/cdx/search/cdx?url={record[0]}&from={record[1][0:4]}&to={record[2][0:4]}&filter=mimetype:text/html&fl=original,timestamp&output=json'
    df = pd.DataFrame()
    for record in records:
        try:
            if valid_url(record[0]):
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    res = response.json()[1:]
                    temp = pd.DataFrame(res)
                    df = pd.concat([df, temp],  axis=0)
                else:
                    try:

                        prox=f'http://api.scraperapi.com?api_key=7bd3ff8c369d22a9e47ae78aad1f912b&url={url}'
                        response = requests.get(prox, headers=headers)
                        if response.status_code == 200:
                            res = response.json()[1:]
                            temp = pd.DataFrame(res)
                            df = pd.concat([df, temp],  axis=0)

                    except Exception as e: print(e)
        except Exception as e:
            print(e)
    return df


def main():
    history = list_dir('./csv_files')
    files_in_sites_folder = list_dir('./sites_json')

    for site in files_in_sites_folder:
        if site not in history:
            records = read_json(f'./sites_json/{site}')
            df = get_snapshots(records=records)
            save_csv(site=site, df=df)


if __name__ == "__main__":
    main()
