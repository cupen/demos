import json
from collections import OrderedDict

from flask import Flask, session, request, make_response
# from flaskext.sqlalchemy import SQLAlchemy
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import Session
import init_db

app = Flask(__name__)

app.debug = True
engine = init_db.create_testdb('test')
scheme = MetaData()
scheme.reflect(engine)

@app.route('/')
def hello_world():
    rs = {
        'schemes':[
            'test',
        ]
    }
    return json.dumps(rs)

@app.route('/<database>')
def database(database):
    if not database == 'test':
        return make_response('', 404)

    global scheme
    rs = OrderedDict()
    for t in scheme.sorted_tables:
        fields = []
        for col in t.columns:
            fields.append({
                'name': col.name,
                'type': str(col.type),
                'nullable': col.nullable,
                'primary': col.primary_key,
            })

        rs[t.name] = {
            'fields': fields,
            'indexs': [],
        }

    return json.dumps(rs)

@app.route('/<database>/<table>')
def table(database, table):
    global scheme
    if table not in scheme.tables:
        return make_response('', 404)

    t = scheme.tables[table]

    db = Session(engine)
    rs = []
    for row in db.query(t).all():
        rs.append({c.name: getattr(row, c.name) for c in t.columns})
        # rs.append(row.__dict__)
    return json.dumps(rs)

class CounterAPI(MethodView):

    def get(self):
        return session.get('counter', 0)

    def post(self):
        session['counter'] = session.get('counter', 0) + 1
        return 'OK'

app.add_url_rule('/counter', view_func=CounterAPI.as_view('counter'))

if __name__ == '__main__':
    app.run()