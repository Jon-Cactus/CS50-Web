import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

def file_uri(filename):
    # Turns a relative path into an abslute path as a Path object with `file:///` prefix
    return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome()

# Set up unittest's TestCase class
class WebPageTests(unittest.TestCase):

    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        driver.get(file_uri("counter.html"))
        increase = driver.find_element(By.ID, "increase")
        increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "1")

    def test_decrease(self):
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element(By.ID, "decrease")
        decrease.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "-1")
    
    def test_multiple_increase(self):
        driver.get(file_uri("counter.html"))
        increase = driver.find_element(By.ID, "increase")
        for i in range(5):
            increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "5")

if __name__ == "__main__":
    unittest.main()