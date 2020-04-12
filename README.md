# price-tracker

Peridodically gathers product data from the given URLs, saves the data to log.json and notifies the user via email on any price drop.

Currently supported websites: n11, Gittigidiyor, Hepsiburada, Amazon TR/Amazon(?)

# Requires Python 3.8+ to run.

### Dependencies: 
`Selenium.py`

### Commands: 
 - `mail` change adress to send mails to / change adress to send mails from.
 - `credentials` change login credentials for sites.
 - `add` add address to list.
 - `remove` remove address from list.
 - `list` print and mail the list items.
 - `reset` reset data.
 - `activate`  start looping through the list and notify with mail on any change.
