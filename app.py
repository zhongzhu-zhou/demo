from flask import Flask, render_template,request,send_file,url_for,send_from_directory
from historical_visualization import displayvisulization
from getlatestdata import get_current_data
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Dailyupdate import daily_update
import os
app = Flask("__name__")


# The historical.csv needs to be updated on a daily basis. Daily_update method would check data and update database when necessary
def check_update():
    if 2 < int(datetime.datetime.utcnow().strftime("%H")) < 22:
        daily_update()
    
        
# Initiating the program. Scheduler will let the func check_update run every hour. 
app.config["CLIENT_IMAGES"] = os.getcwd()+"/download/"
scheduler = BackgroundScheduler()
scheduler.add_job(func = check_update,trigger="interval", hours = 1)
scheduler.start()


#This is the home page. GET method will return the initial layout of the page. POST method will post the form and redirect user to visulization page.
@app.route("/",methods = ["GET","POST"])
def hello():
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = get_current_data()
    return render_template('index.html', data=data,time = dt)

#This is the visualization page where graphs are displayed. Graph will first be generated through the method "displayvisualization" and graph is stored in download folder. Later "download" method will obtain graphs from download folder and pass it into the HTML page.
@app.route("/visualization",methods = ["GET","POST"])
def visualization():
    industry = request.form["industry"]
    metrics = request.form["metrics"]
    displayvisulization(industry, metrics)
    filename = 'historical-' + industry + '-' + metrics + '.png'
    return render_template("display.html",filename = filename)


#This is the method visualization page uses to obtain graphs from download folder.
@app.route("/download/<filename>")
def download(filename):
    print(app.config["CLIENT_IMAGES"])
    return send_from_directory(app.config["CLIENT_IMAGES"],filename = filename)


if __name__ == "__main__":
    app.run(debug = True)
