from flask import Flask, render_template,request,send_file,url_for,send_from_directory
from historical_visualization import displayvisulization
from getlatestdata import get_current_data
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Dailyupdate import daily_update
import os
app = Flask("__name__")

def check_update():
    if 2 < int(datetime.datetime.utcnow().strftime("%H")) < 22:
        daily_update()
app.config["CLIENT_IMAGES"] = os.getcwd()+"/download/"
scheduler = BackgroundScheduler()
scheduler.add_job(func = check_update,trigger="interval", hours = 1)
scheduler.start()


@app.route("/",methods = ["GET","POST"])
def hello():
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = get_current_data()
    return render_template('index.html', data=data,time = dt)


@app.route("/visualization",methods = ["GET","POST"])
def visualization():
    industry = request.form["industry"]
    metrics = request.form["metrics"]
    displayvisulization(industry, metrics)
    filename = 'historical-' + industry + '-' + metrics + '.png'
    return render_template("display.html",filename = filename)



@app.route("/download/<filename>")
def download(filename):
    print(app.config["CLIENT_IMAGES"])
    return send_from_directory(app.config["CLIENT_IMAGES"],filename = filename)


if __name__ == "__main__":
    app.run(debug = True)
