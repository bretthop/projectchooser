from google.appengine.api import users

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
        bean.votes = entity.votes
#
#        # sum up total rating based on all votes
#        for v in bean.votes:
#            bean.rating += v.weight
#            # if vote belongs to current user, set it as user's vote
#            if v.userId == currentUser.email():
#                bean.hasUserVoted = True
#                bean.userVote = v

        return bean

    @staticmethod
    def compareTo(a, b):
        return cmp(b.rating, a.rating)

class BackerBean():
    id = 0
    userId = ''
    remaining_gold = 0
    remaining_silver = 0
    remaining_bronze = 0

#TODO: This may not be needed, but has been committed just in case
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
            bean.proposalId = e.proposalId
            bean.weight = e.weight

            beans.append(bean)

        return beans