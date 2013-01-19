from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

# Models
# TODO: Move to seperate files
class Proposal(db.Model):
	name = db.StringProperty()
	description = db.StringProperty()
	technologiesUsed = db.StringProperty()
	rating = db.IntegerProperty()

class Vote(db.Model):
	userId = db.StringProperty()
	proposalId = db.IntegerProperty()


# Beans
# TODO: Move to seperate files
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


# Handlers
# TODO: Move to seperate files
class ProposalsHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		
		if user:
			propBeans = []
			proposals = db.GqlQuery('SELECT * FROM Proposal')
			
			for proposal in proposals:
				propBean = ProposalBean()
				propBean.fromEntity(proposal)
				
				userVote = db.GqlQuery('SELECT * FROM Vote WHERE userId = \'' +  user.nickname() + '\' AND proposalId = ' + str(proposal.key().id())) 

				if userVote.count() > 0:
					propBean.hasUserVoted = True
								
				propBeans.append(propBean)
			
			data = { 'proposals': propBeans }

			self.response.out.write(template.render('templates/proposals.html', data))
		else:
			self.redirect(users.create_login_url(self.request.uri))
			
	def post(self):
		proposal = Proposal(
			name = self.request.get('name'),
			description = self.request.get('description'),
			technologiesUsed = self.request.get('technologiesUsed'),
			rating = 0
		)
		
		proposal.put()
		
		self.redirect('/')

class VoteHandler(webapp.RequestHandler):
	def post(self):
		proposalId = int(self.request.get('id'))
		votingWeight = self.request.get('weight')
		votingWeightInt = 0
		
		# TODO: Make this an enum or a model
		if votingWeight == 'gold':
			votingWeightInt = 10
		elif votingWeight == 'silver':
			votingWeightInt = 5
		elif votingWeight == 'bronze':
			votingWeightInt = 3
		
		# Apply vote to proposal
		proposal = Proposal.get_by_id(proposalId)
		proposal.rating += votingWeightInt
		proposal.put()
		
		# Record the vote for the user
		user = users.get_current_user()
		Vote(
			userId = user.nickname(),
			proposalId = proposalId
		).put()
		
		self.redirect('/')
		
def main():
	app = webapp.WSGIApplication(
		[('/', ProposalsHandler),
		 ('/vote', VoteHandler)],
		debug=True)
		
	run_wsgi_app(app)

if __name__ == "__main__":
	main()