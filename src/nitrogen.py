import requests, threading, sys
import time
import random
from requests.exceptions import ProxyError, SSLError, ConnectionError, InvalidProxyURL

proxies = []

szal = int(input("Szálak: "))
try:
    with open('proxies.txt') as fp:
        line = fp.readline()
        while line:
            proxies.append(line.strip())
            line = fp.readline()
except:
    sys.exit("Nincs proxies.txt fájl!")

def codeGenerator():
    hossz = 16
    betu = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(betu) for i in range(hossz))

def proxygen():
    return random.choice(proxies)


class fő(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tasks = []

    def run(self):
        i = 0
        while True:
            code = codeGenerator()
            url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
            cp = proxygen()
            proxy = {'https': cp}
            try:
                res = requests.get(url, proxies=proxy).text
                if (not "Unknown Gift Code" in res) and (not "You are being rate limited." in res):
                    print(res)
                    with open('nitrocodes.txt', 'a') as f:
                        f.write(f"Kód: {code}\n")
                    print(f"\033[0mÉRVÉNYES KÓD!\n---------------------\nKód: {code}\n-------------------")
                else:
                    print(f"\033[0m{code} ellenőrizve!\nÁllapot: Érvénytelen!")
                i += 1
                time.sleep(1)
            except ProxyError:
                print("\033[91mProxy hiba!")
                continue
            except InvalidProxyURL:
                print("\033[91mÉrvénytelen proxy!")
                continue
            except SSLError:
                print("\033[91mSSL hiba!")
                continue
            except ConnectionError:
                print("\033[91mCsatlakzási hiba!")
                continue

threads = []
for x in range(szal):
    threads.append(fő())

for thread in threads:
    thread.daemon = True
    thread.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\033[0m\nKilépés...")
        exit(0)
