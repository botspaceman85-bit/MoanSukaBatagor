import random
import requests
from config import PROXY_LIST

class ProxyManager:
    def __init__(self):
        self.proxies = PROXY_LIST.copy()
        self.current_index = 0
        self.working_proxies = []
    
    def get_proxy(self):
        """Ambil proxy random"""
        if not self.proxies:
            self.proxies = PROXY_LIST.copy()
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.current_index += 1
        return proxy
    
    def test_proxy(self, proxy):
        """Test proxy apakah working"""
        try:
            test_url = "http://httpbin.org/ip"
            proxies = {'http': proxy, 'https': proxy}
            resp = requests.get(test_url, proxies=proxies, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def get_working_proxies(self):
        """Dapatkan daftar proxy yang working"""
        working = []
        for proxy in self.proxies:
            if self.test_proxy(proxy):
                working.append(proxy)
        self.working_proxies = working
        return working
    
    def rotate_proxy(self):
        """Rotate proxy"""
        if not self.working_proxies:
            self.get_working_proxies()
        if self.working_proxies:
            return random.choice(self.working_proxies)
        return None
    
    def add_proxy(self, proxy):
        """Tambah proxy baru"""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            return True
        return False