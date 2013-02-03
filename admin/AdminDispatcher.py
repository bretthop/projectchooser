from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from admin.AdminController import AdminController

def main():
    app = webapp.WSGIApplication(
        [
            ('/doAdminAction', AdminController)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()