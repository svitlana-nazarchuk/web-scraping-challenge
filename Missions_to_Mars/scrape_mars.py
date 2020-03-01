
from bs4 import BeautifulSoup as bs
import requests
#import time
import pandas as pd
import pymongo




def scrape():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

# Select database and collection to use
    db = client.mars
    collection = db.mars_data
    

    # Scrape the NASA Mars News Site
    url_nasa="https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response_nasa=requests.get(url_nasa)
    soup_nasa=bs(response_nasa.text, "html.parser")
    resp=response_nasa.json()
    #news title
    news_title=resp['items'][0]['title']
    #news paragraph
    news_p=resp['items'][0]['description']
    
    #Visit the url for JPL Featured Space Image 
    url_jpl="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response_jpl=requests.get(url_jpl)
    soup_jpl=bs(response_jpl.text, "html.parser")
    result_img=soup_jpl.find('img', class_='thumb')
    featured_image_url='https://www.jpl.nasa.gov'+result_img['src']

    #Scrape the latest Mars weather from Mars Weather twitter account
    url_weather="https://twitter.com/marswxreport?lang=en"
    response_weather=requests.get(url_weather)
    soup_weather=bs(response_weather.text, "html.parser")
    mars_weather=soup_weather.find_all('p')[4].text
    mars_weather=mars_weather.replace('\n', ' ')

    #Visit the Mars Facts webpage and use Pandas to scrape the table containing 
    #facts about the planet
    url_facts="https://space-facts.com/mars"
    response_facts=requests.get(url_facts)
    soup_facts=bs(response_facts.text, "html.parser")
    tables = pd.read_html(url_facts)
    df=tables[0]
    df.columns=['description','value']
    html_table = df.to_html()
    df.to_html('table.html')


    #Visit the USGS Astrogeology site
    #to obtain high resolution images for each of Mar's hemispheres.
    url_hemispheres="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response_hemispheres=requests.get(url_hemispheres)
    soup_hemispheres=bs(response_hemispheres.text, "html.parser")
    results=soup_hemispheres.find_all('a', class_='itemLink product-item')
    hemisphere_image_urls=[]
    for result in results:
        title=result.h3.text
        url=result.img['src']
        full_url="https://astrogeology.usgs.gov"+url
        hemisphere_image_urls.append({"title":title, "img_url": full_url})
    


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls":hemisphere_image_urls
        }
    collection.insert_one(mars_data)
    

    # Return results
    return mars_data
