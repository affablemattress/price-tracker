# price-tracker

Peridodically gathers product data from the given URLs, saves the data to log.json and notifies the user via email on any price drop. 

# Requires Python 3.8+ to run.

Uses Opera webdriver by default.

### Dependencies: 
`Selenium.py`

### Commands: 
 - `mail` change address to send mails to / change adress to send mails from.
 - `credentials` change login credentials for websites.
 - `add` add a new address to the tracking list.
 - `remove` remove an address from the list.
 - `list` print and mail the list items.
 - `reset` reset all data.
 - `activate` start looping through the list and notify with mail on any change. 
 - `dectivate` breaks the loop. 
