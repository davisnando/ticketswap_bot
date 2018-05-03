# Ticketswap bot

to install:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` git clone https://github.com/davisnando/ticketswap_bot.git `

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` cd ticketswap_bot `

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` python -m venv .env`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` source .env/bin/activate`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` pip install -r requirements.txt `


download here your chromedriver: https://chromedriver.storage.googleapis.com/index.html?path=2.36/
unzip the driver that you need and move the file to:

### For linux:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`mv chromedriver /usr/bin/chromedriver` 

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cd /usr/bin/`
 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`chmod a+x chromedriver`

### For Mac:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`mv chromedriver /usr/local/bin/chromedriver` 
 
 
### For windows:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; move the chromedriver.exe file to: `<PYTHON FOLDER>/scripts`


## For the headless script (Linux only I think):
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `sudo apt install xvfb`
 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `pip install pyvirtualdisplay`
