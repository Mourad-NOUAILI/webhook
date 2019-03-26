from flask import Flask, redirect, url_for, request
import sys

import dpath.util

from flask_sqlalchemy import SQLAlchemy


import asyncio
from aiohttp import web
import socketio


SECRET_KEY = 'live'
DEBUG = True

sio = socketio.AsyncServer(async_mode='aiohttp')
app1 = web.Application()
sio.attach(app1)

##########
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
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
    data = request.get_json()
    print(data)
    sys.stdout.flush()

    sio.emit('send_data',  {'data': "mmmmmmmmmmmmmmmmmmmm."})

    '''value = dpath.util.search(data, '/entry/0/changes/0')
    if len(value) > 0:
        value = dpath.util.get(data, '/entry/0/changes/0/value')
        post_id = value['post_id']
        item = value['item']
        m = dpath.util.search(data, '/entry/0/changes/0/value/message')
        comment=''
        if len(m) > 0:
            comment = value['message']
        verb = value['verb']
        rows = db.session.query(Posts).count()
        if rows == 0 and item == 'status' and verb == 'add':
            post = Posts(id=post_id, counter=0)
            db.session.add(post)
            db.session.commit()
            print(post_id +" with message " + comment + " added.")
        if item == 'comment' and verb == 'add':
            post = Posts.query.filter_by(id=post_id).first()
            if post:
                post.counter += 1
                db.session.commit()
                print("//////////////////////////////////////////"+str(post.counter))
                if post.counter == 5:
                    print('ok')

        if item == 'post' and verb == 'remove':
            post = Posts.query.filter_by(id=post_id).first()
            if post:
                Posts.query.filter_by(id=post_id).delete()
                db.session.commit()

                print(post_id +" with message " + comment + " deleted.")'''



    return 'ok', 200

async def start_server():
    await sio.connect('http://localhost:8000')
    await sio.emit('run_server',  {'data': "Server is on."})
    app.run(debug=True, port=8000)
    await sio.wait()


if __name__ == '__main__':
    loop.run_until_complete(start_server())
