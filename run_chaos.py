import os
import sys
import time
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════════╗
{Fore.RED}║                                                       ║
{Fore.RED}║      {Fore.YELLOW}🔥 CHAOS TOOLKIT - KAISAR KING'S ⚡️{Fore.RED}      ║
{Fore.RED}║      {Fore.CYAN}Power by KaisarAi BETA{Fore.RED}                  ║
{Fore.RED}║      {Fore.GREEN}Version: 3.0 - Unfiltered{Fore.RED}             ║
{Fore.RED}║                                                       ║
{Fore.RED}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

def show_menu():
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════╗
{Fore.CYAN}║                   📋 MAIN MENU                       ║
{Fore.CYAN}╠═══════════════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.GREEN}1.{Fore.YELLOW} OTP Spammer Massal              {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}2.{Fore.YELLOW} WhatsApp Report Flood          {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}3.{Fore.YELLOW} Target Manager                 {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}4.{Fore.YELLOW} Proxy Manager                  {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}5.{Fore.YELLOW} View Logs                     {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}6.{Fore.YELLOW} Run All (Chaos Mode)          {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}7.{Fore.RED} Exit                            {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

def main():
    while True:
        clear_screen()
        banner()
        show_menu()
        
        choice = input(f"{Fore.CYAN}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == '1':
            os.system("python otp_spammer_massal.py")
        elif choice == '2':
            os.system("python wa_report_pro.py")
        elif choice == '3':
            os.system("python target.py")
        elif choice == '4':
            os.system("python proxy_manager.py")
        elif choice == '5':
            os.system("ls -la logs/")
            input("Press Enter to continue...")
        elif choice == '6':
            print(f"{Fore.RED}[🔥] CHAOS MODE AKTIF!{Style.RESET_ALL}")
            os.system("python otp_spammer_massal.py")
            os.system("python wa_report_pro.py")
            os.system("python target.py")
        elif choice == '7':
            print(f"{Fore.RED}[💀] Bye bye Bos!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[❌] Pilihan gak valid!{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()