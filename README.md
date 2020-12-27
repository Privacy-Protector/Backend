# Backend
The Database has Situation, Tag, Whitelist, Request, these 4 classes. And there are 2 association tables connecting Situation-Tag, Situation-Whitelist.
Route information: https://privacy-protector-v2.herokuapp.com/

1. get_all_situations @app.route("/api/situations/")
2. get_all_stuations_tag @app.route("/api/situations/tag/<tag>/")
3. get_situation @app.route("/api/situation/<int:id>/")
4. create_tag @app.route("/api/tag/", methods=['POST'])
5. add_company_to_whitelist @app.route("/api/situations/whitelist/<int:id>/", methods=['POST'])
6. send_situation_request @app.route("/api/situations/send/", methods=['POST'])
7. get_situation_request @app.route("/api/request/<int:id>/", methods=['GET'])
8. receive_request @app.route("/api/users/receive/", methods=['POST'])
