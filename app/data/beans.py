class ProposalBean():
    id = 0
    name = ''
    description = ''
    technologiesUsed = ''
    rating = 0
    hasUserVoted = False

    def fromEntity(self, entity):
        self.id = entity.key().id()
        self.name = entity.name
        self.description = entity.description
        self.technologiesUsed = entity.technologiesUsed
        self.rating = entity.rating
