import json
from app.data.beans import *

class JsonTmpl:
    pass

# TODO: This class will definitely be re-written soon, this is here purely because it wasn't super easy to encode objects into JSON
class JsonUtil:
    @staticmethod
    def jsonEncodeList(list):
        jsonString = "["

        for index, el in enumerate(list):
            jsonTmpl = []

            if isinstance(el, ProposalBean):
                jsonTmpl = JsonUtil._createProposalTmpl(el)
            elif isinstance(el, VoteBean):
                jsonTmpl = JsonUtil._createVoteTmpl(el)

            jsonString += json.dumps(jsonTmpl.__dict__)

            if index < (len(list) - 1):
                jsonString += ","

        jsonString += "]"

        return jsonString

    @staticmethod
    def _createProposalTmpl(p):
        proposalTmpl = JsonTmpl()

        proposalTmpl.id = p.id
        proposalTmpl.name = p.name
        proposalTmpl.description = p.description
        proposalTmpl.technologiesUsed = p.technologiesUsed
        proposalTmpl.rating = p.rating

        return proposalTmpl

    @staticmethod
    def _createVoteTmpl(v):
        voteTmpl = JsonTmpl()

        voteTmpl.userId = v.userId
        voteTmpl.weight = v.weight

        return voteTmpl