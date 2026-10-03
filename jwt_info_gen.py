import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================================
# Configuration
# ============================================================

CREDIT = "sakib29z"

LOGIN_URL = "https://loginbp.ppmainecoonghj.com"

REGIONAL_CLIENTS = {
    "BD": "https://clientbp.ppmainecoonghj.com",
    "IND": "https://client.ind.freefiremobile.com",
    "BR": "https://client.us.freefiremobile.com",
    "NA": "https://client.us.freefiremobile.com",
    "US": "https://client.us.freefiremobile.com",
    "default": "https://clientbp.ppmainecoonghj.com",
}


# ============================================================
# Your own backend/provider goes here
# ============================================================

def generate_token_from_your_backend(uid, password):
    """
    Connect this function to an authentication service/API
    that you own or are authorized to use.

    It should return a dictionary containing the fields
    required by the response formatter.
    """

    # Example placeholder:
    #
    # return {
    #     "access_token": "...",
    #     "account_id": uid,
    #     "token": "..."
    # }

    raise NotImplementedError(
        "Connect your authorized authentication backend here."
    )


# ============================================================
# Response formatter
# ============================================================

def build_response(token_data):

    region = str(
        token_data.get("region", "BD")
    ).upper()

    server_url = REGIONAL_CLIENTS.get(
        region,
        REGIONAL_CLIENTS["default"]
    )

    account_id = token_data.get(
        "account_id"
    )

    try:
        account_id = int(account_id)
    except (TypeError, ValueError):
        pass

    return {
        "access_token": token_data.get(
            "access_token"
        ),

        "account_id": account_id,

        "login_url": LOGIN_URL,

        "platform_type_used": token_data.get(
            "platform_type_used",
            4
        ),

        "region": region,

        "server_url": token_data.get(
            "server_url",
            server_url
        ),

        "source": token_data.get(
            "source",
            "authorized-backend"
        ),

        "status": "success",

        "timestamp": int(
            time.time()
        ),

        "token": token_data.get(
            "token"
        )
    }


# ============================================================
# Home
# ============================================================

@app.route("/", methods=["GET"])
def index():

    return jsonify({
        "status": "online",
        "credit": CREDIT,
        "endpoint": "/token?uid=UID&password=PASSWORD"
    }), 200


# ============================================================
# Token endpoint
# ============================================================

@app.route(
    "/token",
    methods=["GET", "POST"]
)
def token_endpoint():

    # GET parameters
    uid = request.args.get("uid")
    password = request.args.get("password")

    # JSON body
    if request.is_json:

        body = request.get_json(
            silent=True
        ) or {}

        uid = uid or body.get("uid")
        password = password or body.get(
            "password"
        )

    if not uid or not password:

        return jsonify({
            "status": "error",
            "error": (
                "Both uid and password "
                "parameters are required"
            )
        }), 400

    try:

        token_data = (
            generate_token_from_your_backend(
                str(uid),
                str(password)
            )
        )

        if not isinstance(
            token_data,
            dict
        ):
            raise ValueError(
                "Backend returned invalid data"
            )

        response = build_response(
            token_data
        )

        return jsonify(response), 200

    except NotImplementedError as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 501

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": (
                "Token generation failed"
            )
        }), 500


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

এই server-এর response structure হবে:

{
  "access_token": "...",
  "account_id": 18221071938,
  "login_url": "https://loginbp.ppmainecoonghj.com",
  "platform_type_used": 4,
  "region": "BD",
  "server_url": "https://clientbp.ppmainecoonghj.com",
  "source": "authorized-backend",
  "status": "success",
  "timestamp": 1791048510,
  "token": "..."
}

এখানে "key"/"iv" intentionally response-এ রাখা হয়নি এবং backend-এর authentication secrets client-এর কাছে পাঠানো হচ্ছে না।
