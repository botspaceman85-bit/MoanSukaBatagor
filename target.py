import random
import re
import json
import os
from datetime import datetime

class TargetManager:
    def __init__(self):
        self.targets = []
        self.load_targets()
    
    def load_targets(self):
        """Load target dari file JSON"""
        if os.path.exists('targets.json'):
            with open('targets.json', 'r') as f:
                self.targets = json.load(f)
        else:
            # Default target list
            self.targets = [
                "628123456789",
                "628987654321",
                "628111222333"
            ]
            self.save_targets()
    
    def save_targets(self):
        """Simpan target ke file JSON"""
        with open('targets.json', 'w') as f:
            json.dump(self.targets, f, indent=4)
    
    def add_target(self, phone):
        """Tambah target baru"""
        phone = self.format_phone(phone)
        if phone not in self.targets:
            self.targets.append(phone)
            self.save_targets()
            print(f"[✅] Target {phone} berhasil ditambahkan!")
            return True
        else:
            print(f"[⚠️] Target {phone} sudah ada!")
            return False
    
    def remove_target(self, phone):
        """Hapus target"""
        phone = self.format_phone(phone)
        if phone in self.targets:
            self.targets.remove(phone)
            self.save_targets()
            print(f"[🗑️] Target {phone} berhasil dihapus!")
            return True
        else:
            print(f"[❌] Target {phone} tidak ditemukan!")
            return False
    
    def format_phone(self, phone):
        """Format nomor HP ke format internasional"""
        phone = re.sub(r'[^0-9+]', '', phone)
        if phone.startswith('0'):
            phone = '62' + phone[1:]
        elif not phone.startswith('62') and not phone.startswith('+'):
            phone = '62' + phone
        if phone.startswith('+'):
            phone = phone[1:]
        return phone
    
    def get_random_target(self):
        """Ambil target random"""
        if self.targets:
            return random.choice(self.targets)
        return None
    
    def get_all_targets(self):
        """Ambil semua target"""
        return self.targets.copy()
    
    def generate_targets(self, count=50):
        """Generate target dummy buat testing"""
        prefixes = ['62812', '62813', '62815', '62817', '62818', '62819', '62821', '62822']
        new_targets = []
        for _ in range(count):
            prefix = random.choice(prefixes)
            suffix = ''.join([str(random.randint(0,9)) for _ in range(8)])
            phone = prefix + suffix
            if phone not in self.targets and phone not in new_targets:
                new_targets.append(phone)
        
        self.targets.extend(new_targets)
        self.save_targets()
        print(f"[🎯] Berhasil generate {len(new_targets)} target baru!")
        return new_targets
    
    def clear_targets(self):
        """Kosongkan semua target"""
        self.targets = []
        self.save_targets()
        print("[🧹] Semua target berhasil dibersihkan!")
    
    def show_targets(self):
        """Tampilkan semua target"""
        if not self.targets:
            print("[📭] Belum ada target!")
            return
        
        print(f"\n📱 DAFTAR TARGET ({len(self.targets)}):")
        print("=" * 40)
        for i, target in enumerate(self.targets, 1):
            print(f"{i}. {target}")
        print("=" * 40)

# ============ MAIN BUAT TESTING ============
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║   TARGET MANAGER - CHAOS EDITION     ║
    ╚═══════════════════════════════════════╝
    """)
    
    manager = TargetManager()
    
    while True:
        print("\n📋 MENU TARGET:")
        print("1. Lihat semua target")
        print("2. Tambah target")
        print("3. Hapus target")
        print("4. Generate target random")
        print("5. Bersihkan semua target")
        print("6. Ambil target random")
        print("7. Keluar")
        
        choice = input("\nPilih menu: ")
        
        if choice == '1':
            manager.show_targets()
        elif choice == '2':
            phone = input("Masukkan nomor target (62xxx): ")
            manager.add_target(phone)
        elif choice == '3':
            phone = input("Masukkan nomor target yang mau dihapus: ")
            manager.remove_target(phone)
        elif choice == '4':
            count = int(input("Jumlah target yang digenerate (default 50): ") or "50")
            manager.generate_targets(count)
        elif choice == '5':
            confirm = input("Yakin mau bersihin semua target? (y/n): ")
            if confirm.lower() == 'y':
                manager.clear_targets()
        elif choice == '6':
            target = manager.get_random_target()
            if target:
                print(f"[🎯] Target random: {target}")
            else:
                print("[❌] Belum ada target!")
        elif choice == '7':
            print("[👋] Bye bye! Gas chaos!")
            break
        else:
            print("[❌] Pilihan gak valid!")