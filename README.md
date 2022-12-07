## Usage

1. Create a `credential.json` file and add in your information like so:
   ```json
   {
     "tp": "tp123456",
     "pass": "Tp123456@1111"
   }
   ```
2. Install all necessary dependencies via `pip install -r requirements.txt`
3. Run the program: `py main.py`
4. Install the web drivers that you need:
  - chrome: https://chromedriver.chromium.org/downloads
  - edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
  - firefox: https://github.com/mozilla/geckodriver/releases

## Changing web browser

We support Google Chrome, Microsoft Edge, and Firefox. To use either of it, make sure you have the actual browser installed.
To change browser, go to `option.json` and change to `"chrome"`, `"edge"`, and `"firefox"` for Google Chrome, Microsoft Edge, and Firefox respectively.

This program is only capable of running on Windows. Feel free to contribute if you are using other operating system!
