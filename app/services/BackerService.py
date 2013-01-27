from google.appengine.api import users

from app.data.models import *
from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

class BackerService:

    def GetCurrentBacker(self):
        result = self.GetBackerByEmail(users.get_current_user().email())
        return result

    def GetBackerByEmail(self, email):
        result = self.BackerFactory(email)
        return result

    def BackerFactory(self, email):
        entity = Backer()

        backerKeyQuery = db.GqlQuery("SELECT __key__ FROM Backer WHERE userId = '" + email + "'")
        backerKey = backerKeyQuery.get()

        if backerKey:
            entity = Backer.get_by_id(backerKey.id())
        else:
            entity.userId = email
            entity.put()

            BackerVote(
                backer = entity,
                voteType = VoteTypeUtil.GetVoteTypeByLabel(VoteTypeEnum.GOLD),
                quantity = 1
            ).put()

            BackerVote(
                backer = entity,
                voteType = VoteTypeUtil.GetVoteTypeByLabel(VoteTypeEnum.SILVER),
                quantity = 1
            ).put()

            BackerVote(
                backer = entity,
                voteType = VoteTypeUtil.GetVoteTypeByLabel(VoteTypeEnum.BRONZE),
                quantity = 1
            ).put()

        return entity

    def BackerHasVoteType(self, email, voteTypeLabel):
        result = False
        _backer = self.GetBackerByEmail(email)

        for bv in _backer.remainingVotes:
            if bv.voteType.label == voteTypeLabel:
                if bv.quantity > 0:
                    result = True

        return result

    def AddBackerVote(self, email, voteTypeLabel):
        processed = False
        _backer = self.GetBackerByEmail(email)

        for bv in _backer.remainingVotes:
            if bv.voteType.label == voteTypeLabel:
                bv.quantity += 1
                bv.save()
                processed = True

        if not processed:
            BackerVote(
                backer = _backer,
                voteType = VoteTypeUtil.GetVoteTypeByLabel(voteTypeLabel),
                quantity = 1
            ).put()

    def RemoveBackerVote(self, email, voteTypeLabel):
        processed = False
        _backer = self.GetBackerByEmail(email)

        for bv in _backer.remainingVotes:
            if bv.voteType.label == voteTypeLabel:
                bv.quantity -= 1
                bv.save()
                processed = True

        if not processed:
            raise Exception("User doesn't have enough votes!")