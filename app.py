from flask import Flask , render_template

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('home.html' , name = "이동현")


if __name__ == '__main__':
    app.run()