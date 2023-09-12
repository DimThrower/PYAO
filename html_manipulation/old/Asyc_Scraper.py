import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from HTML import HTML
from HTML_ACTIONS import click, innerHTML_Drill, sim_click
from chrome_settings import custom_chrome_options, un_custom_chrome_options, generate_random_number
import undetected_chromedriver as uc

html = HTML()

async def scrape_website(name, url, prop_dict):
        # Set up the Selenium WebDriver


    # chromeDriverPath = r'C:\Program Files (x86)\chromedriver.exe'
    # browser = webdriver.Chrome(executable_path=chromeDriverPath, options=custom_chrome_options()) 

    #Using modified chromedriver.exe ... "replaced cdc_asdjflasutopfhvcZLmcfl_" with "btlhsaxJbTXmBATUDvTRhvcZLm_"
    chromeDriverPath = r'C:\Program Files (x86)\mod_chromedriver.exe'

    # Use undetected_chromedriver and Options

    try:

        # Putting in a function to wait a random amount to not flag bots
        async def rand_wait(start_range=3, end_range=5): 
            await asyncio.sleep(generate_random_number(start_range, end_range))

        if "zillow" in name:
            for key, value in prop_dict.items():
                try:
                    browser = uc.Chrome(chromeDriverPath=chromeDriverPath, options=un_custom_chrome_options()) 
                
                    # Create the zilow link
                    # Replace spaces with a dash
                    address = value['Street Address'].replace(" ", "-")
                    zillow_url = f"{url}-{address}-{value['Zip Code']}"
                    
                    # Navigate to url
                    browser.get(zillow_url)

                    # Wait for page to load
                    WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, html.selectors['zillow']['Price Page'])))

                    # Parse Price Page
                    soup = BeautifulSoup(browser.page_source, 'html.parser')

                    # Find the older sibling to the price element
                    older_sibling = soup.select_one(html.selectors['zillow']['Sibling Div Price'])

                    # Find the next sibling
                    price_element = older_sibling.next_sibling

                    # Drill down to the innerHTML of the price_elemet
                    est_ARV = innerHTML_Drill(price_element)
                    print(f"ARV Estimate: {est_ARV}")

                finally:
                    # Put in a wait as to not pull up flags
                    await rand_wait()

                    browser.quit()
                    



        if "not" in name:        

            # Navigate to the URL
            browser.get(url)

            # Input the address into the input
            print(f"(Async) Prop Dictionary: {prop_dict}")

            # Put Wait so broweser don't think I'm a bot
            for key, value in prop_dict.items():
                # await asyncio.sleep(rand_wait())
                print(f"Selector: {html.selectors[name]['Address Input']}")

                # Find the the input element
                input_element = browser.find_element(By.CSS_SELECTOR, html.selectors[name]['Address Input'])

                # Simulate human click of input element
                next_x, next_y = await sim_click(browser,
                                    element_css=html.selectors[name]['Address Input'],
                                    duration=generate_random_number(1),
                                    start_x=100,
                                    start_y=100)

                # input_element.click()
                # browser.execute_script("arguments[0].focus();", input_element)

                # Wait before putting in address info
                await asyncio.sleep(5) #generate_random_number(1,2))

                # Put the address and zipcode in the input
                browser.execute_script("arguments[0].value = arguments[1];", input_element, f"{value['Street Address']} {value['Zip Code']}")

                # Find the Search Button
                # search_element = browser.find_element(By.CSS_SELECTOR, html.selectors[name]['Search'])

                # Wait before clicking Seach button
                await rand_wait()

                # Click the Search button
                # search_element.click()

                # Simulate human click for search
                await sim_click(browser,
                                element_css=html.selectors[name]['Search'],
                                duration=generate_random_number(.5),
                                start_x=next_x,
                                start_y=next_y)

                
    finally:
        # Wait before closing the browser
        await rand_wait()

        # Close the broswer
        browser.quit()

    # Return the extracted data
    return 'data'

async def scrape_multiple_websites(urls_dict, prop_dict):
    # Create tasks to scrape each website concurrently
    tasks = []

    for name, url in urls_dict.items():
        print(f"scrap_muliple_website: STILL RUNNING")
        task = asyncio.create_task(scrape_website(name, url, prop_dict))
        tasks.append(task)

    # Wait for all tasks to complete
    scraped_data = await asyncio.gather(*tasks)

    # Process the scraped data as needed

    # Print or return the final result
    print(scraped_data)

async def main(urls_dict, prop_dict):
    print(f'main STILL RUNNING')
    await scrape_multiple_websites(urls_dict, prop_dict)

