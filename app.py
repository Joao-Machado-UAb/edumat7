# app.py

from flask import Flask, jsonify, request, render_template
from activity_facade import ActivityFacade

app = Flask(__name__)

# Instância única do ActivityFacade
activity_facade = ActivityFacade()

# Página de inicial
@app.route("/")
def index():
    return render_template("index.html")


# Página de configuração da atividade e parâmetros respetivos
@app.route("/config", methods=["GET"])
def config():
    return render_template("config.html")


# parametros json
@app.route("/json_params", methods=["GET"])
def json_params():
    return jsonify([
        {"name": "resumo", "type": "text/plain"},
        {"name": "instrucoes", "type": "text/plain"},
    ])


# Lista de analytics da atividade
@app.route("/analytics_list", methods=["GET"])
def analytics_list():
    return jsonify(activity_facade.get_analytics_list())


# Deploy da atividade - Primeira Etapa
@app.route("/user_url", methods=["GET"])
def user_url():
    activity_id = request.args.get("activityID")
    activity_facade.create_activity(activity_id)
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}"})


# Deploy da atividade - Segunda Etapa
@app.route("/deploy", methods=["POST"])
def deploy():
    data = request.get_json()
    activity_id = data.get("activityID")
    student_id = data.get("Inven!RAstdID")
    json_params = data.get("json_params")
    resumo = json_params.get("resumo", "")
    instrucoes = json_params.get("instrucoes", "")
    activity_facade.update_activity(activity_id, resumo, instrucoes)
    return jsonify({
        "url": f"https://edumat.onrender.com/atividade?id={activity_id}&student_id={student_id}"
    })


@app.route("/analytics", methods=["GET"])
def analytics():
    analytics_data = activity_facade.get_analytics_data()
    return render_template("analytics.html", analytics_data=analytics_data)


# atividade equações
@app.route("/equacoes", methods=["GET"])
def equacoes():
    activity_id = request.args.get("activityID")
    data = activity_facade.access_activity_data(activity_id)
    if data:
        resumo = data.get("resumo", "")
        instrucoes = data.get("instrucoes", "")
    else:
        resumo = "Resumo de equações de 7º ano: Aqui você pode encontrar um resumo das equações de 7º ano."
        instrucoes = "https://www.matematica.pt/aulas-exercicios.php?id=190"
    return render_template("equacoes.html", resumo=resumo, instrucoes=instrucoes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
