import mimetypes
from boto.s3.key import Key
from boto.s3.prefix import Prefix
from flask import Blueprint
from flask import abort, render_template, request, send_file
from flask import current_app as app
from pooldcode.auth import requires_auth

plan = Blueprint('pypi', __name__)


def get_list(key=None):
    key = (key or '').lstrip('/')
    prefixes = []
    keys = []

    for item in app.bucket.list(prefix=key or None, delimiter='/'):
        if item.name == key:
            continue
        if isinstance(item, Prefix):
            prefixes.append(item)
        else:
            keys.append(item)

    prefixes = sorted(prefixes, key=lambda i: i.name)
    keys = sorted(keys, key=lambda i: i.name)
    return prefixes + keys


def render_key(key=None, raise_404=True):
    items = get_list(key=key)

    if raise_404 and len(items) < 1:
        abort(404)

    return render_template('pypi.html', key=key, items=items)


def render_resource(key):
    key = Key(bucket=app.bucket, name=key)

    if not key.exists():
        abort(404)

    name = key.name.strip('/').split('/')[-1]
    key.open()
    key.name = None
    return send_file(key,
                     mimetype=key.content_type,
                     attachment_filename=name,
                     as_attachment=True)


@plan.route('/', methods=['GET'])
@requires_auth
def bucket():
    return render_key(raise_404=False)


@plan.route('/<path:key>')
@requires_auth
def key(key):
    if not key or request.path.endswith('/'):
        key = '/%s/' % key.strip('/')
        return render_key(key=key)
    return render_resource(key)


@plan.route('/', methods=['POST'])
def submit():
    if len(request.files) < 1:
        return 'OK'

    name = request.form.get('name')

    if not name:
        abort(405)

    root = '%s/' % name

    for key in request.files:
        file = request.files[key]
        key = '%s%s' % (root, file.filename)
        key = Key(bucket=app.bucket, name=key)
        size = file.content_length
        headers = None

        (mimetype, encoding) = mimetypes.guess_type(file.filename)

        if encoding == 'gzip':
            mimetype = 'application/x-gzip'

        if mimetype:
            headers = {
                'Content-Type': mimetype
            }

        key.set_contents_from_file(file.stream, size=size, headers=headers)
        file.close()
        key.close()

    return 'OK'
