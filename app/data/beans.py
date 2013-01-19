class ProposalBean():
    id = 0
    name = ''
    description = ''
    technologiesUsed = ''
    rating = 0
    hasUserVoted = False
    votes = []

    def fromEntity(self, entity):
        self.id = entity.key().id()
        self.name = entity.name
        self.description = entity.description
        self.technologiesUsed = entity.technologiesUsed
        self.rating = -1    #entity.rating

class BackerBean():
    id = 0
    userId = ''
    remaining_gold = 0
    remaining_silver = 0
    remaining_bronze = 0