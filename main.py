import requests
import json
import random

import os
import threading
from colorama import Fore
from colorama import init
from time import sleep

init(convert=True)


vaild_tokens = []
ratelimited_tokens = []

def generate_random_number_string(length=6):
    number_string = ''.join(random.choices('0123456789', k=length))
    return number_string


session = requests.Session()
session.trust_env = False
proxylist=[]
def proxies():
    r = requests.get("https://api.proxyscrape.com?request=getproxies&proxytype=http")
    rformat = r.text.strip()
    rformat = rformat.replace("\r","")
    rlist = list(rformat.split("\n"))
    with open("proxies.txt", "w") as x:
        for proxy in rlist:
            proxylist.append(proxy)


def check(token):
    proxy=random.choice(proxylist)

    r=session.get('https://discord.com/api/v9/users/@me',headers={"Authorization": token},proxies={    'http': proxy    })
    if r.status_code == 200:
        print(f"{Fore.GREEN}[Success]{Fore.RESET} Connected to token: {Fore.CYAN}{token}{Fore.RESET}")
        vaild_tokens.append(token)
        return True
    elif r.status_code == 429:
        print(f"{Fore.YELLOW}  Rate Limited {Fore.YELLOW}[{Fore.RESET}429{Fore.YELLOW}] {Fore.CYAN}| {Fore.RESET}{token}")
    else:
        print(f"{Fore.RED}[Dead]{Fore.RESET} Dead token: {Fore.CYAN}{token}{Fore.RESET}")
        return False
        


def print_results(botName, botToken, inviteUrl):
    print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} Bot Name: {Fore.CYAN}{botName}{Fore.RESET} & Bot Token: {Fore.CYAN}{botToken}{Fore.RESET} Invite URL: {Fore.CYAN}{inviteUrl}{Fore.RESET}")

    with open('results.txt', 'a') as file:
        file.write(f"================================================\nBot Name: {botName}\nBot Token: {botToken}\nInvite URL: {inviteUrl}\n================================================\n")


def generate_invite(botID):
    url = f"https://discord.com/api/oauth2/authorize?client_id={botID}&permissions=8&scope=bot+applications.commands"
    return url

def reset_bot_token(botID, authorToken):
    url = f'https://discord.com/api/v9/applications/{botID}/bot/reset'

    headers = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': authorToken,
        'content-length': '0',
        'cookie': '__dcfduid=a4504bd0ba8011ee82863b54be4175db; __sdcfduid=a4504bd1ba8011ee82863b54be4175db0e46b0b6a97ede84b6bd024500fad1f532144ecdf0169c0b3404348ae7a29b87; _gcl_au=1.1.1054920407.1706162655; _ga=GA1.1.981724761.1706162655; __stripe_mid=6a5e2bf5-32fb-4717-968c-830d4b6f9eae63b8f3; cf_clearance=wN.BzqGN4KtmJRyOhLCZzSwmGUKSA6GISlqpnZPyq4M-1706609646-1-AdrWHl4Mxwit+vDJNUD1H91xzMU1eb9KWbc9a9jX6yvNp7N8q/4YUL2z8fpuaHkSaG2CPKswVyC/sQWxR0iL3dg=; __cfruid=9bda13c69bb87ea9c6815ffc6a6068e25c987f16-1706706202; _cfuvid=l5dBsi5YU8KbtTTKl89S8lOaBiSLuc0LXij6Gm2IoQ4-1706706202836-0-604800000; locale=en-US; OptanonConsent=isIABGlobal=false&datestamp=Wed+Jan+31+2024+16%3A03%3A30+GMT%2B0300+(GMT%2B03%00)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; _ga_Q149DFWHT7=GS1.1.1706706211.3.0.1706706211.0.0.0',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/developers/applications/1202245404364918835/bot',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-track': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLz9kaXNjb3JkdG9rZW49TVRFNU9UWXlOalkxTkRRek5qSTVPRGMxTWcuR2l4eE40LkV1dzIwRmQ2cGRob0Q4VGg0U1hsaGw0cEphRUFWY0JrREcwZFhnIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
    }

    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data['token']

def create_bot(token):
    url = "https://discord.com/api/v9/applications"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "MTE5OTYyNjY1NDQzNjI5ODc1Mg.GixxN4.Euw20Fd6pdhoD8Th4SXlhl4pJaEAVcBkDG0dXg",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-track": "Your x-track header here",
    }
    data = {"name": f"Hyber Bot {generate_random_number_string()}", "team_id": None}

    r = requests.post(url, headers=headers, data=json.dumps(data))
    if r.status_code == 200 or r.status_code == 201:
        data = r.json()
        
        bot_id = data['id']
        bot_name = data['name']
        bot_token = reset_bot_token(bot_id, token)
        invite_url = generate_invite(bot_id)

        print_results(bot_name, bot_token, invite_url)
        return "done"

    elif r.status_code == 429:
        print(f"{Fore.YELLOW}  Rate Limited {Fore.YELLOW}[{Fore.RESET}429{Fore.YELLOW}] {Fore.CYAN}| {Fore.RESET}{token}")
        return "ratelimited"
    else:
        print(f"{Fore.RED}[Dead]{Fore.RESET} Dead token: {Fore.CYAN}{token}{Fore.RESET}")
        print(r.status_code)
        return "cancel"


proxies()

with open("tokens.txt", "r") as file:
    print(f"{Fore.BLACK}[INFO]{Fore.RESET} Started {Fore.CYAN}tokens.txt{Fore.RESET} file")

    for line in file:
        line = line.strip()
        check(line)
    
    print(f"{Fore.BLUE}[INFO]{Fore.RESET} Finished {Fore.CYAN}tokens.txt{Fore.RESET} file")

    if len(vaild_tokens) <= 0:
        print(f"{Fore.RED}[EXIT]{Fore.RESET} There is no valid tokens inside {Fore.CYAN}tokens.txt{Fore.RESET} file.")
        exit(1)
    else:
        print(f"{Fore.BLUE}[INFO]{Fore.RESET} Found {Fore.GREEN}{len(vaild_tokens)}{Fore.RESET} vaild tokens inside {Fore.CYAN}tokens.txt{Fore.RESET} file")




while vaild_tokens:
    token = vaild_tokens.pop(0)
    status = create_bot(token)

    if status == 'ratelimited':
        print(f"{Fore.RED}[RATELIMITED]{Fore.RED} Token: {Fore.CYAN}{token}{Fore.RESET} is being ratelimited.")
        ratelimited_tokens.append(token)
    elif status == 'cancel':
        print(f"{Fore.RED}[CANCEL]{Fore.RESET} Token {Fore.CYAN}{token}{Fore.RESET} is being in the {Fore.RED}CANCEL{Fore.RESET} state")
    elif status == 'done':
        print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} Token: {Fore.CYAN}{token}{Fore.RESET} has been used successfually")
        vaild_tokens.append(token)
    
    sleep(1)


while ratelimited_tokens:
    sleep(180)  # Wait for 3 minutes before retrying rate-limited tokens
    token = ratelimited_tokens.pop(0)  # Get the first rate-limited token
    print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} Retrying token {Fore.CYAN}{token}{Fore.RESET} after rate limit.")
    status = create_bot(token)

    if status != 'ratelimited':  # If it's no longer rate-limited, remove it from the list
        if status == 'done':
            print(f"Token {token} is done. Will reuse the same token.")
            ratelimited_tokens.insert(0, token)  # Re-insert at the beginning to retry
        elif status == 'cancel':
            print(f"Token {token} is cancelled. Will not retry.")