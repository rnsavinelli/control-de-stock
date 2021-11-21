from server import app
from server.configuration import configuration

app.run(
    host=configuration["server"]["host"],
    port=configuration["server"]["port"],
    debug=True,
)
