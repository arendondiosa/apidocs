from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/colors/<palette>/', methods=['PUT'])
def colors(palette):
    """
    Getting a list of applications applying some filters and sort fields as params 
    ---
    responses:
      200:
        description: Applications from the query.
        example: { data: { "applications": [ { application_business": 4687, "application_number": "497083110106922", "cents_on_the_dollar": 0.0, "channel": "ISO", "client_id": 6,  }  ], "total_applications": 100 } }
        type: Json
    """
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)

app.run(debug=True)
