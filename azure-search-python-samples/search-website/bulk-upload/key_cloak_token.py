import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from time import sleep as wait

class KeyCloakToken():
    """

    """
    base_url = "https://auth.crt.nuance.com/oauth2/auth?response_type=token&state=623969cb-c884-4264-8871-10d4f55e9d3c&redirect_uri=https%3A%2F%2Fmix.nuance.com%2Fv3%2F&client_id=mix-portal-client&provider=mix-mix-portal-client&hash=%23%2Flogin&tenant=mix&skipconsent=true&scope=mix-api"
    referer = "https://mix.nuance.com/v3/"
    username = "aditya.singh@nuance.com"
    password = "<password>"
    end_point = 'https://{}'.format("mix.nuance.com")


    def __init__(self):
        super().__init__()
        self.service_reponse ={}
        self._headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        self._base_url = self.base_url

        self._payload = {
            'username': self.username,
            'password': self.password
        }
        self._master_headers = {
            'User-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36",
            'Referer': self.referer
        }

        self._org_headers = {
            'User-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36",
            'Referer': self._base_url
        }
        self._login_headers = {
            'User-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self._base_url
        }

    def get_access_token(self):
        import requests
        retries = 20

        while retries > 0:
            try:
                _session = requests.Session()
                print("trying again")
                self.r = _session.get(self._base_url, headers=self._master_headers, verify=False)
                self.r = _session.get(self.r.url, headers=self._master_headers, verify=False)
                self._org_return_url = self.get_action_url(self.r)
                self.r = _session.post(self._org_return_url, data=self._payload, headers=self._login_headers, verify=False)
                self._token = self.r.url.split("&")[0].split("=")[-1]
                print(self._token)
                return self._token
            except requests.ConnectionError:
                wait(90)
                retries = retries - 1
                continue
            except TypeError:
                wait(90)
                retries = retries - 1
                continue
            except ConnectionRefusedError:
                wait(90)
                retries = retries - 1
                continue
        return None

    def get_action_url(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        return bs.find(id='kc-form-login')['action']


if __name__ == '__main__':
    kt = KeyCloakToken('')
    print (kt.get_access_token())

