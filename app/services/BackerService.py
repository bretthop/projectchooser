from app.data.beans import *
from app.data.models import Backer
from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

class BackerService:

    def GetCurrentBackerBean(self):
        result = self.BackerFactory(users.get_current_user().email())
        return result

    def BackerFactory(self, email):
        result = BackerBean()
        entity = Backer()

        backerKeyQuery = db.GqlQuery("SELECT __key__ FROM Backer WHERE userId = '" + email + "'")
        backerKey = backerKeyQuery.get()

        if backerKey:
            entity = Backer.get_by_id(backerKey.id())
            result = BackerBean.fromEntity(entity)
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
                quantity = 2
            ).put()

            BackerVote(
                backer = entity,
                voteType = VoteTypeUtil.GetVoteTypeByLabel(VoteTypeEnum.BRONZE),
                quantity = 4
            ).put()

            result = BackerBean.fromEntity(entity)

        return result

    def BackerHasVoteType(self, email, voteType):
        #TODO: implement

        return True
