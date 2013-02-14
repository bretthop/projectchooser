import json
from app.data.model.Domain import Domain
from app.data.models import Proposal, Role, Backer

###
# Factory method for creating a proposal object from JSON
#
def toProposal(jsonStr):
    jsonDict = json.loads(jsonStr)

    proposal = None

    if jsonDict.has_key('domain') and jsonDict['domain'].has_key('id'):
        domainId = jsonDict['domain']['id']

        if domainId:
            # Construct a proposal object, giving it the required domain
            domain = Domain.get_by_id(int(domainId))
            proposal = Proposal(domain = domain)

            # Delete the domain attribute, as we have already set the domain to the proposal
            jsonDict.pop('domain')

            # Set basic values
            for name, value in jsonDict.iteritems():
                setattr(proposal, name, value)

    return proposal

def toBacker(jsonStr):
    jsonDict = json.loads(jsonStr)

    role = Role.gql('WHERE name = \'BACKER\'').get()

    backer = Backer(
        email = jsonDict['email'],
        username = jsonDict['username'],
        password = jsonDict['password'],
        role = role
    )

    return backer