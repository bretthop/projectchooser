from google.appengine.ext import db
from app.data.model.VoteType import VoteType

class VoteTypeUtil:

    @staticmethod
    def GetVoteTypeByLabel(label):
        label = str(label).upper()
        _voteTypeId = db.GqlQuery("SELECT __key__ FROM VoteType WHERE label = '" + label + "'").get().id()
        result = VoteType.get_by_id(_voteTypeId)

        return result