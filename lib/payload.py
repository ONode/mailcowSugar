from flask import Flask, jsonify
from flask import request

from lib.com.u1 import NameUtil, readconf
from lib.const import LocalConf, Errors, logger_swagger_mail

app = Flask(__name__)

import http.client
import json

conn = http.client.HTTPSConnection(LocalConf.API_HOST)

headers = {
    'X-API-Key': LocalConf.API_KEY,
    'Content-Type': 'application/json'
}
NameUtil.init_dict()
config = readconf(
    file_name="resources.json",
    required_values=['api_key', 'api_host', 'temp_pass']
)
LocalConf.API_KEY = config['api_key']
LocalConf.API_HOST = config['api_host']
LocalConf.TEMP_EMAIL_AC_PASS = config['temp_pass']


# Define a simple endpoint to return a JSON object
@app.route('/api')
def hello():
    return jsonify({'message': 'Hello this is temp email api'})


# Define an endpoint to return a list of users
@app.route('/api/v1/users')
def get_users():
    users = {
        'total': 9999,
        'newusers_by_24h': 30
    }
    return jsonify(users)


# Define an endpoint to return a user by ID
@app.route('/api/v1/users/<int:user_id>')
def get_user(user_id):
    user = {'id': user_id, 'name': 'User {}'.format(user_id)}
    return jsonify(user)


@app.route('/api/v1/mail/create_mail_box', methods=['POST'])
def append_new_mail_box():
    user_data = request.get_json()
    email_specification = user_data.get("email")
    if "@" not in email_specification:
        return jsonify(Errors.INVALID_EMAIL)
    email_part = email_specification.split("@")
    payload = json.dumps({
        "local_part": email_part[0],
        "domain": email_part[1],
        "name": NameUtil.get_ethname(True),
        "quota": "1024",
        "password": LocalConf.TEMP_EMAIL_AC_PASS,
        "password2": LocalConf.TEMP_EMAIL_AC_PASS,
        "active": "1",
        "force_pw_update": "0",
        "tls_enforce_in": "0",
        "tls_enforce_out": "0"
    })
    conn.request("POST", "/api/v1/add/mailbox", payload, headers)
    res = conn.getresponse()
    data = res.read()
    ok = json.loads(data)
    if isinstance(ok, list):
        for action in ok:
            if action.get("type") == "success":
                email_dat = action.get("log")
                if len(email_dat) >= 4:
                    dat_ = email_dat[3]
                    base = Errors.SUCCESS_ACTION
                    if "name" in dat_:
                        # name = dat_.get("name")
                        base.update(dat_)
                        return jsonify(base)

            if action.get("type") == "danger":
                logger_swagger_mail.info("failed to create new email")
                return jsonify(Errors.EXISTING_EMAIL)

    return jsonify(Errors.UNKNOWN_ERR)


@app.route('/api/v1/mail/check_exist/<str:full_email>')
def exist_email(full_email: str):
    if "@" not in full_email:
        return jsonify(Errors.INVALID_EMAIL)
    p = full_email.split("@")

    user = {'id': p[0], 'domain': p[1]}
    return jsonify(user)


@app.route('/api/v1/getMessages/<str:user_id>/<str:domain>')
def get_messages(user_id: str, domain: str):
    user = {'id': user_id, 'name': 'User {}'.format(user_id)}
    return jsonify(user)


@app.route('/api/v1/getFullMessage/<str:user_id>/<str:domain>/<int:mail_id>')
def get_full_messages(user_id: str, domain: str, mail_id: int):
    user = {'id': user_id, 'name': 'User {}'.format(user_id)}
    return jsonify(user)
