#!/usr/bin/env python
# coding: utf-8

import requests
import base64
import configparser
import json
import yaml
import datetime

Token_url = "https://libra.mdg.si.i.nagoya-u.ac.jp/oauth2/token"
Orion_url = "https://virgo.mdg.si.i.nagoya-u.ac.jp/v2/entities"

class mdgFiware:
  def __init__(self) -> None:
    with open('setting.yaml', 'r') as yml:
      map = yaml.safe_load(yml)
      self.id = map['entity']['id']
      self.type = map['entity']['type']
      self.service = map['entity']['service']
      self.servicepath = map['entity']['servicepath']
      self.keys = map['keys']
      self.client_id = map['config']['client']['id']
      self.client_secret = map['config']['client']['secret']
      self.attrs = map['attributes']

      self.token_url = Token_url
      self.orion_url = Orion_url


  def show_config(self) -> str:
    print("=== Config ===")
    print('id:\t\t', self.id)
    print('type:\t\t',self.type)
    print('service:\t',self.service)
    print('servicepath:\t',self.servicepath)
    print('token_url:\t',self.token_url)
    print('orion_url:\t',self.orion_url)


  def __getAuthToken(self) -> str:
    basic = base64.b64encode((self.client_id+":"+self.client_secret).encode())
    headers_map = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": "Basic " + basic.decode(),
      "Accept": "application/json"
    }
    try:
      res = requests.post(self.token_url, data="grant_type=client_credentials", headers=headers_map)
      res.raise_for_status()
    except Exception as e:
      raise
    else:
      return res.json()["access_token"]
    

  def sendData(self, raw, timestamp=None, console=True, debug=False) -> None:
    try: token = self.__getAuthToken()
    except Exception as e:
      print(e)
      print('トークンの取得中にエラーが発生しました。クライアントIDやクライアントシークレットを確認してください。')

    data = json.loads(raw)
    if timestamp == None:
      timestamp=datetime.datetime.utcnow()
    else:
      timestamp = timestamp[0:19]
      timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=-9)
    body = {
      'id': self.id, 'type': self.type,
    }
    body['dateObserved'] = {
      'type': 'DateTime',
      'value': timestamp.strftime('%Y-%m-%dT%H:%M:%S%Z'),
      'metadata': {}
    }
    if console: print("データをFIWAREに送信します...")
    try:
      for attr in self.attrs:
        context = {
          'value': data[attr['value']],
          'type': attr['type']
        }
        body[attr['name']] = context
    except Exception as e:
      print(e)
      print('JSONのパース中にエラーが発生しました。設定ファイルの内容と引数のJSONの対応などを再確認してください。')  
    
    try:
      headers_map = {
        "Content-Type": "application/json",
        "X-Auth-Token": token,
        "Accept": "application/json",
        "fiware-service": self.service,
        "fiware-servicepath": self.servicepath
      }
      params_map = {
        "options": "upsert"
      }
      body = json.dumps(body)
      res = requests.post(self.orion_url, data=body, headers=headers_map, params=params_map)
      res.raise_for_status()
    except Exception as e:
      print(e)
      print('FIWAREへのデータの送信中にエラーが発生しました。')
    else:
      if console: print("成功しました。")
      if debug: print(body)
      return res.status_code


  def displayData(self, console=True) -> None:
    token = self.__getAuthToken()
    if console: print("データをFIWAREから取得します...")
    try:
      headers_map = {
        "X-Auth-Token": token,
        "fiware-service": self.service,
        "fiware-servicepath": self.servicepath
      }
      res = requests.get(self.orion_url, headers=headers_map)
      res.raise_for_status()
    except Exception as e:
      print(e)
      print('FIWAREからデータの取得中にエラーが発生しました。')
    else:
      if console: print("成功しました。データを表示します。")
      print(json.dumps(res.json(), indent=2))


if __name__ == '__main__':
  a = mdgFiware()
  a.show_config()