from app import app
from flask import render_template
from aunty_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
@app.route('/<path:path>')
def home(path=None):
    return render_template('index.html')

@app.route("/manifest.json")
def manifest():
    return app.send_static_file("build/manifest.json")

@app.route("/service-worker.js")
def service():
    return app.send_static_file("build/service-worker.js")

@app.route("/precache-manifest.4ce3c1861f06c49a5377ecf892738541.js")
def precache():
    return app.send_static_file("build/precache-manifest.4ce3c1861f06c49a5377ecf892738541.js")

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
