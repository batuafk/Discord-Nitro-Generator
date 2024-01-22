from torswitch import TorProtocol
import threading
import requests
import psutil
import string
import random
import time
import sys
import os

speed = int(input("Speed (10 = slow, 100 = fast): "))

api = "https://discordapp.com/api/v9/entitlements/gift-codes/"
api2 = "?with_application=false&with_subscription_plan=true"
gift = "https://discord.com/gifts/"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def set_title(title):
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()


def check_process_exists(process_name):
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == process_name:
            return True
    return False


def terminate_process(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            pid = process.info['pid']
            try:
                p = psutil.Process(pid)
                p.terminate()
            except psutil.NoSuchProcess:
                pass


def format_duration(seconds):
    years, seconds = divmod(seconds, 31536000)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    result = ""
    if years:
        result += f"{int(years)}y "
    if days:
        result += f"{int(days)}d "
    if hours:
        result += f"{int(hours)}h "
    if minutes:
        result += f"{int(minutes)}m "
    if seconds:
        result += f"{int(seconds)}s"

    return result


def tor_rotation():
    global ip_change_count, tor_ip
    while True:
        tor.AbsoluteNewTorIp()
        ip_change_count += 1


def update_title():
    start_time = time.time()
    while True:
        time.sleep(1)
        duration = time.time() - start_time
        set_title(format_duration(duration))


def check_code():
    global error_count, invalid_count, valid_count

    code = "".join(random.choice(chars) for _ in range(16))
    url = api + code + api2
    time.sleep(random.randrange(0, 10))
    self_error = 0

    while True:
        if self_error > 0:
            time.sleep(1)
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.get(url, proxies=proxies, headers=headers, timeout=10)
            if response.status_code == 200:
                nitro = gift + code
                try:
                    print(f"\033[32m{nitro} {tor_ip} | IP Change: {ip_change_count} Error: {error_count} Invalid: {invalid_count} Valid: {valid_count}\033[0m\033[0m")
                    valid_count += 1
                    try:
                        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                        file_path = os.path.join(desktop_path, "valid_codes.txt")
                        with open(file_path, "a") as file:
                            file.write(nitro + "\n")
                        os.startfile(file_path)
                    except:
                        with open("valid_codes.txt", "a") as file:
                            file.write(nitro + "\n")
                        os.system("start valid_codes.txt")
                    return True
                except Exception as e:
                    print(f"\033[32m{nitro} {tor_ip} Error: {e}\033[0m")
            elif response.status_code == 429:
                nitro = gift + code
                print(f"\033[31m{nitro} {tor_ip} {response.status_code} | IP Change: {ip_change_count} Error: {error_count} Invalid: {invalid_count} Valid: {valid_count}\033[0m\033[0m")
                error_count += 1
                self_error += 1
            else:
                nitro = gift + code
                print(f"\033[31m{nitro} {tor_ip} {response.status_code} | IP Change: {ip_change_count} Error: {error_count} Invalid: {invalid_count} Valid: {valid_count}\033[0m")
                invalid_count += 1
                if self_error > 0:
                    error_count = error_count - self_error
                return False
        except:
            nitro = gift + code
            print(f"\033[31m{nitro} {tor_ip} 000\033[0m")
            error_count += 1
            self_error += 1


if __name__ == '__main__':
    set_title("NitroGen")
    clear()

    if check_process_exists("tor.exe") is True:
        terminate_process("tor.exe")
        print("tor.exe terminated")

    if os.name != "nt":
        try:
            os.popen("sudo service tor stop")
            print("Service tor stopped")
        except:
            pass

    if os.path.exists("user_agents.txt"):
        with open("user_agents.txt", "r") as file:
            user_agents = [line.strip('\n') for line in file.readlines()]
        print(f"Loaded {len(user_agents)} user agents")
    else:
        print("Error: user_agents.txt not found")
        input()
        sys.exit()

    proxies = {
        'http': "socks5://127.0.0.1:9050",
        'https': "socks5://127.0.0.1:9050"
    }

    tor = TorProtocol()
    tor.Stop()
    tor.Start()
    tor_ip = tor.AbsoluteNewTorIp()

    ip_change_count = 1
    error_count = 0
    invalid_count = 0
    valid_count = 0

    thread = threading.Thread(target=tor_rotation)
    thread.daemon = True
    thread.start()

    thread = threading.Thread(target=update_title)
    thread.daemon = True
    thread.start()

    chars = string.ascii_letters + string.digits

    print('')
    while True:
        threads = []

        for _ in range(speed):
            thread = threading.Thread(target=check_code)
            thread.daemon = True
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
