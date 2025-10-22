import random
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # нужен для хранения сессий


@app.route("/")
def index():
    score = session.get("score", 0)
    message = session.pop("message", "")  # выводим 1 раз, потом убираем
    return render_template_string("""
    <html>
      <head>
        <title>Три карточки</title>
        <style>
          body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
          .cards { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }
          .card { width: 100px; height: 150px; background: #4CAF50; color: white;
                  display: flex; justify-content: center; align-items: center;
                  font-size: 24px; cursor: pointer; border-radius: 10px; }
          .score { font-size: 20px; margin-top: 20px; }
          .message { font-size: 22px; margin-top: 20px; font-weight: bold; }
          .success { color: green; }
          .fail { color: red; }
        </style>
      </head>
      <body>
        <h1>Игра "Три карточки"</h1>
        <p>Под какой картой спрятан мячик?</p>
        <div class="cards">
          <form method="post" action="{{ url_for('guess') }}">
            <input type="hidden" name="choice" value="1">
            <button class="card">1</button>
          </form>
          <form method="post" action="{{ url_for('guess') }}">
            <input type="hidden" name="choice" value="2">
            <button class="card">2</button>
          </form>
          <form method="post" action="{{ url_for('guess') }}">
            <input type="hidden" name="choice" value="3">
            <button class="card">3</button>
          </form>
        </div>
        {% if message %}
        <div class="message {{ 'success' if 'угадал' in message else 'fail' }}">
          {{ message }}
        </div>
        {% endif %}
        <div class="score">
          Текущий счёт: <b>{{ score }}</b>
        </div>
      </body>
    </html>
    """, score=score, message=message)


@app.route("/guess", methods=["POST"])
def guess():
    choice = int(request.form["choice"])
    ball = random.randint(1, 3)
    score = session.get("score", 0)

    if choice == ball:
        score += 1
        session["message"] = f"✅ Угадал! Мячик был под {ball}"
    else:
        score = max(0, score - 1)
        session["message"] = f"❌ Не угадал! Мячик был под {ball}"

    session["score"] = score
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

