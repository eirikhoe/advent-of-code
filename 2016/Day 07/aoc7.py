from pathlib import Path

data_folder = Path(".").resolve()

def has_tls_support(ip):
    hypernet = 0
    tls = False
    for i in range(len(ip)-3):
        if ip[i] == '[':
            hypernet += 1
        elif ip[i] == ']':
            hypernet -= 1
        else: 
            tls_crit = ((ip[i]==ip[i+3]) and (ip[i+1]==ip[i+2])) and (ip[i]!=ip[i+1])
            if tls_crit and hypernet:
                return False
            elif tls_crit:
                tls = True
    return tls

def has_ssl_support(ip):
    hypernet = 0
    abas = set()
    babs = set()
    for i in range(len(ip)-2):
        if ip[i] == '[':
            hypernet += 1
        elif ip[i] == ']':
            hypernet -= 1
        else:
            crit = (ip[i]==ip[i+2]) and (ip[i]!=ip[i+1]) 
            if crit and hypernet:
                babs.add(ip[i+1]+ip[i])
            elif crit:
                abas.add(ip[i]+ip[i+1])
    return not abas.isdisjoint(babs)


def count_ips(ips,ip_type='tls'):
    if ip_type == 'tls':
        ip_checker = has_tls_support
    else:
        ip_checker = has_ssl_support
    n_ips = 0
    for ip in ips:
        n_ips += ip_checker(ip)
    return n_ips 

def main():
    data = data_folder.joinpath("input.txt").read_text()
    ips = data.split('\n')

    print("Part 1")
    print(f"{count_ips(ips,'tls')} IPs has TLS support")
    print()

    print("Part 2")
    print(f"{count_ips(ips,'ssl')} IPs has SSL support")

    
if __name__ == "__main__":
    main()
