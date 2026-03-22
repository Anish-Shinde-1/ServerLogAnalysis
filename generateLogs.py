import random
from datetime import datetime, timedelta

OUTPUT_FILE = "server.log"
TOTAL_REQUESTS = 1000000   # change to 1_000_000 for very large logs

normal_ips = [
"192.168.1.10","192.168.1.11","192.168.1.12","192.168.1.13","192.168.1.14",
"192.168.1.15","192.168.1.16","192.168.1.17","192.168.1.18","192.168.1.19",

"10.0.0.5","10.0.0.6","10.0.0.7","10.0.0.8","10.0.0.9",

"172.16.0.2","172.16.0.3","172.16.0.4","172.16.0.5","172.16.0.6",

"34.120.45.23","52.14.92.11","18.203.55.90","3.87.211.10","44.201.32.8"
]

attacker_ips = [
"185.220.101.1",
"185.220.101.2",
"45.33.32.156",
"91.134.182.92",
"103.251.167.20",
"46.101.12.34"
]

bot_ips = [
"66.249.66.1",
"66.249.66.2",
"157.55.39.1",
"207.46.13.5"
]

# Endpoints
pages = [
"/",
"/home",
"/products",
"/products/laptop",
"/products/phone",
"/cart",
"/checkout",
"/login",
"/register",
"/profile",
"/search?q=keyboard"
]

api_routes = [
"/api/login",
"/api/products",
"/api/cart",
"/api/search",
"/api/orders"
]

static_files = [
"/static/app.js",
"/static/vendor.js",
"/static/style.css",
"/static/logo.png",
"/static/banner.jpg",
"/static/fonts.woff",
"/favicon.ico"
]

admin_targets = [
"/admin",
"/admin/login",
"/admin/config",
"/phpmyadmin",
"/wp-admin",
"/.env",
"/config.php",
"/backup.zip",
"/db.sql"
]

# HTTP methods
methods = (
["GET"] * 85 +
["POST"] * 10 +
["PUT"] * 3 +
["DELETE"] * 2
)

# Status distribution
status_codes = (
[200] * 85 +
[301] * 5 +
[302] * 4 +
[400] * 2 +
[401] * 1 +
[403] * 1 +
[404] * 1 +
[500] * 1
)

# User agents
agents = [

# Windows Chrome
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0 Safari/537.36",

# Mac Safari
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 Version/16.0 Safari/605.1.15",

# Linux Firefox
"Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",

# iPhone
"Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",

# Android Chrome
"Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36",

# CLI tools
"curl/7.68.0",
"python-requests/2.31.0",
"Wget/1.21.1",

# Bots
"Googlebot/2.1 (+http://www.google.com/bot.html)",
"Bingbot/2.0 (+http://www.bing.com/bingbot.htm)"
]

referrers = [
"-",
"https://google.com",
"https://google.com/search?q=laptop",
"https://google.com/search?q=python+logs",
"https://bing.com",
"https://duckduckgo.com",
"https://twitter.com",
"https://facebook.com",
"https://linkedin.com",
"https://news.ycombinator.com",
"https://reddit.com"
]

# ---------------- timestamp generator ----------------

def generate_timestamp(current_time):

    hour = current_time.hour

    # daily traffic pattern
    if 0 <= hour <= 6:
        rate = 2
    elif 7 <= hour <= 11:
        rate = 5
    elif 12 <= hour <= 18:
        rate = 12
    else:
        rate = 6

    r = random.random()

    # normal traffic
    if r < 0.85:
        gap = random.expovariate(rate)

    # burst traffic
    elif r < 0.97:
        gap = random.expovariate(rate * 4)

    # quiet gap
    else:
        gap = random.uniform(2, 8)

    current_time += timedelta(seconds=gap)

    timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S +0000")

    return current_time, timestamp


# ---------------- traffic generators ----------------

def generate_normal_request():

    ip = random.choice(normal_ips)

    method = random.choice(methods)

    endpoint = random.choice(
        pages + pages + static_files + static_files + api_routes
    )

    status = random.choice(status_codes)

    size = random.randint(200,8000)

    agent = random.choice(agents)

    ref = random.choice(referrers)

    return ip,method,endpoint,status,size,agent,ref


def generate_bot_request():

    ip = random.choice(bot_ips)

    method = "GET"

    endpoint = random.choice(
        pages + static_files + pages + static_files
    )

    status = random.choice([200,200,200,301])

    size = random.randint(200,7000)

    agent = random.choice([
        "Googlebot/2.1 (+http://www.google.com/bot.html)",
        "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)"
    ])

    ref = "-"

    return ip,method,endpoint,status,size,agent,ref


def generate_attack_request():

    ip = random.choice(attacker_ips)

    method = random.choice(["GET","POST"])

    endpoint = random.choice(admin_targets + admin_targets)

    status = random.choice([401,403,404])

    size = random.randint(100,1200)

    agent = random.choice([
        "curl/7.68.0",
        "python-requests/2.31.0"
    ])

    ref = "-"

    return ip,method,endpoint,status,size,agent,ref


def generate_bruteforce():

    ip = random.choice(attacker_ips)

    method = "POST"

    endpoint = "/login"

    status = random.choice([401,401,401,200])

    size = random.randint(300,900)

    agent = "python-requests/2.31.0"

    ref = "-"

    return ip,method,endpoint,status,size,agent,ref


# ---------------- main generator ----------------

def main():

    current_time = datetime.now()

    with open(OUTPUT_FILE,"w") as f:

        i = 0

        while i < TOTAL_REQUESTS:

            # occasional attack spike
            if random.random() < 0.002:

                spike = random.randint(20,80)

                for _ in range(spike):

                    current_time, timestamp = generate_timestamp(current_time)

                    ip,method,endpoint,status,size,agent,ref = generate_attack_request()

                    log = f'{ip} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status} {size} "{ref}" "{agent}"\n'

                    f.write(log)

                    i += 1

                    if i >= TOTAL_REQUESTS:
                        break

                continue


            r = random.random()

            if r < 0.90:
                req = generate_normal_request()

            elif r < 0.95:
                req = generate_bot_request()

            elif r < 0.985:
                req = generate_attack_request()

            else:
                req = generate_bruteforce()


            ip,method,endpoint,status,size,agent,ref = req

            current_time, timestamp = generate_timestamp(current_time)

            log = f'{ip} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status} {size} "{ref}" "{agent}"\n'

            f.write(log)

            i += 1


    print(f"Generated {TOTAL_REQUESTS} log entries → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()