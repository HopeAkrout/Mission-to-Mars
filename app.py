# import dependancies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# set up Flask
app = Flask(__name__)


# connect to Mongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# set up Flask routes
# home page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   print(mars)
   return render_template("index.html", mars=mars, hemisphere_length=len(mars["hemisphere_images"]))

# scrape route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   print("before update")
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   print("after update")
   return redirect('/', code=302)

# run
if __name__ == "__main__":
   app.run()