from app.data.models import *

class BackerVoteService:

    def GetBackerVotesByBackerId(self, backerId):
        _backer = Backer.get_by_id(int(backerId))

        return BackerVote.gql("WHERE backer = :backer", backer = _backer)

    def GetBackerCurrentProposals(self, backerId):
        _backer = Backer.get_by_id(int(backerId))
        result = []

        votes = Vote.all().filter('backer = ', _backer)    #.filter('proposal.status = ', 'OPEN')

        for v in votes:
            if v.proposal.status == 'OPEN':
                result.append(v.proposal)

        return result
