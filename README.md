# si206-finalproject

My final projects crawls and scrapes multiple webpages from https://spotcrime.com/mi/ann+arbor/daily. After scraping the webpages using BeautifulSoup, the raw data is first stored in a cache. The raw data is then processed into a CSV file, making it simpler to import into a DB file.

My program has three main parts, the first part being scraping and caching the data using get_daily_crime_data(). The following few functions such as csv_init_db() and table_2_db() manipulates and stores the data into a database. The second part of the code is for processing the data from the database, with functions such as crime_time() and crime_frequency() that creates dictionaries of crime data and is used in part three. crime_locations() creates a big dictionary of street names and the number of times that happen on that street. The final main part of my project consists of the interactive_prompt(), which allows users to interact with the program and create plotly visualizations.

How to use the program:
1) Run the function get_daily_crime_data() to scrape and cache the webpages for crime data in Ann Arbor. This will take about 30 minutes to finish caching. The function also inserts data from cache into a CSV file. Open the CSV file and delete lines 2841-2845 & 20650-20654.
2) Run csv_init_db(), table_2_db(), update_data() to create database.
3) Call the function interactive_prompt(), which allows you to create plots from the database. Available commands:
  "plot crime_frequency bar"
  - creates a bar chart of crime frequency by type.
  "plot crime_time bubble"
  - creates a bubble chart of crime rates by the hour of the day.
  "plot crime_locations table"
  - creates a table of road names in Ann Arbor and crime rates.
  "plot crime_over_time line"
  - creates a line graph of crime rates over the past 9 years.
  "help"
  - prints these options
  "exit"
  - quits the program
