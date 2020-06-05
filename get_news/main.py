from flask import Flask,jsonify
from flask import Blueprint
from flask_pymongo import PyMongo
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
cors=CORS(app,resources={r"/*":{"origins":"*"}})
app.config["MONGO_URI"]="your mongo uri"
app.config['MONGO_DBNAME'] = 'news'
mongo=PyMongo(app)
@app.route('/')
def index():
	news = mongo.db.news 
	result = []
	for field in news.find():
		result.append({'title':field['title'],'content':field['content'],'time':field['time'],'by':field['by'],'url':field['url']})
	return jsonify(result)
if __name__=='__main__':
	app.run(debug=True)
