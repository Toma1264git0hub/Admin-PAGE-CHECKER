import requests
import threading

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

def logo():
    print(f"""{YELLOW}
                                              _.oo.
                      _.u[[/;:,.         .odMMMMMM'
                   .o888UU[[[/;:-.  .o@P^    MMM^
                  oN88888UU[[[/;::-.        dP^
                 dNMMNN888UU[[[/;:--.   .o@P^
               ,MMMMMMN888UU[[/;::-. o@^
                NNMMMNN888UU[[[/~.o@P^
                888888888UU[[[/o@^-..
               oI8888UU[[[/o@P^:--..
            .@^  YUU[[[/o@^;::---..
          oMP     ^/o@P^;:::---..
       .dMMM    .o@^ ^;::---...
      dMMMMMMM@^`       `^^^^
     YMMMUP^
      ^^

••••••••••••••••••••••••••••••••••••••••••••••••••
{CYAN}TELEGRAM:@K_DKP
GITHUB:@toma1264git0hub
TIKTOK:@.HTML.1{YELLOW}
••••••••••••••••••••••••••••••••••••••••••••••••••
{RESET}""")


def send_to_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(RED + "[ERROR] Failed to send message: " + str(e) + RESET)


def check_path(full_url, token, chat_id):
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code in [200, 301, 302, 403]:
            found_msg = f"[FOUND] {full_url} (Status: {response.status_code})"
            print(GREEN + found_msg + RESET)
            send_to_telegram(token, chat_id, found_msg)
        else:
            print(YELLOW + f"[CHECK] {full_url} (Status: {response.status_code})" + RESET)
    except requests.RequestException:
        print(RED + f"[ERROR] Failed to connect to {full_url}" + RESET)


def start_scan(base_url, token, chat_id, num_threads):
    try:
        with open("admin_paths_TOMAS.txt", "r", encoding="utf-8") as file:
            paths = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(RED + "[ERROR] File 'admin_paths_TOMAS.txt' not found." + RESET)
        return

    print(BLUE + f"[INFO] Scanning started on {base_url} ..." + RESET)

    def worker(path):
        full_url = base_url + path
        check_path(full_url, token, chat_id)

    threads = []
    for path in paths:
        while threading.active_count() > num_threads:
            pass
        t = threading.Thread(target=worker, args=(path,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(BLUE + "[DONE] Scan finished." + RESET)


if __name__ == "__main__":
    logo()

    print(f"""{CYAN}
[ TOOL NAME ]: Admin Panel Scanner by @K_DKP

[ DESCRIPTION ]:
This tool scans websites for hidden admin panels and sends results to your Telegram account.

[ HOW TO USE ]:
1_ Telegram Token Bot Intervention  
2_ To intervene ID Telegram account  
3_ Enter the number of threads  
4_ Enter the website link without / at the end  
[+]Note: You must use VPN
{RESET}""")

    print(GREEN + "Enter your Telegram bot token:" + RESET)
    token = input("@K_DKP•>> ")

    print(GREEN + "Enter your Telegram chat ID:" + RESET)
    chat_id = input("@K_DKP•>> ")

    print(GREEN + "Enter the base URL (e.g. https://example.com):" + RESET)
    base_url = input("@K_DKP•>> ")

    print(GREEN + "Enter number of threads (e.g. 20):" + RESET)
    try:
        threads_count = int(input("@K_DKP•>> "))
    except ValueError:
        threads_count = 10
        print(YELLOW + "[WARNING] Invalid input. Defaulting to 10 threads." + RESET)

    start_scan(base_url, token, chat_id, threads_count)