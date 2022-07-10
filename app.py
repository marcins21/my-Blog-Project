import datetime
from time import strftime
from flask import Flask
from flask import render_template,request
from pymongo import MongoClient

#Flask app factory
#def create_app():


app = Flask(__name__)
#Client
client = MongoClient("mongodb+srv://msitko21:<password>@microblog-ap.d4dha.mongodb.net/test")
#Database microblog
app.db = client.microblog

entries = []
entries_with_date = []

#Home Route
@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
        
        #inserting data in MongoDB
        app.db.entries.insert_one({"content":entry_content,"date":formatted_date})

    #app.db.entries Construction ('content':'Moj tekst', 'date':'data')
    entries_with_date = [
    (
        entry["content"],                                                  # Creating list from dictionary taken from MongoDB
        entry["date"],
        datetime.datetime.strptime(entry["date"], '%Y-%m-%d').strftime("%b %d") #Date-Formating  ---- Formatowanie Daty
    )
    for entry in app.db.entries.find({})
]
    return render_template("home.html",entries = entries_with_date)


if __name__ == "__main__":
    app.run(debug=True)

    #Flask app Factory 
    #return app
