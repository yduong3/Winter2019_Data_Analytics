
# Mission to Mars

![mission_to_mars](Images/mission_to_mars.jpg)

Build a web application that scrapes various websites for data related to the Mission to Mars and display the information in a single HTML page.



```python
# Declare Dependencies 
import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
```


```python
# Choose the executable path to driver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
```

### NASA Mars News

- Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign text to variables to reference later.


```python
# Visit NASA news url through splinter module
news_url = 'https://mars.nasa.gov/news'
browser.visit(news_url)
```


```python
# HTML object to create a Beautiful Soup object
news_html = browser.html
news_soup = bs(news_html,'lxml')
```


```python
# Retrieve elements that contains the latest news title and news_paragraph
news_title = news_soup.find('div', class_='content_title').text
news_p = news_soup.find('div', class_='article_teaser_body').text
```


```python
# Print scrapped data 
print(news_title)
print(news_p)
```

    NASA Social Media and Websites Win Webby Awards 
    NASA's social media presence, the InSight mission social media accounts, NASA.gov and SolarSystem.NASA.gov will be honored at the 2019 Webby Awards - "the Oscars of the Internet."
    

### JPL Mars Space Images - Featured Image

- Visit JPL Featured Space Image.
- Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.


```python
# Visit Mars Space Images through splinter module
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)
```


```python
# HTML object to create a Beautiful Soup object
jpl_html = browser.html
jsoup = bs(jpl_html,'lxml')
```


```python
# Retrieve background-image url from style tag and print img_link
img_link = jsoup.find('div', class_='carousel_container').article.footer.a['data-fancybox-href']
print(img_link)
```

    /spaceimages/images/mediumsize/PIA16682_ip.jpg
    


```python
# Retrive base url and concatenate website url with scrapped route
base_link = 'https://www.jpl.nasa.gov'
featured_image_url = base_link + img_link

# Print full link to featured image
print(featured_image_url)
```

    https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA16682_ip.jpg
    

### Mars Weather

- Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.


```python
# Visit Mars Weather Twitter through splinter module
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)
```


```python
# HTML object to create a Beautiful Soup object
w_html = browser.html
wsoup = bs(w_html,'lxml')
```


```python
tweets = wsoup.find_all('p', class_='TweetTextSize')
for tweet in tweets:
    weather_tweet = tweet.find('a').previousSibling
    if 'sol' and 'pressure' in weather_tweet:
        break
    else:
        continue
weather_tweet
```




    'InSight sol 144 (2019-04-23) low -98.7ºC (-145.7ºF) high -17.6ºC (0.4ºF)\nwinds from the SW at 4.2 m/s (9.5 mph) gusting to 11.1 m/s (24.8 mph)\npressure at 7.40 hPa'




```python
#Replace new line with , and print data
mars_weather = weather_tweet.replace('\n',', ')
print(mars_weather)
```

    InSight sol 144 (2019-04-23) low -98.7ºC (-145.7ºF) high -17.6ºC (0.4ºF), winds from the SW at 4.2 m/s (9.5 mph) gusting to 11.1 m/s (24.8 mph), pressure at 7.40 hPa
    

### Mars Facts

- Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
- Use Pandas to convert the data to a HTML table string.


```python
# Visit Mars facts url 
fact_url = 'https://space-facts.com/mars/'
```


```python
# Use Panda's 'read_html' to parse the url
fact_table = pd.read_html(fact_url)

# Find the Mars facts table
mars_fact_table = fact_table[0]
mars_fact_table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Assign the columns Description and Value and use Description as index
mars_fact_table.columns = ['Description','Value']
mars_fact_table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Description</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Generate HTML table from Mars facts dataframe
mars_fact_table_html = mars_fact_table.to_html (header=True, index=False, justify='center')
```


```python
#Strip unwanted newlines to clean up the table and print
mars_fact_table_html = mars_fact_table_html.replace('\n', '')
print(mars_fact_table_html)
```

    <table border="1" class="dataframe">  <thead>    <tr style="text-align: center;">      <th>Description</th>      <th>Value</th>    </tr>  </thead>  <tbody>    <tr>      <td>Equatorial Diameter:</td>      <td>6,792 km</td>    </tr>    <tr>      <td>Polar Diameter:</td>      <td>6,752 km</td>    </tr>    <tr>      <td>Mass:</td>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <td>Moons:</td>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <td>Orbit Distance:</td>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <td>Orbit Period:</td>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <td>Surface Temperature:</td>      <td>-153 to 20 °C</td>    </tr>    <tr>      <td>First Record:</td>      <td>2nd millennium BC</td>    </tr>    <tr>      <td>Recorded By:</td>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>
    

### Mars Hemispheres

- Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.


```python
# Visit hemispheres website through splinter module 
hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hem_url)
```


```python
# HTML object to create a Beautiful Soup object
hem_html = browser.html
hsoup = bs(hem_html,'lxml')
```


```python
# # Retreive all items that contain mars hemispheres information
items = hsoup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items
for i in items: 
    # Store title
    title = i.find('h3').text.strip(' Enhanced')
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    hsoup = bs(partial_img_html,'lxml')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + hsoup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

# Print hemisphere_image_urls
print(hemisphere_image_urls)
```

    [{'title': 'Cerberus Hemispher', 'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}, {'title': 'Schiaparelli Hemispher', 'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}, {'title': 'Syrtis Major Hemispher', 'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}, {'title': 'Valles Marineris Hemispher', 'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]
    
