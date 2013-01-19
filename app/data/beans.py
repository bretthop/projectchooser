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
        return ProposalBean(
            id = entity.key().id(),
            name = entity.name,
            description = entity.description,
            technologiesUsed = entity.technologiesUsed,
            rating = -1,    #entity.rating
        )

    @staticmethod
    def compare(a, b):
        return cmp(b.rating, a.rating)

class BackerBean():
    id = 0
    userId = ''
    remaining_gold = 0
    remaining_silver = 0
    remaining_bronze = 0