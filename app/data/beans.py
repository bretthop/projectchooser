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
        bean = ProposalBean()

        bean.id = entity.key().id()
        bean.name = entity.name
        bean.description = entity.description
        bean.technologiesUsed = entity.technologiesUsed
        bean.rating = 0 #entity.rating

        return bean

    @staticmethod
    def compare(a, b):
        return cmp(b.rating, a.rating)

    def setVotes(self, votes, currentUser):
        self.votes = votes
        weight = 0

        # sum up total rating based on all votes
        for v in votes:
            weight += v.weight
            # if vote belongs to current user, set is as user's vote
            if v.userId == currentUser.email():
                self.hasUserVoted = True
                self.userVote = v

        self.rating = weight

class BackerBean():
    id = 0
    userId = ''
    remaining_gold = 0
    remaining_silver = 0
    remaining_bronze = 0