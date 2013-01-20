from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from app.resources.ProposalResource import *
from app.resources.VoteResource import *
from app.resources.WithdrawResource import *

# TODO: Using a static index.html file to replace the '/' url mapping
# TODO: Replace '/vote' URL mapping with API mapping in 'APIDispatcher.py'
def main():
    app = webapp.WSGIApplication(
        [
            ('/', ProposalResource),
            ('/vote', VoteResource),
            ('/withdraw', WithdrawResource)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()