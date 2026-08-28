# ============ KONFIGURASI SENTRAL ============
import os
from datetime import datetime

# === API CONFIG ===
MAX_THREADS = 50
RETRY_COUNT = 3
TIMEOUT = 8
USE_PROXY = True

# === PROXY CONFIG ===
PROXY_LIST = [
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

# === WHATSAPP CONFIG ===
WA_BUSINESS_TOKEN = "EAAG..."  # Ganti pake token asli
PHONE_ID = "123456789012345"

# === LOGGING CONFIG ===
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = f"{LOG_DIR}/chaos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# === USER-AGENT ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
]

# === TELEGRAM BOT CONFIG (Opsional) ===
TELEGRAM_BOT_TOKEN = None  # Isi kalo mau pake notif ke Telegram
TELEGRAM_CHAT_ID = None