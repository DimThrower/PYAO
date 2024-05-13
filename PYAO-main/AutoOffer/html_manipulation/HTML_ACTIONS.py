from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException
import ctypes, time, asyncio, math

# Since there is a wait in this function, and it used in a async function we need to make the wait async... i think
async def sim_click(browser, element_css, duration, start_x, start_y):

    def ease_in_out_quad(t):
        return t * t * (3 - 2 * t)

    def interpolate(start, end, progress):
            # Use a curved interpolation function
        return start + (end - start) * (math.sin(progress * math.pi - math.pi / 2) + 1) / 2
    
    # Get the element
    element = browser.find_element(By.CSS_SELECTOR, element_css)
    
    # Get the coordinates of the target element
    target_location = element.location
    target_size = element.size

    # Calculate the center coordinates of the target element
    target_x = target_location['x'] + (target_size['width'] // 2)
    target_y = target_location['y'] + (target_size['height'] // 2)

    # Define the duration and the number of steps for the movement
    duration = duration  # Duration in seconds
    steps = 60  # Number of steps

    # Calculate the distance between current position and target position
    distance_x = target_x
    distance_y = target_y

    # Execute JavaScript to simulate smooth mouse movement towards the target element
    for i in range(steps):
        progress = ease_in_out_quad(i / steps)
        current_x = int(interpolate(start_x, distance_x, progress))
        current_y = int(interpolate(start_y, distance_y, progress))

        browser.execute_script(f"var ev = document.createEvent('MouseEvent');"
                              f"ev.initMouseEvent('mousemove', true, true, window, null, 0, 0, {current_x}, {current_y}, false, false, false, false, 0, null);"
                              f"window.dispatchEvent(ev);")

        # Calculate the sleep time based on the duration divided by the number of steps
        sleep_time = duration / steps
        await asyncio.sleep(sleep_time)

    # Simulate click by executing JavaScript click on the element
    browser.execute_script("arguments[0].click();", element)

    # Return ending poisitions so next simulate click knows wher to start
    return (target_x, target_y)




def innerHTML_Drill (current_tag):
    """
    Recursively drills down into the DOM until a non-blank inner HTML is found.
    Args:
        current_tag: The current BeautifulSoup tag being processed.
    Returns:
        The inner HTML of the first non-blank tag found, or None if no inner HTML is found.
    """
    if current_tag:
        if current_tag.string and current_tag.string.strip():
                return current_tag.string.strip()
        else:
                if current_tag.find():
                    return innerHTML_Drill(current_tag.find())
                else: 
                        # print('No innerHTML found')
                        return None
    else: return None
            

def click(browser, wait, e_type, element, errmsg, allow_errmsg = False):
        # ID Element
        if e_type == 'id':
            try:
                WebDriverWait (browser, wait).until (
                    ec.element_to_be_clickable ((By.ID, element)))  # Setting timeout for 'Prospect' button to load
                browser.find_element(By.ID, element).click ()  # Clicking the 'Prospects' button
                return True

            except:# (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                print (errmsg)  # Error thrown if loading takes longer than the specified time
                if allow_errmsg is True:
                    ctypes.windll.user32.MessageBoxW (0, errmsg, "Timed Out", 1)
                return False

        # CLASS Element
        if e_type == "class":
            try:
                WebDriverWait(browser, wait).until(
                    ec.element_to_be_clickable((By.CLASS_NAME, element)))  # Setting timeout for 'Prospect' button to load
                browser.find_element(By.CLASS_NAME, element).click()  # Clicking the 'Prospects' button
                return True

            except:# (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                print(errmsg)  # Error thrown if loading takes longer than the specified time
                if allow_errmsg is True:
                    ctypes.windll.user32.MessageBoxW(0, errmsg, "Timed Out", 1)
                return False

        # HREF Element
        if e_type == "href":
            try:
                WebDriverWait(browser, wait).until(
                    ec.element_to_be_clickable((By.LINK_TEXT, element)))  # Setting timeout for 'Prospect' button to load
                browser.find_element(By.LINK_TEXT, element).click()  # Clicking the 'Prospects' button
                return True

            except:# (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                print(errmsg)  # Error thrown if loading takes longer than the specified time
                if allow_errmsg is True:
                    ctypes.windll.user32.MessageBoxW(0, errmsg, "Timed Out", 1)
                return False

        # CSS Element
        if e_type == "css":
            try:
                WebDriverWait(browser, wait).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, element)))  # Setting timeout for 'Prospect' button to load
                browser.find_element(By.CSS_SELECTOR, element).click()  # Clicking the 'Prospects' button
                return True

            except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                print(errmsg)  # Error thrown if loading takes longer than the specified time
                if allow_errmsg is True:
                    ctypes.windll.user32.MessageBoxW(0, errmsg, "Timed Out", 1)
                return False



        # XPATH Element
        if e_type == "xpath":
            try:
                WebDriverWait(browser, wait).until(
                    ec.element_to_be_clickable((By.XPATH, element)))  # Setting timeout for 'Prospect' button to load
                browser.find_element(By.XPATH, element).click() # Clicking the 'Prospects' button
                return True

            except:# (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                print(errmsg)  # Error thrown if loading takes longer than the specified time
                if allow_errmsg is True:
                    ctypes.windll.user32.MessageBoxW(0, errmsg, "Timed Out", 1)
                return False

        # LINK TEXT Element
        if e_type == "linktext":
            try:
                WebDriverWait(browser, wait).until(
                    ec.element_to_be_clickable((By.LINK_TEXT, element)))  # Setting timeout for 'Prospect' button to load
                browser.find_element(By.LINK_TEXT, element).click()  # Clicking the 'Prospects' button
                return True

            except:# (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                print(errmsg)  # Error thrown if loading takes longer than the specified time
                if allow_errmsg is True:
                    ctypes.windll.user32.MessageBoxW(0, errmsg, "Timed Out", 1)
                return False
        