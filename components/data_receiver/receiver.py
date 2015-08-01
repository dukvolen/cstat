#!/bin/python
#------------------------------------------------
#  @brief       Service for receiving any data
#  @author      Andrew Simine
#  @copyright   Copyrighted by Andrew Simine
#
#------------------------------------------------
import json
import datetime
from components.data_receiver.report_dumper import ReportDumper

from flask import Flask, make_response, request, jsonify
from flask.ext.httpauth import HTTPBasicAuth

#------------------------------------------------
app = Flask(__name__)
auth = HTTPBasicAuth()

#------------------------------------------------
@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

#------------------------------------------------
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

#------------------------------------------------
@app.route('/cstat/api/v1.0/data', methods=['POST'])
#@auth.login_required
def save_report():
    print(dir(request))
    try:
        data = request.json
        print(json.dumps(data))
        data['datetime'] = datetime.datetime.now()

        rdumper = ReportDumper(data)
        if(not rdumper.dump_report()):
            print("Can't dump received report!")
            return jsonify({'status': "error:Can't save received data!"})
    except Exception as e:
        print('Error: {}'.format(e.args))
        return jsonify({'status': "error:Can't save received data!"})
    return jsonify({'status': 'ok'})

#------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

#------------------------------------------------
