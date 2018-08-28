from .app import app


# Tempory solution for running containerised server
def run_server():
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)
