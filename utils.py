import re
import time
import random
import json
import logging
from datetime import datetime
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

class Logger:
    def __init__(self, log_file=None):
        self.log_file = log_file
        if log_file:
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
    
    def info(self, msg):
        print(f"{Fore.GREEN}[✓] {msg}{Style.RESET_ALL}")
        if self.log_file:
            logging.info(msg)
    
    def error(self, msg):
        print(f"{Fore.RED}[✗] {msg}{Style.RESET_ALL}")
        if self.log_file:
            logging.error(msg)
    
    def warning(self, msg):
        print(f"{Fore.YELLOW}[⚠] {msg}{Style.RESET_ALL}")
        if self.log_file:
            logging.warning(msg)
    
    def success(self, msg):
        print(f"{Fore.CYAN}[+] {msg}{Style.RESET_ALL}")
        if self.log_file:
            logging.info(f"SUCCESS: {msg}")
    
    def chaos(self, msg):
        print(f"{Fore.MAGENTA}[🔥] {msg}{Style.RESET_ALL}")
        if self.log_file:
            logging.info(f"CHAOS: {msg}")

def format_phone(phone):
    """Format nomor HP ke internasional"""
    phone = re.sub(r'[^0-9+]', '', phone)
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    elif not phone.startswith('62') and not phone.startswith('+'):
        phone = '62' + phone
    if phone.startswith('+'):
        phone = phone[1:]
    return phone

def random_delay(min_sec=0.1, max_sec=0.5):
    """Random delay buat hindari detection"""
    time.sleep(random.uniform(min_sec, max_sec))

def generate_otp_code():
    """Generate random OTP code"""
    return str(random.randint(1000, 9999))

def load_json(file_path):
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return None

def save_json(file_path, data):
    """Save ke JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def banner():
    """Tampilkan banner keren"""
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════╗
{Fore.RED}║      {Fore.YELLOW}CHAOS TOOLKIT - KAISAR KING'S⚡️{Fore.RED}        ║
{Fore.RED}║      {Fore.CYAN}Power by MonzapThorenFore.RED}               ║
{Fore.RED}╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)