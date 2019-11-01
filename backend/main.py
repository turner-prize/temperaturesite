#web server which will accept a post request with a location, temp level, humidity level, light level and write it to a db
#page to view each of these on a graph. simple, charts.js or something.
#cronjob to run daily to check when the last log was.
from waitress import serve
import config

#app = Flask(__name__)
connex_app = config.connex_app
connex_app.add_api("swagger.yml")

if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=3000,debug=True)
    serve(connex_app,host='0.0.0.0',port=3000)
    
#export FLASK_APP=main.py
#flask run --host=0.0.0.0 --port=3000
