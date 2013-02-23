from app.data.models import *
from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil
from app.services.BackerVoteService import BackerVoteService

class BackerService:
    def VerifyBacker(self, email, password):
        backer = self.GetBackerByEmail(email)

        if backer and backer.password == password:
            return backer
        else:
            return None

    def GetBackerByEmail(self, email):
        backer = Backer.gql("WHERE email = '%s'" % email).get()

        #TODO: Pass in a hashmap (or something) from the resource layer that includes a list of fields the user is expanding on
        #TODO: and use this to determine weather or not to include the current proposals in the result
        if backer:
            #fetch a list of backer's votes for open proposals
            curVotes = BackerVoteService().GetBackerCurrentVotes(backer.key().id())

            # Apparently you can't set empty lists to dynamic properties, so check for nulls (this has to be researched more)
            if curVotes:
                curVotes = sorted(curVotes, key=lambda Vote: Vote.voteType.weight, reverse=True)

                setattr(backer, 'currentVotes', curVotes)

        return backer

    def CreateBacker(self, email, username, password, role):
        # Note: There seems like a better way to do this, but i couldn't see an OR in GQL right away
        emailBackerExists = Backer.gql("WHERE email = '%s'" % email).get()
        usernameBackerExists = Backer.gql("WHERE username = '%s'" % username).get()

        if emailBackerExists or usernameBackerExists:
            raise ValueError("The backer you tried to create already exists")


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