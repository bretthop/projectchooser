from app.data.models import *

class BackerVoteService:

    def GetBackerVotesByBackerId(self, backerId):
        _backer = Backer.get_by_id(int(backerId))

        return BackerVote.gql("WHERE backer = :backer", backer = _backer)
