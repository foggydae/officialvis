from flask import Flask, request, render_template
# from Utils.EntityModel import EntityModel
import json

app = Flask(__name__)
cur_file_name = ""

@app.route("/", methods=['GET'])
def Index():
    return render_template("main.html")


# @app.route("/api/load_file", methods=["POST", "GET"])
# def load_file():
#     if request.method == 'POST':
#         global entity_model, cur_file_name
#         entity_model = EntityModel(verbose=False)
#         file = request.files["myfile"]
#         entity_model.upload(file)
#         cur_file_name = file.filename
#     return render_template("dashboard.html", filename=cur_file_name)


# @app.route("/api/get_hierarchy_data/<message>", methods=["GET"])
# def get_hierarchy_data(message):
#     message_dict = json.loads(message)
#     ignore_branches = message_dict["ignore_branches"]
#     try:
#         return json.dumps(entity_model.get_json_tree(ignore_branches=ignore_branches))
#     except:
#         print("hierarchy fail")
#         return "NO_DATA"


# @app.route("/api/get_map_data/<message>", methods=["GET"])
# def get_map_data(message):
#     message_dict = json.loads(message)
#     duns = message_dict['select_entity']
#     try:
#         return json.dumps(entity_model.get_gps(duns))
#     except:
#         print("map fail")
#         return "NO_DATA"


# @app.route("/api/get_summary_data", methods=["GET"])
# def get_summary_data():
#     try:
#         count_dict = entity_model.get_data_stats(verbose=False)
#         pnid_list = entity_model.get_pnid_list()
#         global_ultimate_list = entity_model.get_global_ultimates()
#         metadata_list = entity_model.get_metadata()
#         result = {
#             "count_dict": count_dict,
#             "pnid_list": pnid_list,
#             "global_ultimate_list": global_ultimate_list,
#             "metadata_list": metadata_list,
#             "filename": cur_file_name
#         }
#         return json.dumps(result)
#     except:
#         return "NO_DATA"


# @app.route("/api/get_SIC_sibling/<message>", methods=["GET"])
# def get_SIC_sibling(message):
#     message_dict = json.loads(message)
#     selected_duns = message_dict["selected_duns"]
#     digits = message_dict["digits"] # 2
#     logic = message_dict["logic"] # 'OR'
#     max_num = message_dict["max_num"] # 10
#     try:
#         return json.dumps(entity_model.find_siblings(selected_duns, digits=digits, logic=logic, max_num=max_num))
#     except:
#         print("siblings fail")
#         return "NO_DATA"


# @app.route("/api/get_stat_data", methods=["GET"])
# def get_stat_data():
#     try:
#         result = entity_model.get_data_stats(verbose=False)
#         result["filename"] = cur_file_name
#         return json.dumps(result)
#     except:
#         return "NO_DATA"


# @app.route("/api/get_LOB_list", methods=["GET"])
# def get_LOB_list():
#     try:
#         return json.dumps(entity_model.get_lob_list())
#     except:
#         return "NO_DATA"


# @app.route("/api/filter/<message>", methods=["GET"])
# def filter(message):
#     message_dict = json.loads(message)
#     keyword = message_dict["keyword"]
#     lob = message_dict["lob"]
#     try:
#         return json.dumps(entity_model.filter_entity(keyword, lob))
#     except:
#         return "NO_DATA"


# @app.route("/api/recommend/<message>", methods=["GET"])
# def recommend(message):
#     message_dict = json.loads(message)
#     print("recommend")
#     print(message_dict)
#     selected_duns = message_dict["selected_duns"]
#     weights = message_dict["weights"]
#     digits = message_dict["digits"]
#     logic = message_dict["logic"]
#     # try:
#     return json.dumps(entity_model.similarity_score(selected_duns, weights=weights, digits=digits, logic=logic))
#     # except:
#     #     return "NO_DATA"


if __name__ == "__main__":
    app.run(debug=True)
