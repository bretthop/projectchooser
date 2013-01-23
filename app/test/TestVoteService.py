import unittest
from app.services.VoteService import VoteService
from app.data.models import *

class TestVoteService(unittest.TestCase):
    _vs = None

    def setUp(self):
        self._vs = VoteService()

    def test_voteForProposal(self):
        _voteType = VoteType.get_by_id(31)
        _proposal = Proposal.get_by_id(1)

        Vote(
            userId = "test@example.com",
            proposal = _proposal,
            voteType = _voteType
        ).put()

if __name__ == '__main__':
    unittest.main()