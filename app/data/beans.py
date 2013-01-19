class ProposalBean():
    id = 0
    name = ''
    description = ''
    technologiesUsed = ''
    rating = 0
    hasUserVoted = False
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

    def setVotes(self, votes):
        self.votes = votes
        weight = 0

        #TODO: fetch SUM from DB if possible using db.GqlQuery('SELECT SUM(weight) FROM Vote WHERE proposalId = ' + str(proposal.key().id()))
        for v in votes:
            weight += v.weight

        self.rating = weight

class BackerBean():
    id = 0
    userId = ''
    remaining_gold = 0
    remaining_silver = 0
    remaining_bronze = 0