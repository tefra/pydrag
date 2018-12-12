from flask import Flask, redirect, render_template, request, url_for
from pydrag import AuthSession, AuthToken, Config, configure

app = Flask(__name__)


tokens = {}  # type: ignore


@app.route("/")
def index():
    show_config = Config.instance().api_key == ""
    return render_template(
        "index.html", tokens=tokens, show_config=show_config
    )


@app.route("/configure", methods=["POST"])
def config():
    configure(
        api_key=request.form.get("api_key"),
        api_secret=request.form.get("api_secret"),
        username=request.form.get("username"),
        password=request.form.get("password"),
    )
    return redirect(url_for("index"))


@app.route("/gen-token")
def gen_token():
    global tokens

    token = AuthToken.generate()
    tokens.update({token.token: None})
    return redirect(url_for("index"))


@app.route("/authorize/<token>", methods=["GET"])
def authorize_token(token):
    global tokens
    tokens[token] = True
    token = AuthToken(token=token)
    return redirect(token.auth_url)


@app.route("/get-session/<token>", methods=["GET"])
def get_session(token):
    global tokens
    session = AuthSession.from_token(token)
    tokens[token] = session
    return redirect(url_for("index"))


@app.route("/session", methods=["POST", "GET"])
def gen_session():
    if request.method == "POST":
        url = "http://www.last.fm/api/auth/?api_key={}&cb={}".format(
            Config.instance().api_key, url_for("gen_session", _external=True)
        )
        return redirect(url)
    else:
        token = request.args.get("token")
        return redirect(url_for("get_session", token=token))
