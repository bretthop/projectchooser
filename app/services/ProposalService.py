from google.appengine.api import users

from app.data.models import *
from app.data.beans import *
from app.services.BackerService import *

class ProposalService:

    def ProposalFactory(self, name, description, technologies):
        result = Proposal(
            name             = name,
            description      = description,
            technologiesUsed = technologies,
            status           = 'OPEN'
        )
        return result

    def GetProposalBeansByStatus(self, status):
        result = []
        proposals = Proposal.gql("WHERE status = '" + status +"'")

        for proposal in proposals:
            propBean = ProposalBean.fromEntity(proposal)
            result.append(propBean)

        return result