from flask import Flask
from blog import bp as blogbp
from auth import bp as authbp

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='jhsgdyagdbwuskauia54fajfiah')



app.register_blueprint(blogbp)
app.register_blueprint(authbp)
app.add_url_rule('/',endpoint='blog.index')




if __name__ == "__main__":
    app.run(debug=True)
