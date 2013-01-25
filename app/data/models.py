from google.appengine.ext import db
from app.data.model.VoteType import VoteType

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()
    status           = db.StringProperty()

    @staticmethod
    def jsonFields():
        return ['name', 'description', 'technologiesUsed', 'status', 'votes']

    #TODO: Replace with a proper JSON library
    @staticmethod
    def fromJson(json):
        proposal = Proposal()

        proposal.name = json['name']
        proposal.description = json['description']
        proposal.technologiesUsed = json['technologiesUsed']
        proposal.status = 'OPEN'

        return proposal

class Vote(db.Model):
    userId      = db.StringProperty()
    proposal    = db.ReferenceProperty(Proposal, required=True, collection_name='votes')
    voteType    = db.ReferenceProperty(VoteType, required=True)

    @staticmethod
    def jsonFields():
        return ['userId', 'voteType']

class Backer(db.Model):
    userId           = db.StringProperty()

    @staticmethod
    def jsonFields():
        return ['userId', 'remainingVotes']

class BackerVote(db.Model):
    backer          = db.ReferenceProperty(Backer, required=True, collection_name='remainingVotes')
    voteType        = db.ReferenceProperty(VoteType, required=True)
    quantity        = db.IntegerProperty()

    @staticmethod
    def jsonFields():
        return ['voteType', 'quantity']


