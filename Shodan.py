import time
import requests
import re
import os
import json
import secrets
import string

banner = """
.▄▄ ·  ▄ .▄      ·▄▄▄▄   ▄▄▄·  ▐ ▄      ▄▄ • ▄▄▄ . ▐ ▄ ▄▄▄ .▄▄▄   ▄▄▄· ▄▄▄▄▄      ▄▄▄  
▐█ ▀. ██▪▐█▪     ██▪ ██ ▐█ ▀█ •█▌▐█    ▐█ ▀ ▪▀▄.▀·•█▌▐█▀▄.▀·▀▄ █·▐█ ▀█ •██  ▪     ▀▄ █·
▄▀▀▀█▄██▀▐█ ▄█▀▄ ▐█· ▐█▌▄█▀▀█ ▐█▐▐▌    ▄█ ▀█▄▐▀▀▪▄▐█▐▐▌▐▀▀▪▄▐▀▀▄ ▄█▀▀█  ▐█.▪ ▄█▀▄ ▐▀▀▄ 
█▄▪▐███▌▐▀▐█▌.▐▌██. ██ ▐█ ▪▐▌██▐█▌    ▐█▄▪▐█▐█▄▄▌██▐█▌▐█▄▄▌▐█•█▌▐█ ▪▐▌ ▐█▌·▐█▌.▐▌▐█•█▌
▀▀▀▀ ▀▀▀ · ▀█▄▀▪▀▀▀▀▀•  ▀  ▀ ▀▀ █▪    ·▀▀▀▀  ▀▀▀ ▀▀ █▪ ▀▀▀ .▀  ▀ ▀  ▀  ▀▀▀  ▀█▄▀▪.▀  ▀
Добро пожаловать в шодан генератор!
"""
# уберите детей от экрана
class Mail:
    main_url = "https://temp-mail.io/en"
    api_url = "https://api.internal.temp-mail.io/api/v2/email/new"

    def __init__(self, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"):
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": ua
        })

    def create(self, min_len=10, max_len=10):
        self.session.get(self.main_url)
        data = {"min_name_length": str(min_len), "max_name_length": str(max_len)}
        response = self.session.post(self.api_url, data=data).json()
        self.email = response["email"]
        self.password = self.genpass()
        return self.email, self.password

    def genpass(self, length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    def readmail(self):
        url = f"https://api.internal.temp-mail.io/api/v2/email/{self.email}/messages"
        return self.session.get(url).content.decode("utf-8")

class pizdecnaxyi:
    main_url = "https://account.shodan.io"
    reg_url = f"{main_url}/register"
    login_url = f"{main_url}/login"

    def __init__(self, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"):
        self.session = requests.Session()
        self.session.headers.update({
            "origin": self.main_url,
            "referer": self.reg_url,
            "user-agent": ua
        })
        self.mail = Mail()
        self.account_count = 0

    def regacc(self):
        self.user = self.mail.genpass(length=12)
        self.mail.create()
        self.passwd = self.mail.password
        page = self.session.get(self.reg_url)
        token = re.search(r'csrf_token.*="(\w*)"', page.text).group(1)
        data = {"username": self.user, "password": self.passwd, "password_confirm": self.passwd, "email": self.mail.email, "csrf_token": token}
        response = self.session.post(self.reg_url, data=data).text
        if "Please check the form and fix any errors" not in response:
            self.session.get(self.main_url)
            return self.mail.email, self.passwd
        return None

    def activateacc(self):
        retries = 15
        retry = 0
        while retry < retries: # у создателя точно кто то сдох
            try:
                activation = re.search(r'(https://account.shodan.io/activate/\w*)', self.mail.readmail()).group(1)
            except KeyboardInterrupt:
                return None
            except Exception as e:
                retry += 1
                time.sleep(3)
                continue
            else:
                break
        if retry == retries:
            print("Не получилось принять сообщение почты!")
            return None
        self.session.get(activation)
        with open('accounts.txt', 'a', encoding='utf-8') as f:
            self.account_count += 1
            f.write(f"[{self.account_count}] Данные от аккаунта: {self.user}:{self.passwd}\n")

    def bananchiki(self):
        print(f"[{self.account_count}] Сгенерировал аккаунт вот данные: {self.user}:{self.passwd} > accounts.txt")
        response = self.session.get(self.login_url)
        match = re.search(r'csrf_token.*="(\w*)"', response.text)
        if match is not None:
            token = match.group(1)
            data = {"username": self.user, "password": self.passwd, "grant_type": "password", "continue": self.main_url, "csrf_token": token, "login_submit": "Login"}
            response = self.session.post(self.login_url, data=data).text
            res = self.session.get(self.main_url).text
            match = re.search(r'<td>(\w*)<br /><br />', res)
            if match is not None:
                api = match.group(1)
            else:
                time.sleep(2)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    generator = pizdecnaxyi()
    print(banner)
    num_acc = int(input("Сколько аккаунтов будут сгенерированы? "))
    print("Начинаю генерацию...")
    for i in range(num_acc):
        info = generator.regacc()
        if info:
            time.sleep(3)
            generator.activateacc()
            generator.bananchiki() 
            time.sleep(3)
        else:
            print("Никнейм или почта занята!")

if __name__ == "__main__":
    main()
