import os


class Config:
    headers = {
        'authority': 'projects.propublica.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        # 'cookie': '_cfuvid=qarxXCaXvSE2ObQXrtZPyhyVG514kviO3oaynUtCwZM-1703265268570-0-604800000; pp-tracking={"pageCount":0}; _cb=CXd2-3Y9UhFBWhieb; _chartbeat2=.1703265270296.1703265270296.1.CTyrGNFa_xDDLBvMoBoPLVgB1GEtP.1; _cb_svref=external; _ga=GA1.2.1048516087.1703265271; _gid=GA1.2.2083575960.1703265271; sailthru_pageviews=1; sailthru_content=744efcc450bd64064b9dcbfb86a237b2; sailthru_visitor=8734c3db-87ed-4d35-8cb3-a273480f1961; _ga_K9RW8M6GL5=GS1.1.1703265271.1.1.1703265516.44.0.0',
        'referer': 'https://projects.propublica.org/nypd-ccrb/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    }
    BASE_URL = 'https://projects.propublica.org'


class PostgresConfig:
    POSTGRES_LOGIN = os.environ.get('POSTGRES_LOGIN', 'postgres')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '1912')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5433')
    POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE', 'postgres')
