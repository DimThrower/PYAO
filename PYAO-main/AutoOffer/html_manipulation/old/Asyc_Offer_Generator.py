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

chromeDriverPath = r'C:\Program Files (x86)\mod_chromedriver.exe'

async def rand_wait(start_range=3, end_range=6): 
    await asyncio.sleep(generate_random_number(start_range, end_range))

import asyncio

async def task(task_id):
    print(f"Starting task {task_id}")
    # This is where my code for puting info in Rhino Needs to go
    # and possible 
    try:
        browser = uc.Chrome(chromeDriverPath=chromeDriverPath, options=un_custom_chrome_options()) 
        browser.get(zillow_url)
        pass
    finally:
        browser.quit()

    
    await rand_wait()  # Simulating some task work
    print(f"Task {task_id} finished")

async def run_tasks():
    queue = asyncio.Queue()

    # Enqueue initial tasks
    # I think is where the first batch of proprties 
    # will go when the function is first opend
    for i in range(1, 15):
        await queue.put(i)

    # This limits the number of cocurrent operations to 5
    semaphore = asyncio.Semaphore(5)

    # Function the processes an async task
    async def process_task(task_id):
        # Require task to wait aquire a permit from Semaphore 
        async with semaphore:
            # After semaphore grants premit 
            # Await for the completion of the task
            await task(task_id)


    while True:
        # Initialize list to store tasks
        tasks = []

        # Continuously retrieves tasks from a queue and 
        # creates asyncio tasks to process them concurrently
        # Check to ensure list is not empty
        while not queue.empty():
            # Retrieve the latest queued task from queue
            task_id = await queue.get()

            # Create an asyncio task and add it to the task list
            tasks.append(asyncio.create_task(process_task(task_id)))

        # Check to see if tasks list is empty
        if not tasks:
            # Exit the loop if there are no more tasks
            break

        # Wait for all tasks to complete
        # The "*" unpacks the tasks list into seperate elements
        await asyncio.gather(*tasks)  
        
        # This is where I might use a socket to send more que more tasks
        # Add more tasks dynamically if needed
        # for i in range(len(tasks)):
        #     # Add more tasks to the que
        #     await queue.put(i + 1)

# Run the tasks
loop = asyncio.get_event_loop()
loop.run_until_complete(run_tasks())