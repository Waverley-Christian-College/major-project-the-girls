import requests

# --- Bright Data Proxy Gateway Config ---
PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = "port"
PROXY_USER = "user_name"
PROXY_PASS = "password"

# --- Build proxy URL ---
proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {"http": proxy_url, "https": proxy_url}

# --- Test URL (Bright Data Geo Test) ---
test_url = "https://geo.brdtest.com/welcome.txt?product=dc&method=native"

# --- Run test ---
try:
    print("🔄 Testing proxy gateway:", PROXY_HOST)
    response = requests.get(test_url, proxies=proxies, timeout=10)
    if response.status_code == 200:
        print("✅ Proxy is working!\n")
        print(response.text)
    else:
        print(f"❌ Proxy failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"❌ Proxy connection error: {e}")
