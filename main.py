import messagebox
import threading
import requests
import random
import string
import psutil
import socket
import socks
import time
import os

banner = """
 _   _ _ _              ____         __     _____  
| \ | (_) |_ _ __ ___  / ___| ___ _ _\ \   / / _ \ 
|  \| | | __| '__/ _ \| |  _ / _ \ '_ \ \ / / (_) |
| |\  | | |_| | | (_) | |_| |  __/ | | \ V / \__, |
|_| \_|_|\__|_|  \___/ \____|\___|_| |_|\_/    /_/ 
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_title(title):
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

def wait_internet_connection():
    print("Waiting for an internet connection...")
    while True:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=20)
            print("Internet connection established.")
            return True
        except:
            time.sleep(20)

class tor:
    def configure():
        try:
            path = "tor\\torrc"
            ports = range(9000, 10000)

            with open(path, "w") as torrc_file:
                for port in ports:
                    line = f"SocksPort {port}\n"
                    torrc_file.write(line)
            return True
        except Exception as e:
            return e

    def restart():
        if is_process_running("tor.exe"):
            terminate_process("tor.exe")
            
        os.system("start tor\\tor.exe -f tor\\torrc")
        time.sleep(5)

    def stop():
        os.system("taskkill /F /IM tor.exe")

def is_process_running(process_name):
    for process in psutil.process_iter(["pid", "name"]):
        if process.info["name"] == process_name:
            return True
    return False

def terminate_process(process_name):
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if process.info["name"] == process_name:
            pid = process.info["pid"]
            try:
                p = psutil.Process(pid)
                p.terminate()
            except psutil.NoSuchProcess:
                pass

def get_user_agents():
    with open("user-agents.txt", "r") as file:
        user_agents = file.readlines()
    return [agent.strip() for agent in user_agents]

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def check_code(code, proxy, user_agent):
    global valid_codes, invalid_codes

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(proxy.split(":")[1]))
    socket.socket = socks.socksocket
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        message = response.json()["message"]
        if response.status_code == 200:
            valid_codes += 1
            print(f"\033[32m[{formatted_time}] {code} | {proxy} | Valid: {valid_codes} Invalid: {invalid_codes} | {message}\033[0m")
            save_valid_code(code)
            msgbox = messagebox.askyesno(title="NitroGenV9 - Valid Code", message=f"Claim? {code}")
            if msgbox is True:
                os.system(f"start https://discord.com/gifts/{code}")
        else:
            invalid_codes += 1
            print(f"\033[94m[{formatted_time}] {code} | {proxy} | Valid: {valid_codes} Invalid: {invalid_codes} | {message}\033[0m")
    except Exception as e:
        print(f"\033[94m[{formatted_time}] {code} | {proxy} | Valid: {valid_codes} Invalid: {invalid_codes} | Connection error\033[0m")
        print(e)
        time.sleep(5)

        proxy = random.choice(proxies)
        user_agent = random.choice(user_agents)
        check_code(code, proxy, user_agent)

def save_valid_code(code):
    with open("valid_codes.txt", "a") as file:
        file.write(f"https://discord.com/gifts/{code}\n")

def main():
    global proxies, user_agents, start_time
    proxies = [f"127.0.0.1:{port}" for port in range(9000, 10000)]
    user_agents = get_user_agents()

    tor.configure()
    tor.restart()

    start_time = time.time()
    try:
        while True:
            for proxy in proxies:
                code = generate_code()
                user_agent = random.choice(user_agents)
                thread = threading.Thread(target=check_code, args=(code, proxy, user_agent))
                thread.daemon = True
                thread.start()
                time.sleep(0.4)

            tor.restart()
    except KeyboardInterrupt:
        tor.stop()

if __name__ == "__main__":
    valid_codes = 0
    invalid_codes = 0

    clear()
    print(banner)
    set_title("DNGv9 by Bt08s")

    main()
