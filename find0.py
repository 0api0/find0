import os
import subprocess
import signal
import sys
import requests
import argparse
 
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

def main(args):
    domain = args.domain
    if not os.path.exists(domain):
        os.makedirs(domain)
    print(f"{YELLOW}Finding subdomains using assetfinder...{ENDC}")
    subdomains = set()
    with open(f"{domain}/all_subdomains.txt", "w") as f:
        assetfinder_output = subprocess.run(['assetfinder','-subs-only', f'{domain}'], capture_output=True, text=True)
        for subdomain in assetfinder_output.stdout.split('\n'):
            if subdomain and subdomain not in subdomains:
                subdomains.add(subdomain)
                f.write(subdomain + '\n')
    print(f"{GREEN}Found {len(subdomains)} unique subdomains{ENDC}")

    print(f"{YELLOW}Probing for live subdomains using httprobe...{ENDC}")
    live_subdomains = set()
    with open(f"{domain}/live_subdomains.txt", "w") as f:
        httprobe_output = subprocess.run(['httprobe'], input='\n'.join(subdomains), capture_output=True, text=True)
        for subdomain in httprobe_output.stdout.split('\n'):
            if subdomain and subdomain not in live_subdomains:
                # Check if URL status code is between 200 and 299
                try:
                    response = requests.get(subdomain.strip(), timeout=10)
                    if response.status_code >= 200 and response.status_code < 300:
                        live_subdomains.add(subdomain)
                        f.write(subdomain + '\n')
                except:
                    pass
    print(f"{GREEN}Found {len(live_subdomains)} live subdomains{ENDC}")

    print(f"{YELLOW}Extracting parameters using waybackurls...{ENDC}")
    with open(f"{domain}/parameters.txt", "w") as f:
        for subdomain in live_subdomains:
            wayback_output = subprocess.run(['waybackurls', subdomain], capture_output=True, text=True)
            for url in wayback_output.stdout.split('\n'):
                f.write(url + '\n')    
    print(f"{GREEN}Finished extracting parameters{ENDC}")

if __name__ == "__main__":
    try:
        name_block = """
    ##############################################################
    #            Find0 parametrs from domain                     #
    #                                                            #
    #                 Created by 0api0                           #
    #                       April 2023                           #
    ##############################################################
    A folder named domain will be placed containing what has been extracted
    """
        print(name_block)
        parser = argparse.ArgumentParser()
        parser.add_argument("domain", help="Domain to scan")
        args = parser.parse_args()
        main(args)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan aborted by user{ENDC}")
        sys.exit(0)
