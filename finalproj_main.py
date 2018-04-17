import json
import csv
import requests
from bs4 import BeautifulSoup
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go

CSVFILE = 'cdata.csv'
DBNAME = 'crime_database.db'
CACHE_FNAME = 'crimedata_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def get_daily_crime_data():
    baseurl = "https://spotcrime.com/mi/ann+arbor/daily"
    page_text = make_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text,'html.parser')
    findcolumn = page_soup.find(class_="main-content-column")
    findrow = findcolumn.find(class_="row")
    finda = findrow.find_all('a')
    links = []
    for d in finda:
        links.append(d['href'])
    baseurl_more = baseurl +'/more'
    page_text2 = make_request_using_cache(baseurl_more)
    page_soup2 = BeautifulSoup(page_text2,'html.parser')
    findcolumn2 = page_soup2.find(class_="main-content-column")
    findrow2 = findcolumn2.find(class_="row")
    finda2 = findrow2.find_all('a')
    for c in finda2:
        links.append(c['href'])
    simpleurl = "https://spotcrime.com"

    with open(CSVFILE, "w", newline='') as f:
        wr = csv.writer(f)
        for url in links:
            crawl_url = simpleurl + url
            crawltext = make_request_using_cache(crawl_url)
            page_soup3 = BeautifulSoup(crawltext,'html.parser')
            content_div = page_soup3.find(class_="table")
            wr.writerows([[td.text for td in row.find_all("td")] for row in content_div.select("tr + tr")])

def csv_init_db():
    print('Creating Database.')
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Data';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Data' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Date' TEXT NOT NULL,
            'Time' TEXT,
            'Name' TEXT NOT NULL,
            'CrimeId' INTEGER,
            'Address' TEXT);'''
    cur.execute(statement)
    conn.commit()

    print('Inserting Data.')
    with open(CSVFILE, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if 'AM' or 'PM' in row[2]:
                insertion = (row[2][:8], row[2][10:-1], row[1], row[3])
                statement = """INSERT INTO 'Data' VALUES (NULL, ?, ?, ?, NULL, ?)"""
                cur.execute(statement, insertion)
                conn.commit()
            else:
                insertion = (row[2][:8], row[1], row[3])
                statement = """INSERT INTO 'Data' VALUES (NULL, ?, NULL, ?, NULL, ?)"""
                cur.execute(statement, insertion)
                conn.commit()
    conn.close()

def table_2_db():
    print('Creating Database.')
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'CrimeType';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'CrimeType' (
            'Type' TEXT,
            'Id' INTEGER NOT NULL);'''
    cur.execute(statement)
    conn.commit()

    print('Inserting Data.')
    with open(CSVFILE, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        crime_list = []
        counter = 0
        for row in csvReader:
            if row[1] not in crime_list:
                crime_list.append(row[1])
        for c in crime_list:
            counter += 1
            insertion = (c, counter)
            statement = """INSERT INTO 'CrimeType' VALUES (?,?)"""
            cur.execute(statement, insertion)
            conn.commit()
    conn.close()

def update_data():
    print('Updating Id.')
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    insert = '''UPDATE Data
    SET CrimeId = (SELECT Id FROM CrimeType
    WHERE CrimeType.Type == Data.Name)'''
    cur.execute(insert)
    conn.commit()
    conn.close()

def crime_time():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    crime_by_hour = {}
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "12:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['12AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "01:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['1AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "02:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['2AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "03:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['3AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "04:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['4AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "05:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['5AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "06:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['6AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "07:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['7AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "08:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['8AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "09:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['9AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "10:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['10AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "11:__ AM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['11AM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "12:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['12PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "01:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['1PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "02:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['2PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "03:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['3PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "04:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['4PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "05:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['5PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "06:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['6PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "07:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['7PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "08:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['8PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "09:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['9PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "10:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['10PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "11:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['2PM'] = v
    query = '''SELECT COUNT(*) FROM Data WHERE Time LIKE "02:__ PM"'''
    cur.execute(query)
    v = cur.fetchone()[0]
    crime_by_hour['11PM'] = v
    return crime_by_hour

def crime_frequency():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    query = '''SELECT Name, COUNT(*) FROM Data GROUP BY Name'''
    cur.execute(query)
    freq_dict = {}
    for freq in cur:
        freq_dict[freq[0]] = freq[1]
    return freq_dict

def crime_locations():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    query = '''SELECT Address FROM Data'''
    cur.execute(query)
    list = cur.fetchall()
    streetnames = []
    for x in list:
        if 'ANN ARBOR' in x[0]:
            streetnames.append(x[0][:-10])
        elif 'YPSILANTI' in x[0]:
            streetnames.append(x[0])
    location_freq = {}
    for a in streetnames:
        parsedadd = a.split()
        for x in parsedadd:
            try:
                int(x)
                continue
            except:
                if x not in location_freq:
                    location_freq[x] = 1
                else:
                    location_freq[x] += 1
    return location_freq

def crime_over_time():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    crime_by_year = {}
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%10"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2010'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%11"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2011'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%12"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2012'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%13"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2013'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%14"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2014'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%15"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2015'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%16"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2016'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%17"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2017'] = count
    query = '''SELECT COUNT(*) FROM Data WHERE Date LIKE "%18"'''
    cur.execute(query)
    count = cur.fetchone()[0]
    crime_by_year['2018'] = count
    return crime_by_year

def interactive_prompt():
    response = ''
    while response != 'exit':
        response = input("Enter command here: ")
        if response == 'exit':
            print('Bye!')

        elif response == 'help':
            print('Available commands:\n'
              'plot crime_frequency bar\n'
              '\tcreates a bar chart of crime frequency by type.\n'
              'plot crime_time bubble\n'
              '\tcreates a bubble chart of crime rates by the hour of the day.\n'
              'plot crime_locations table\n'
              '\tcreates a table of road names in Ann Arbor and crime rates.\n'
              'plot crime_over_time line\n'
              '\tcreates a line graph of crime rates over the past 9 years.\n'
              'help\n'
              '\tprints these options\n'
              'exit\n'
              '\tquits the program')

        elif response == 'plot crime_frequency bar':
            data = [go.Bar(x=[d for d in crime_frequency().keys()], y=[e for e in crime_frequency().values()], marker=dict(color='red'))]
            layout = go.Layout(title='Instances of Crime by Type',)
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='basic-bar')

        elif response == 'plot crime_time bubble':
            size = [100, 70, 60, 40, 30, 20, 20, 20, 30, 40, 60, 70, 90, 80, 60, 80, 60, 50, 40, 30, 20, 20, 30, 60]
            trace0 = go.Scatter(x=[t for t in crime_time().keys()], y=[u for u in crime_time().values()], mode='markers',
            marker=dict(size=size,sizemode='area',sizeref=2.*max(size)/(40.**2),sizemin=4))
            data = [trace0]
            py.plot(data, filename='bubblechart-size-ref')

        elif response == 'plot crime_locations table':
            trace = go.Table(columnorder =[1,2],columnwidth = [300,250],header=dict(values=['<b>Road Name</b>', '<b>Crime Frequency</b><br>From 10/01/10 to 02/26/16'],
            line = dict(color='#7D7F80'),
            fill = dict(color='#a1c3d1'),
            align = ['center'] * 5,
            font = dict(size=16)),
            cells=dict(values=[[a for a in crime_locations().keys()],[b for b in crime_locations().values()]],
            line = dict(color='#7D7F80'),
            fill = dict(color='#EDFAFF'),
            align = ['center'] * 5))
            layout = dict(width=1200, height=800)
            data = [trace]
            fig = dict(data=data, layout=layout)
            py.plot(fig, filename = 'styled_table')

        elif response == 'plot crime_over_time line':
            trace = go.Scatter(
            x = [v for v in crime_over_time().keys()],
            y = [c for c in crime_over_time().values()],
            line = dict(color = ('rgb(205, 12, 24)'),width = 4))
            data = [trace]
            layout = dict(title = 'Crime Rates in Ann Arbor From January 2010 to February 2018',
            xaxis = dict(title = 'Year'),
            yaxis = dict(title = 'Frequency'),)

            fig = dict(data=data, layout=layout)
            py.plot(fig, filename='basic-line')

        else:
            print('Command not found. Enter "help" for more info.')

if __name__ == "__main__":
    # get_daily_crime_data()
    # csv_init_db()
    # table_2_db()
    # update_data()
    interactive_prompt()
