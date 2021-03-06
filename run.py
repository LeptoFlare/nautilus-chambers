"""Run nautilus."""
from nautilus import app, utils


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=utils.env.get('debug')
    )
