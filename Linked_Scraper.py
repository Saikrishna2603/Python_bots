from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import re
import time
import random
from datetime import datetime

driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
driver.maximize_window()

# Function to log in to job portals

def login_to_portal(driver, portal, username, password):
    
    if portal == "linkedin":
            driver.get("https://www.linkedin.com/login")
            driver.find_element(By.ID, "username").send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            input("Please complete the CAPTCHA or image verification, then press Enter to continue...")
            time.sleep(10)
    elif portal == "dice":
        driver.get("https://www.dice.com/dashboard/login")
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]").click()
    time.sleep(5)
    
# Function to extract email from text
def extract_emails(text):
    """Extract emails from text with enhanced pattern matching"""
    email_pattern = r"[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,64}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)

def extract_emails_from_posts(driver, KEYWORDS):
    max_posts=50
    all_emails = set()
    data = []
    for keyword in KEYWORDS:
        try:
            """Search LinkedIn posts and extract email addresses."""
            emails = set()
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={keyword.replace(' ', '%20')}"
            driver.get(search_url)
            time.sleep(10)
            filters(driver)
            click_show_more_results(driver,keyword)
            posts = driver.find_elements(By.CLASS_NAME, "feed-shared-update-v2")
            for post in posts:
                # Your existing post interaction logic
                emails = extract_emails_from_post(post)
                all_emails.update(emails)
        except Exception as e:
            print(f"Error processing keyword {keyword}: {str(e)}")
    return list(all_emails)  
    
def extract_emails_from_post(post): 
    """Extract emails from a single LinkedIn post element"""
    emails = set()
    
    try:
        # Get visible text content
        post_text = post.text
        emails.update(extract_emails(post_text))
        
        # Extract from mailto links
        mailto_links = post.find_elements(By.CSS_SELECTOR, 'a[href^="mailto:"]')
        for link in mailto_links:
            href = link.get_attribute('href')
            if href.startswith('mailto:'):
                email = href.split('mailto:')[1].split('?')[0].strip()
                if email and '@' in email:
                    emails.add(email)
                    
        # Extract from hidden text spans
        hidden_spans = post.find_elements(By.CSS_SELECTOR, 'span.visually-hidden')
        for span in hidden_spans:
            hidden_text = span.text
            emails.update(extract_emails(hidden_text))
            
    except Exception as e:
        print(f"Error extracting emails: {str(e)}")
    
    return emails

def click_show_more_results(driver,keyword):
    """Scrolls until the 'Show more results' button is found, clicks it up to 20 times, and ensures all posts are loaded."""

    max_clicks=20
    max_scroll_attempts = 10  # Maximum times to scroll while searching for the button
    click_count = 0  # Counter for button clicks
    """Click 'Show more results' button if available"""
    for _ in range(max_clicks):
        try:
            # Find the button using multiple attributes for reliability
            show_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@class, 'scaffold-finite-scroll__load-button') and contains(., 'Show more results')]")
            )
        )
            
             # Continuously scroll until "Show more results" button is found
            scroll_attempt = 0
            button_found = False
            
            while not button_found and scroll_attempt < max_scroll_attempts:
                # Scroll down
                driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(2)  # Wait for content to load
                
                # Try to find the button
                try:
                    show_more_button = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(@class, 'scaffold-finite-scroll__load-button') and contains(., 'Show more results')]")
                    )
                )
                    if show_more_button.is_displayed():
                        button_found = True
                        print(f"Found 'Show more results' button after {scroll_attempt + 1} scrolls")
                        
                except:
                    scroll_attempt += 1
                    print(f"Scrolling attempt {scroll_attempt}/{_}")
                    
            if not button_found:
                print("Could not find 'Show more results' button after maximum scroll attempts")
                break

            
            # Scroll to button and click with JavaScript
            scroll_attempt = 0  # Reset scroll attempts before clicking
            while True and scroll_attempt == 20:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", show_more_button)
                time.sleep(2)  # Allow smooth scroll effect
                scroll_attempt += 1

                

            driver.execute_script("arguments[0].click();", show_more_button)
            print(f"Clicked 'Show more results' button ({click_count + 1}/{max_clicks}) for {keyword}")

            # Wait for new content to load
            time.sleep(random.uniform(1.5, 3.5))  # Random delay to mimic human behavior
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "feed-shared-update-v2"))
            )
            click_count += 1
            
        except Exception as e:
            print(f"No more 'Show more results' button or loading failed: {str(e)}")
            break

#Function to save emails to a text file
def save_emails_to_excel(emails):
    """Save extracted email addresses to a text file in ["",""] format."""
    file_name = f"LinkedIn_Post_Emails_{datetime.today().strftime('%Y-%m-%d')}.txt"
    formatted_emails = '[\n' + ',\n'.join([f'    "{email}"' for email in emails]) + '\n]'
     # Write to text file
    with open(file_name, 'w') as f:
        f.write(formatted_emails)
    print(f"Emails saved in list format to {file_name}")

#Filters
def filters(driver):
    # Open 'All filters' menu
        driver.find_element(By.XPATH, "//button[text()='All filters']").click()
        time.sleep(2)
        
        #Sort By latest posts
        date_posted = driver.find_element(By.XPATH, "//label[contains(., 'Latest')]")
        date_posted.click()
        
        # Apply 'Date Posted' filter (Past 24 hours)
        date_posted = driver.find_element(By.XPATH, "//label[contains(., 'Past 24 hours')]")
        date_posted.click()
        
        # Click 'Show Results'
        driver.find_element(By.XPATH, "//button[contains(@class, 'artdeco-button--primary')]").click()
        time.sleep(3)
        
# Main automation logic
def Scraper():
    credentials = {
        "linkedin": {"username": "krishna7072.m@gmail.com", "password": "marketing@2024"},
    }


    for portal, creds in credentials.items():
        try:
            login_to_portal(driver, portal, creds["username"], creds["password"])
            # Keywords for searching LinkedIn posts
            KEYWORDS = [
                "c2c", "java developer", "sr. full stack java developer", 
                "full stack java developer", "java full stack developer", 
                "java backend developer", "java engineer", "software engineer","java"
                ,"full stack developer","backend developer","java engineer"
            ]
            
            emails = extract_emails_from_posts(driver, KEYWORDS)
            save_emails_to_excel(emails)
            driver.quit()
        except Exception as e:
            print(f"Error with {portal}: {e}")

    driver.quit()
    
if __name__ == "__main__":
    print("LinkedIN Post Scraper Started.")
    Scraper()
