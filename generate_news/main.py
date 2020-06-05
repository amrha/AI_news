import json
import logging
import pymongo
from simpletransformers.language_generation import LanguageGenerationModel
import requests
def good(ch):
  if "<|endoftext|>" not in ch:
    return (False)
  for i in range(20):
    if ch[-i:]==ch[-2*i:-i]:
      return(False)
  return(True)
url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=3e8a3411185c4a1390e349eeb775fa7f')
response = requests.get(url)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)
args={}
args["length"]=1000
args["use_cuda"]=True
myclient = pymongo.MongoClient("mongodb+srv://amrou:23856415@cluster0-k8dcj.gcp.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["test"]
mycol = mydb["news"]
for count in (response.json())["articles"]:
  content=count["description"]
  title=count["title"]
  time=count["publishedAt"]
  url=count["urlToImage"]
  by=count["source"]["name"]
  if content==None or content=="":
    continue
  for i in range(10):
    try:
      model = LanguageGenerationModel("gpt2", "distilgpt2",use_cuda=True)
      c=model.generate(prompt=content,args=args)[0]
      print(len(c))
      if len(c)>1000 and good(c) and len(c)<2000:
        print(c)
        mydict = {'title':title,'content':c[:-13],'time':time,'by':by,'url':url}
        mycol.create_index([('title', pymongo.ASCENDING)], unique=True)
        x = mycol.insert_one(mydict)
        break
    except:
      pass
