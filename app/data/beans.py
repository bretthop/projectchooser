from google.appengine.api import users
from app.data.models import *

class ProposalBean():
    id = 0
    name = ''
    description = ''
    technologiesUsed = ''
    rating = 0
    hasUserVoted = False
    userVote = None,
    votes = []

    @staticmethod
    def fromEntity(entity):
        """
        :type entity: Proposal
        """
        bean = ProposalBean()
        currentUser = users.get_current_user()

        bean.id = entity.key().id()
        bean.name = entity.name
        bean.description = entity.description
        bean.technologiesUsed = entity.technologiesUsed
        bean.votes = VoteBean.fromEntities(entity.votes)

        # sum up total rating based on all votes
        bean.rating = 0
        for voteBean in bean.votes:
            bean.rating += voteBean.weight
            # if vote belongs to current user, set it as user's vote
            if voteBean.userId == currentUser.email():
                bean.hasUserVoted = True
                bean.userVote = voteBean

        return bean

    def toEntity(self):
        return Proposal(
            name = self.name,
            description = self.description,
            technologiesUsed = self.technologiesUsed,
            status = self.status
        )

    @staticmethod
    def compareTo(a, b):
        return cmp(b.rating, a.rating)

    #TODO: Replace with a proper JSON library
    @staticmethod
    def fromJson(json):
        bean = ProposalBean()

        bean.name = json['name']
        bean.description = json['description']
        bean.technologiesUsed = json['technologiesUsed']
        bean.status = 'OPEN'

        return bean


class BackerBean():
    id = 0
    userId = ''
    remaining_gold = 0
    remaining_silver = 0
    remaining_bronze = 0

class VoteBean():
    id = None
    userId = None
    proposalId = None
    weight = 0

    @staticmethod
    def fromEntities(entities):
        beans = []

        for e in entities:
            bean = VoteBean()

            bean.id = e.key().id()
            bean.userId = e.userId
            bean.proposalId = e.proposal.key().id()
            bean.weight = e.voteType.weight

            beans.append(bean)

        return beans
