import os
import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from multiprocessing import Process, Queue
import threading
from selenium.webdriver.support.ui import Select

NAPTIME = int(os.environ.get('NAPTIME', 10))
BASE_URL = "http://localhost:5111"

def _nap(naptime=NAPTIME):
    time.sleep(naptime)

def _run_app(q):
    from prosodic.web.app import app, socketio
    def start_server():
        socketio.run(app, port=5111, debug=False)
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    q.put("Server started")
    server_thread.join()

@pytest.fixture(scope="module")
def app_server():
    queue = Queue()
    p = Process(target=_run_app, args=(queue,))
    p.start()
    assert queue.get(timeout=30) == "Server started"
    _nap()
    yield
    p.terminate()
    p.join()

@pytest.fixture(scope="module")
def driver(app_server):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

    yield driver
    driver.quit()

def test_homepage(driver):
    driver.get(BASE_URL)
    assert "Prosodic [prə.'sɑ.dɪk]" in driver.title

def test_parse_text(driver):
    driver.get(BASE_URL)
    
    textarea = driver.find_element(By.ID, "inputtext")
    textarea.clear()
    textarea.send_keys("To be or not to be, that is the question")

    parse_button = driver.find_element(By.ID, "parsebtn")
    parse_button.click()

    # Wait for the results to load
    WebDriverWait(driver, NAPTIME).until(
        EC.presence_of_element_located((By.ID, "parseresults"))
    )

    # Print the entire page source for debugging
    print(driver.page_source)

    results = driver.find_element(By.ID, "parseresults")
    
    # Check if any part of the input text is present in the results
    assert any(part in results.text for part in ["To be", "or not to be", "that is the question"]), f"Expected text not found. Actual content: {results.text}"

def test_meter_settings(driver):
    driver.get(BASE_URL)

    max_s_select = Select(driver.find_element(By.ID, "max_s"))
    max_s_select.select_by_value("3")

    textarea = driver.find_element(By.ID, "inputtext")
    textarea.clear()
    textarea.send_keys("To be or not to be")
    
    parse_button = driver.find_element(By.ID, "parsebtn")
    parse_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "parseresults"))
    )

    results = driver.find_element(By.ID, "parseresults")
    assert "s s s" not in results.text  # No more than 3 consecutive stressed syllables

def test_error_handling(driver):
    driver.get(BASE_URL)

    textarea = driver.find_element(By.ID, "inputtext")
    textarea.clear()

    parse_button = driver.find_element(By.ID, "parsebtn")
    parse_button.click()

    # Wait for the results to load
    _nap()

    # Print the entire page source for debugging
    print(driver.page_source)

    results = driver.find_element(By.ID, "parseresults")
    assert results.text.strip() != "", f"Expected error message, but got empty result: {results.text}"

def test_long_text_parsing(driver):
    driver.get(BASE_URL)

    long_text = "To be, or not to be, that is the question:\n" * 5  # Reduced to 5 for quicker testing
    textarea = driver.find_element(By.ID, "inputtext")
    textarea.clear()
    textarea.send_keys(long_text)

    parse_button = driver.find_element(By.ID, "parsebtn")
    parse_button.click()

    # Wait for the results to load
    _nap()

    # Print the entire page source for debugging
    print(driver.page_source)

    results = driver.find_element(By.ID, "parseresults")
    assert "To be, or not to be, that is the question:" in results.text, f"Expected text not found. Actual content: {results.text}"
    
    # Count the occurrences of the phrase in the table
    table = driver.find_element(By.ID, "table_lines")
    rows = table.find_elements(By.TAG_NAME, "tr")
    count = sum(1 for row in rows if "To be, or not to be, that is the question:" in row.text)
    assert count >= 1

def test_app_run():
    queue = Queue()
    p = Process(target=_run_app, args=(queue,))
    try:
        p.start()
        # Wait for the server to start
        assert queue.get(timeout=30) == "Server started"
        
        # Give some extra time for the server to be fully ready
        _nap()
        
        # Test if the server is running
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        
    finally:
        p.terminate()
        p.join()

if __name__ == "__main__":
    pytest.main([__file__])