# Hofer product alert
A personal script that checks whether a specific product is available
on the Slovenian Hofer's website. If a specific product is available, 
an email will be sent to your email address.

Note that this is a script for personal purposes only.

## Usage
First, download and unzip the chromedriver (You need to have google-chrome installed).
```bash
wget https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```

Install the pip requirements:
```bash
pip install -r requirements.txt
```

To run the script:
```bash
SENDGRID_API_KEY=<your-sendgrid-api-key>\ PATH_TO_CHROMEDRIVER=<your-path-to-chromedriver>\
EMAIL_ADDRESS=<your-email-address>\
python3 <your> <product> <list>
```

You can run the script periodically by using cron scheduler.

