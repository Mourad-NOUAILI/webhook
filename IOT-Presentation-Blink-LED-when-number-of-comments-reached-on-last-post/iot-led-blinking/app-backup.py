from flask import Flask, redirect, url_for, request, make_response, render_template
import sys

import dpath.util

from flask_sqlalchemy import SQLAlchemy

class colors:
    GREEN = "\u001b[32m"
    RESET = "\u001b[0m"
    RED = "\u001b[31m"
    YELLOW = "\u001b[33m"
    BOLD = "\u001b[1m"

response = "mmezmemezez"

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'live'
#app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///led_blink_comments.db'

db = SQLAlchemy(app)



class Posts(db.Model):
    id = db.Column(db.String, primary_key=True)
    counter = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"Posts('{self.id}', '{self.counter}')"

# https://developers.facebook.com/docs/graph-api/webhooks/
@app.route('/', methods=['GET'])
def verify_webhook():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == 'incoming-comment':
            return "not ok", 403
        return request.args.get('hub.challenge'), 200
    return 'Ok', 200

@app.route('/', methods=['POST'])
def get_data():
    global response


    data = request.get_json()



    value = dpath.util.search(data, '/entry/0/changes/0')
    if len(value) > 0:
        print(data)
        value = dpath.util.get(data, '/entry/0/changes/0/value')
        post_id = value['post_id']
        item = value['item']
        m = dpath.util.search(data, '/entry/0/changes/0/value/message')
        comment=''
        if len(m) > 0:
            comment = value['message']
        verb = value['verb']

        # Keep only the last post on the database.
        if (item == 'status' or item ==  'photo') and verb == 'add':
            rows = db.session.query(Posts).count()
            if rows > 0:
                Posts.query.delete()
                db.session.commit()

            post = Posts(id=post_id, counter=0)
            db.session.add(post)
            db.session.commit()
            print(colors.BOLD + colors.GREEN + '---->>>>>>>>>>' +post_id +" with message " + comment + " added.----<<<<<<<<<<<<<<<<" + colors.RESET)
            response = '0'


        if item == 'comment' and verb == 'add':
            post = Posts.query.filter_by(id=post_id).first()
            if post:
                post.counter += 1
                db.session.commit()
                print(colors.BOLD + colors.GREEN + "---->>>>>>>>>># of commants of post("+post_id+"): "+str(post.counter) +'----<<<<<<<<<<<<<<<<' + colors.RESET)
                if post.counter == 5:
                    response = '1'

        if item == 'post' and verb == 'remove':
            post = Posts.query.filter_by(id=post_id).first()
            if post:
                Posts.query.filter_by(id=post_id).delete()
                db.session.commit()
                print(colors.BOLD + colors.GREEN + '---->>>>>>>>>>' +post_id +" with message deleted.----<<<<<<<<<<<<<<<<" + colors.RESET)
                response = '0'






    print(colors.BOLD + colors.GREEN + "///////////////////Notification to send to the client: "+str(response)+"///////////////////\n" + colors.RESET)
    return response, 200


if __name__ == '__main__':
    app.run(debug=False, port=8000)
