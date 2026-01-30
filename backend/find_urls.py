import requests

base_urls = [
    "https://raw.githubusercontent.com/pavitrakumar78/Vedas-Dataset/master/",
    "https://raw.githubusercontent.com/pavitrakumar78/Vedas-Dataset/main/",
]

files = [
    "Rigveda/rigveda.csv", 
    "Rigveda/Rigveda.csv", 
    "Rigveda/rigveda_clean.txt",
    "RigVeda/rigveda.csv"
]

print("Testing URLs...")
for base in base_urls:
    for f in files:
        url = base + f
        try:
            r = requests.head(url)
            if r.status_code == 200:
                print(f"FOUND: {url}")
        except:
            pass
