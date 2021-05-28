from types import MethodDescriptorType
from flask import Flask , render_template
from data import Articles

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('home.html' , name = "이동현")

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/articles',methods=['GET','POST'])
def articles():
    articles = Articles()
    return render_template('articles.html', articles = articles)


if __name__ == '__main__':
    app.run()