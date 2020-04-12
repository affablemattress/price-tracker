# price-tracker

Peridodically gathers product data from the given URLs, saves the data to log.json and notifies the user via email on any price drop. 

Supports: n11, Gittigidiyor, Hepsiburada, Amazon TR/Amazon(?)

Uses Opera webdriver by default.

# Requires Python 3.8+ to run.

### Dependencies: 
`Selenium.py`

### Commands: 
 - `mail` change adress to send mails to / change adress to send mails from.
 - `credentials` change login credentials for sites.
 - `add` add address to the tracking list.
 - `remove` remove address from the list.
 - `list` print and mail the list items.
 - `reset` reset all data.
 - `activate`  start looping through the list and notify with mail on any change. 
 - `dectivate`  breaks the loop. 
