from app.data.models import *
from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

class BackerService:
    def VerifyBacker(self, email, password):
        backer = self.GetBackerByEmail(email)

        if backer and backer.password == password:
            return backer
        else:
            return None

    def GetBackerByEmail(self, email):
        backer = Backer.gql("WHERE email = '%s'" % email).get()

        #TODO: fetch a list of open proposals with vote from backer
        #TOFIX: openProposals is added to a collection _dynamic_properties of db.Expando object
        #TOFIX: all fields starting with "_" are skipped by JSON serializer
        #setattr(entity, 'openProposals', '1')

        return backer

    def CreateBacker(self, email, username, password, role):
        entity = Backer (
            email = email,
            username = username,
            password = password,
            role = role
        )

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