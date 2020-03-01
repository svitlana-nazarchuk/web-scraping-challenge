from flask import Flask, render_template
import pymongo
from scrape_mars import scrape
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db=client.mars
collection = db.mars_data


@app.route('/')
def index():
    
    scrape()
    data=list(db.mars_data.find())
    #print(data[0])
    

    return render_template("index.html", mars_data=data[0])

@app.route('/scrape')
def scraped_page():

    scrape()
    data=list(db.mars_data.find())
    length=len(data)
    
    return render_template("index.html", mars_data=data[length-1])    

if __name__ == "__main__":
    app.run(debug=True)





