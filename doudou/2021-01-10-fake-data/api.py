from flask import Flask, jsonify, request
from mimesis.schema import Field, Schema
from mimesis.enums import Gender

app = Flask(__name__)

_ = Field('zh')
schema = Schema(schema=lambda: {
    'id': _('uuid'),
    'name': _('person.name'),
    'version': _('version', pre_release=True),
    'timestamp': _('timestamp', posix=False),
    'owner': {
        'email': _('person.email', domains=['test.com'], key=str.lower),
        'token': _('token_hex'),
        'creator': _('full_name', gender=Gender.FEMALE)
    },
    'address': {
        'country': _('address.country'),
        'province': _('address.province'),
        'city': _('address.city')
    }
})


@app.route('/apps', methods=('GET',))
def apps_view():
    count = request.args.get('count', default=1, type=int)
    data = schema.create(iterations=count)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5200, debug=True)
