from flask import Flask
from flask import request
from threading import Thread
from termcolor import colored
import requests
import json
import inspect

app = Flask('')
headBody = "<!DOCTYPE html><html lang='en'><head>  <title>Bootstrap Example</title>  <meta charset='utf-8'>  <meta name='viewport' content='width=device-width, initial-scale=1'>  <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>  <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>  <script src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js'></script>  <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'></script></head><style>* {  box-sizing: border-box;}body {  margin: 0;  font-family: Arial;} .header {  text-align: center;  padding: 32px;}.row {  display: -ms-flexbox; /* IE10 */  display: flex;  -ms-flex-wrap: wrap; /* IE10 */  flex-wrap: wrap;  padding: 0 4px;}/* Create four equal columns that sits next to each other */.column {  -ms-flex: 25%; /* IE10 */  flex: 25%;  max-width: 25%;  padding: 0 4px;}.column img {  margin-top: 8px;  vertical-align: middle;  width: 100%;}/* Responsive layout - makes a two column-layout instead of four columns */@media screen and (max-width: 800px) {  .column {    -ms-flex: 50%;    flex: 50%;    max-width: 50%;  }}/* Responsive layout - makes the two columns stack on top of each other instead of next to each other */@media screen and (max-width: 600px) {  .column {    -ms-flex: 100%;    flex: 100%;    max-width: 100%;  }}</style><body>"
endBody = "</body></html>"



def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()