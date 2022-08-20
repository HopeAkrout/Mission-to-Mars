# Mission-to-Mars

The client wanted to build a site that had the latest news and photos of Mars.  The project utilized Jupyter Notebook to test the code first, then export to a .py to go into effect.  The scraping.py is aptly named; this code scrapes the various sites required to gather all of the requested data and will work until the site structure is updated as the commands are to scrape the latest headline, latest photo, etc. and not hardcoding specific site addresses for data.

The app.py file is run with flask through Mongo database to run the command for scraping.py to run and temporarily store the data. The index.html file merely configures the web page layout and asthetics.