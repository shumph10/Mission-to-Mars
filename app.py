#import dependencies
from flask import Flask, render_template, redirect, url_for
    #well use flask to render a template, redirecting to another url and creating a url
from flask_pymongo import PyMongo
    #us PyMongo to  interact with the mongo db
import scraping
    #use scraping we will convert from Jupyter to python

#set up flask
app = Flask(__name__)

#tell python how to connect to mongo using PyMongo
#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
    #first part tell python that our app will connect to mongo using a URI,
        #a Uniform Resource Identifier, similar to a URL
    #second part is the URI well use to connect the app to mongo
        #saying the app can reach mongo through the local host
            #server using port 27017 using the database named mars_app
mongo = PyMongo(app)

#Set up app routes
#need 2 routes, the main page, and one to scrape the new data using code weve written
    #use url/scrape to activate scraping code with flask
    #flask routes bind urls to functions

#def the route for the HTML page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
        #uses pymongo to find the mars collection in our db which we
        #will create when we convert out Jupyter scraping code to Python script
        #assigns the variable for that paths use later on
    return render_template("index.html", mars = mars)
        #index.html is a default HTML file that well use to display the info weve scrapped
        #tells flask to return the HTML template - well build the file leter 
        #mars=mars tell python to use the mars collection in mongo

#set up function for web scrapping
    #will scrape updated data when we push the button on the homepage
    #button will run the code when clicked
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
        #tells to look at the mars collection in the db
    mars_data = scraping.scrape_all()
        #scrape new data using our scraping.py script
        #function from the exported jupyter notebook
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    #.update_one(query_parameter, {"$set": data}, options)
        #update the db, but not if an identical record already exists
        #in the query_paramter can specify a field like news_title: "s"
            #will update a document with the matching description
            #leaving blank matches the first document in the collection
        #set:data - means the document wil be modified($set) with the data in question
        #upsert - True - tells mongo to create a new doc if one doesnt already exist
            #and new data will be saved even if we have already created a doc for it

    return redirect('/', code=302)
        #return a message when successful
        #redirects back to the main page so we can see our updated content

#tell flask to run

if __name__ =="__main__":
    app.run(port="8001", debug=True)




## code without notes
# from flask import Flask, render_template, redirect, url_for
# from flask_pymongo import PyMongo
# import scraping

# app = Flask(__name__)

# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

# @app.route("/")
# def index():
#    mars = mongo.db.mars.find_one()
#    return render_template("index.html", mars=mars)

# @app.route("/scrape")
# def scrape():
#    mars = mongo.db.mars
#    mars_data = scraping.scrape_all()
#    mars.update_one({}, {"$set":mars_data}, upsert=True)
#    return redirect('/', code=302)

# if __name__ == "__main__":
#    app.run(port="8001", debug=True)