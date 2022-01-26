from random import randint
import time
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.secret_key = 'para guardar datos'

@app.route('/',methods=['GET'])
def panel_initial():
    if not('points' in session):
        session["points"] = 0
        session["activities"] = ""
        session["cont"] = 0
        session["game_over"] = 0
        session["message"] = ""
    return render_template("index.html")

@app.route('/process_money',methods=['POST'])
def process_money():
    value = request.form["building"]

    if value == "restart":
        session.clear()
    else:
        points = 0
        points = randint(int(request.form["value_min"]),int(request.form["value_max"]))

        if (randint(0,1) == 0 and int(request.form["flag_take"]) == 1):
            points *= -1
        
        date = time.strftime('%Y/%m/%d %H:%M%p', time.localtime())

        if points > 0:
            session["activities"] = "<p class='text_green'>earned "+str(points)+" golds from the "+value+" ("+date+")</p>" + session["activities"]
        elif points < 0:
            session["activities"] = "<p class='text_red'>Entered a "+value+" and lost "+str(points*-1)+" golds ... Ouch ... ("+date+")</p>" + session["activities"]
        else:
            session["activities"] = "<p class='text_gray'>I don't win gold ("+date+")</p>" + session["activities"]

        session["points"] += points
        if session["points"] < 0:
            session["points"] = 0
        session["cont"] += 1
        
        if session["points"] >= 500:
            session["game_over"] = 1
            session["message"] = "Has won the game"
        elif session["cont"] == 15:
            session["game_over"] = 1
            session["message"] = "Has lost the game"
        
        print(session["cont"])

    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)