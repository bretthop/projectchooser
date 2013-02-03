from google.appengine.ext import webapp

from app.services.VoteService import *

class AdminController(webapp.RequestHandler):

    _voteService   = VoteService()
    _backerService = BackerService()

    def post(self):
        try :
            action = self.request.get('action')

            if action == 'ADD_USER':
                email       = self.request.get('email')
                username    = self.request.get('username')
                password    = self.request.get('password')

                self._backerService.CreateBacker(email, username, password)

                self.response.out.write('Done!')
            else:
                self.response.out.write('No Action!')
        except BaseException as e:
            self.response.write(str(e))
    def get(self):
        try:
            action = self.request.get('action')

            if action == 'addVoteTypes':
                self._voteService.PopulateVoteTypes()

            elif action == 'clear':
                self.clearDatabase()

            elif action == 'resetToStable':
                self.clearDatabase()
                self._voteService.PopulateVoteTypes()

            self.response.out.write('Done!')
        except BaseException as e:
            self.response.write(str(e))

    def clearDatabase(self):
        '''
        Note: This doesn't seem a great way to do this, however this is apparently one of the recommended ways.
        See:
        https://groups.google.com/forum/?fromgroups=#!topic/google-appengine/7AgAo8qS_mk
        http://stackoverflow.com/questions/108822/delete-all-data-for-a-kind-in-google-app-engine
        '''
        kinds = ['Domain', 'Proposal', 'Vote', 'VoteType', 'Backer', 'BackerVote']

        for kind in kinds:
            while True:
                q = db.GqlQuery("SELECT __key__ FROM " + kind)

                if q.count() <= 0:
                    break

                db.delete(q.fetch(200))