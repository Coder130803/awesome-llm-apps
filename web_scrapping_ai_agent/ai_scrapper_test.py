from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import streamlit as st
import os
import time
from scrapegraphai.graphs import SmartScraperGraph

# Set up the Streamlit app
st.title("Web Scraping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape a website using the OpenAI API")

# Get OpenAI API key from os
openai_access_token = Open_AI_Key

# Select the model
model = st.radio(
    "Select the model",
    ["gpt-3.5-turbo", "gpt-4"],
    index=0,
)

graph_config = {
    "llm": {
        "api_key": openai_access_token,
        "model": model,
    },
}

def create_driver_instance(driver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    return driver

# Get the URL of the website to scrape
url = st.text_input("Enter the URL of the website you want to scrape")
if url:
    # Use WebDriver Manager to handle ChromeDriver
    driver_path = '/Users/sahil_p/awesome-llm-apps/chromedriver-mac-arm64/chromedriver'
    driver = create_driver_instance(driver_path)
    driver.get(url)

    # Ensure the page is fully loaded
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")

    wait = WebDriverWait(driver, 30)  # Increase the wait time to 30 seconds

    try:
        # Wait until the element is located
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.results-base")))
        page_content = driver.page_source
        print("debug")
        print(page_content[:2000])  # Print first 2000 characters to avoid too long output

        # Get the user prompt
        user_prompt = st.text_input("What do you want the AI agent to scrape from the website?")
        if user_prompt:
            # Create a SmartScraperGraph object
            smart_scraper_graph = SmartScraperGraph(
                prompt=user_prompt,
                source=page_content,
                config=graph_config
            )
            # Scrape the website
            if st.button("Scrape"):
                with st.spinner('Scraping the website...'):
                    try:
                        result = smart_scraper_graph.run()
                        st.success("Scraping completed successfully!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
    except TimeoutException:
        st.error("TimeoutException: Element not found")
    
    driver.quit()
