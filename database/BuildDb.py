from google.appengine.ext import webapp

from app.services.VoteService import *

class BuildDb(webapp.RequestHandler):

    _voteService = VoteService()

    def get(self):
        action = self.request.get('action')

        try:
            if action == 'addVoteTypes':
                self._voteService.PopulateVoteTypes()

            elif action == 'clear':
                self.clearDatabase()

            elif action == 'resetToStable':
                self.clearDatabase()
                self._voteService.PopulateVoteTypes()

            self.response.out.write('Done!')
        except BaseException:
            self.response.out.write('Failed!')

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