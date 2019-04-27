# import Dependecies 
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    # choose the executable path to driver
    executable_path = {"executable_path": "./chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
	browser = init_browser()

	# create surf_data dict that we can insert into mongo
	mars_data = {}

	# NASA Mars
	news_url = 'https://mars.nasa.gov/news'
	browser.visit(news_url)
	news_html = browser.html
	news_soup = bs(news_html,'lxml')
	news_title = news_soup.find('div', class_='content_title').text
	news_p = news_soup.find('div', class_='article_teaser_body').text

	# add title and summary to mars data dict
	mars_data['news_title'] = news_title
	mars_data['summary'] = news_p

	
	# JPL Mars Space Images - Featured Image
	jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(jpl_url)
	jpl_html = browser.html
	jsoup = bs(jpl_html,'lxml')
	img_link = jsoup.find('div', class_='carousel_container').article.footer.a['data-fancybox-href']
	base_link = 'https://www.jpl.nasa.gov'
	featured_image_url = base_link + img_link

	# add featured image to mars data dict
	mars_data['featured_image'] = featured_image_url


	# Mars Weather
	weather_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(weather_url)
	w_html = browser.html
	wsoup = bs(w_html,'lxml')
	tweets = wsoup.find_all('p', class_='TweetTextSize')
	for tweet in tweets:
		weather_tweet = tweet.find('a').previousSibling
		if 'sol' and 'pressure' in weather_tweet:
			break
		else:
			continue
	mars_weather = weather_tweet.replace("\n",", ")

	# add weather to mars data dict
	mars_data['weather'] = mars_weather

	# Mars Facts
	fact_url = 'https://space-facts.com/mars/'
	fact_table = pd.read_html(fact_url)
	mars_fact_table = fact_table[0]
	mars_fact_table.columns = ['Description','Value']
	mars_fact_table_html = mars_fact_table.to_html (header=True, index=False, justify='center')
	mars_fact_table_html = mars_fact_table_html.replace('\n', '')

	# add facts table to mars data dict
	mars_data['fact_table'] = mars_fact_table_html


	# Mars Hemispheres
	hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hem_url)
	hem_html = browser.html
	hsoup = bs(hem_html,'lxml')
	items = hsoup.find_all('div', class_='item')
	hemisphere_image_urls = []
	hemispheres_main_url = 'https://astrogeology.usgs.gov'
	for i in items: 
		title = i.find('h3').text.strip(' Enhanced')
		partial_img_url = i.find('a', class_='itemLink product-item')['href']
		browser.visit(hemispheres_main_url + partial_img_url)
		partial_img_html = browser.html
		hsoup = bs(partial_img_html,'lxml')
		img_url = hemispheres_main_url + hsoup.find('img', class_='wide-image')['src']
		hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

	# add facts table to mars data dict
	mars_data['hemisphere_image'] = hemisphere_image_urls


	# Close the browser after scraping
	browser.quit()

	# Return results
	return mars_data

if __name__ == "__main__":
	scrape()