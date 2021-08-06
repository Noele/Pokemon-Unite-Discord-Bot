from flask import Flask, render_template, redirect
from flask import request
import secrets
import os
import json
from urllib.parse import unquote

app = Flask(__name__)


@app.route('/createuser')
def createuser():
    username = request.args.get('username')
    profilepicture = unquote(request.args.get('profilepicture'))
    discriminator = request.args.get('discriminator')
    bottoken = request.args.get('bottoken')
    userid = request.args.get('userid')

    if bottoken != "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ":
        return
    if not os.path.isfile(f"data/{userid}.json"):
        with open(f"data/{userid}.json", "a") as f:
            f.write('{"user_id": "' + userid + '", "token": "' + secrets.token_hex(16) + '", "profilepicture": "' +
                    profilepicture + '", "discriminator": "' + discriminator + '", "username": "' + username + '"'
                       ', "trainerid": "", "favouritepokemon": "", "playstoplane": false, "playsjungle": false, '
                       '"playsbotlane": false, "biography": "", "rank": "", "level": 0}')
    else:
        return render_template('page.html'), 409

    return render_template('page.html'), 201


@app.route('/dashboard')
def dashboard():
    profilepicture = ""
    if not os.path.isfile(f'data/{request.args.get("userid")}.json'):
        return render_template("invalidlogin.html"), 404
    with open(f'data/{request.args.get("userid")}.json') as json_file:
        data = json.load(json_file)
        if request.args.get('token') != data["token"]:
            return render_template("invalidlogin.html"), 404
        profilepicture = data["profilepicture"]
        trainerid = data["trainerid"]
        level = data["level"]
        favouritepokemon = data["favouritepokemon"]
        rank = data["rank"]
        playstoplane = data["playstoplane"]
        playsbotlane = data["playsbotlane"]
        playsjungle = data["playsjungle"]
        biography = data["biography"]

    return render_template("dashboard.html",
                           profilepicture=profilepicture,
                           trainerid=trainerid,
                           level=level,
                           favouritepokemon=favouritepokemon,
                           rank=rank,
                           playstoplane=playstoplane,
                           playsbotlane=playsbotlane,
                           playsjungle=playsjungle,
                           biography=biography), 201


@app.route('/getuser')
def getuser():
    bottoken = request.args.get('bottoken')
    if bottoken != "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ":
        return
    with open(f'data/{request.args.get("userid")}.json') as json_file:
        data = json.load(json_file)
        payload = data
    return payload


@app.route('/submit')
def submit():
    trainerid = request.args.get('trainerid')
    favouritepokemon = request.args.get('favouritepokemon')
    playstoplane = request.args.get('playstoplane')
    playsjungle = request.args.get('playsjungle')
    playsbotlane = request.args.get('playsbotlane')
    biography = request.args.get('bio')
    userid = request.args.get('userid')
    rank = request.args.get('rank')
    level = request.args.get('level')

    data = ""
    with open(f"data/{userid}.json", 'r') as f:
        data = json.load(f)
        data["trainerid"] = trainerid
        data["favouritepokemon"] = favouritepokemon
        data["playstoplane"] = True if playstoplane == "on" else False
        data["playsjungle"] = True if playsjungle == "on" else False
        data["playsbotlane"] = True if playsbotlane == "on" else False
        data["biography"] = biography
        data["rank"] = rank
        data["level"] = int(level)
    with open(f"data/{userid}.json", 'w') as f:
        json.dump(data, f)

    return render_template("thankyou.html"), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
