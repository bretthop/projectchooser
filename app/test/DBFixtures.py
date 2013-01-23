from app.data.models import VoteType

class DBFixtures:

    def PopulateVoteTypes(self):
        vt = VoteType()
        vt.label = 'GOLD'
        vt.weight = 8
        vt.put()

        vt = VoteType()
        vt.label = 'SILVER'
        vt.weight = 5
        vt.put()

        vt = VoteType()
        vt.label = 'BRONZE'
        vt.weight = 3
        vt.put()