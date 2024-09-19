#!/usr/bin/env python
#

import requests
import sys

timeout = 3
verbose = True
version = "1.0.2"
banner = """
             _             
            (_)            
  __ _ _ __  _ _ __   __ _ 
 / _` | '_ \| | '_ \ / _` |
| (_| | |_) | | | | | (_| |
 \__, | .__/|_|_| |_|\__, |
    | | |             __/ |
    |_|_|            |___/ 

                      by TamilBotNet
                      version: {}
      Updated by Crazy Danish Hacker,abu
""".format(version, sys.argv[0])

usage = "\n [SYNTAX]  python {} target.txt"

# Check if any args have been set.
if len(sys.argv) <= 1:
    print(banner)
    print(usage)
    exit(1)

# Set the output filename to be used globally
filename = "OnlineDomains_{}".format(sys.argv[1])
# some site return 403 instead of 200 when request without user agent.
header = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30'}


def create_file(user_file):
    with open(user_file, "w") as output_file:
        output_file.close()


def main():
    print(banner)
    global filename  # This could be an arg to main() if we wanted to.
    with open(sys.argv[1], "r") as input_file:
        create_file(filename)

        for line in input_file:
            # Note: Strip only works at the beginning or end of a string.
            url = "https://{}".format(line.strip())
            try:
                req = requests.get(url, timeout=timeout, headers=header)
                if req.status_code == 200:
                    extra = "- HTTP 200 OK" if verbose else ""
                    print("[+] Domain is online! ({}) {}".format(url, extra))
                    with open(filename, "a") as output_file:
                        output_file.write("{}\n".format(
                            line.strip()))  # Change here
                        output_file.close()
                else:
                    extra = "HTTP {}".format(
                        req.status_code) if verbose else ""
                    print(
                        "[-] Domain did not return 200 OK! ({}) {}".format(url, extra))
            except KeyboardInterrupt:
                exit()
            except requests.exceptions.Timeout:
                print("[-] Domain timed out! ({})".format(url))
            except requests.exceptions.ConnectionError:
                print("[-] Domain may not exist! ({})".format(url))
            except requests.exceptions.TooManyRedirects:
                print("[-] Domain has too many redirects! ({})".format(url))


if __name__ == "__main__":
    main()
