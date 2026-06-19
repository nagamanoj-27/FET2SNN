try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("Selenium is installed!")
except ImportError:
    print("Selenium is NOT installed.")
