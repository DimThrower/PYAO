from selenium import webdriver
import random
#import undetected_chromedriver as uc


def generate_random_ip():
    octets = []
    for _ in range(4):
        octet = random.randint(0, 255)
        octets.append(str(octet))
    ip_address = ".".join(octets)
    return ip_address

def generate_random_number(start_range=1024, end_range=65535):
    return random.randint(start_range, end_range)

# Define user, ip, and ports. Combine into one list
def user_proxy():
    # A list of user agents show uniqueness
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4806.53 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4895.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4947.23 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.4987.42 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5029.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5075.96 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5121.23 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5168.48 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5215.75 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5263.12 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5309.29 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5355.56 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5401.83 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5447.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5493.163 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5541.96 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5596.32 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5649.57 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5704.86 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5761.123 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.5820.41 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.5879.68 Safari/537.36",
    ]

    # Most of these don't seem to work so I'm only using the good ones
    # These ip address don't work, need to get a paid version sometime in the future
    proxy_list = [
        ("216.137.184.253", 80),
        ("143.42.163.193", 80),
        ("103.152.112.234", 80),
        ("149.19.40.78", 8082),
        ("72.170.220.17", 8080),
        ("107.152.32.195", 8080), # good
        ("64.225.8.179", 9996),
        ("107.152.32.114", 8080), # good
        ("64.225.4.12", 9998),
        ("64.225.4.81", 9991), 
        ("207.2.120.19", 80),
        ("64.225.8.82", 9978),
        ("162.212.153.76", 8080), # good
        ("174.108.200.2", 8080),
        ("162.202.70.105", 1888),
        ("64.225.8.121", 9987),
        ("64.225.4.63", 9991),
    ]

    screen_sizes = (
    ("1920,1080"),
    ("1366,768"),
    ("1280,800"),
    ("1440,900"),
    ("1024,768"),
    ("1680,1050"),
)

    combined_list = []

    for i, user_agent in enumerate(user_agents):
        proxy = proxy_list[i % len(proxy_list)]
        screen_size = screen_sizes[i % len(screen_sizes)]
        combined_list.append((user_agent, proxy, screen_size))

    return combined_list

def custom_chrome_options():
    options = webdriver.ChromeOptions()
    # Set up the proxy server
    proxy_host = generate_random_ip
    # proxy_port = generate_random_port()

    proxy = f'{proxy_host}:80'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')

    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Example options for human-like behavior
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    # options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Disable /dev/shm usage
    options.add_argument('--referer=https://www.google.com/search?q=home+estimates&source=hp&ei=Yx1nZKgwq6uq2w_qionYAQ&iflsig=AOEireoAAAAAZGcrczpjbh4CuT5G8HNFbxKO2typfuei&ved=0ahUKEwjo7Z_B5oD_AhWrlWoFHWpFAhsQ4dUDCAs&uact=5&oq=home+estimates&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOhAIABADEI8BEOoCEIwDEOUCOhAILhADEI8BEOoCEIwDEOUCOggIABCABBCxAzoLCC4QgAQQsQMQgwE6EQguEIAEELEDEIMBEMcBENEDOgsILhCKBRCxAxCDAToLCAAQgAQQsQMQgwE6CwguEIAEEMcBENEDOhQILhCABBCxAxCDARDHARDRAxDUAjoRCC4QgwEQxwEQsQMQ0QMQgAQ6DgguEIAEELEDEMcBENEDOggILhCxAxCABDoLCC4QrwEQxwEQgAQ6CAgAEIoFEJIDOggILhCABBCxAzoRCC4QgwEQrwEQxwEQsQMQgAQ6EQguEIoFELEDEIMBEMcBEK8BOgsIABCKBRCxAxCDAToFCC4QgAQ6CwgAEIAEELEDEMkDOgsILhCABBCxAxDUAlCMBVi9N2CvOWgHcAB4AIABWYgBtQuSAQIyMJgBAKABAbABCg&sclient=gws-wiz')  # Replace with the desired referrer URL

    return options

def un_custom_chrome_options():
    # Website with info on how to hide bot https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

    # Get thee list that contains, user, proxy, and list
    user_proxy_screen_list = user_proxy()

    options = webdriver.ChromeOptions()

    # Generate a randowm number that dictates what ip, port, and user will be used
    print(f"Length of user_proxy_list: {len(user_proxy_screen_list)}")
    rand_index = generate_random_number(0, len(user_proxy_screen_list)-1)

    # Get and set random window size from user_proxy_screen_list
    options.add_argument(f"window-size={user_proxy_screen_list[rand_index][2]}")

    #For ChromeDriver version 79.0.3945.16 or over
    options.add_argument('--disable-blink-features=AutomationControlled')
                                        
    #Will pick a random user agent from list
    options.add_argument(f"--user-agent={user_proxy_screen_list[rand_index][0]}")

    # Will diable Pop ups
    options.add_argument("--disable-popup-blocking")
    
    # This retains the cookies
    # options.add_argument("user-data-dir=selenium") 

    # Get and set random ip address from user_proxy_screen_list
    # options.proxy_host = user_proxy_screen_list[rand_index][1][0]
    
    # Get and set random port number from user_proxy_screen_list
    # options.proxy_port = user_proxy_screen_list[rand_index][1][1]   

    return options






