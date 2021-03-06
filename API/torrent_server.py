import flask
import json
from flask import request
from flask import Response
from flask_cors import CORS
from waitress import serve
import requests
from datetime import datetime
import TorrentScraper as scraper

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/getTorrentsList', methods=['GET'])
def getTorrentsList():
  search_key = request.args.get('search_key')
  return Response(json.dumps({"torrents" : scraper.search1337x(search_key)}), mimetype='application/json')

@app.route('/getMagnet', methods=['GET'])
def getMagnet():
  url = request.args.get('link')
  return Response(json.dumps(scraper.get1337xTorrentData(url)), mimetype='application/json')  

@app.route('/getSites', methods=["GET"])
def getSites():
  sites = ["1337x", "ThePirateBay", "Ettvdl", "Rarbg"]
  return Response(json.dumps({"sites" : sites}), mimetype='application/json')

@app.route('/getTorrents', methods=["GET"])
def getTorrents():
  search_key = request.args.get("search_key")
  if(search_key is None or search_key == ""):
    return Response(json.dumps("Invalid Request"))
  site = request.args.get("site")
  try:
    if(site == "1337x"):
      return Response(json.dumps({"torrents" : scraper.search1337x(search_key)}), mimetype="application/json")
    elif(site == "ThePirateBay"):
      return Response(json.dumps({"torrents" : scraper.searchTPB(search_key)}), mimetype="application/json")
    elif(site == "Rarbg"):
      return Response(json.dumps({"torrents" : scraper.searchRarbg(search_key)}), mimetype="application/json")
    elif(site == "Ettvdl"):
      return Response(json.dumps({"torrents" : scraper.searchEttv(search_key)}), mimetype="application/json")
    else:
      return Response(json.dumps({"torrents" : scraper.search1337x(search_key)}), mimetype="application/json")
  except Exception as e:
    print(e)
    return Response(json.dumps("Invalid Request"))

@app.route('/getTorrentData', methods=["GET"])
def getTorrentData():
  link = request.args.get("link")
  if(link is None or link == ""):
    return Response(json.dumps("Invalid Request"))
  site = request.args.get("site")
  try:
    if(site == "1337x"):
      return Response(json.dumps(scraper.get1337xTorrentData(link)), mimetype="application/json")
    elif(site == "ThePirateBay"):
      return Response(json.dumps(scraper.getTPBTorrentData(link)), mimetype="application/json")
    elif(site == "Rarbg"):
      return Response(json.dumps(scraper.getRarbgTorrentData(link)), mimetype="application/json")
    elif(site == "Ettvdl"):
      return Response(json.dumps(scraper.getEttvTorrentData(link)), mimetype="application/json")
    else:
      return Response(json.dumps(scraper.get1337xTorrentData(link)), mimetype="application/json")
  except:
    return Response(json.dumps("Invalid Request"))

serve(app, host="0.0.0.0", port=50000)
