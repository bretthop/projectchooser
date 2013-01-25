function addProposal()
{
    showAjaxLoader();

    var data = {
        name: $('#name').val(),
        description: $('#description').val(),
        technologiesUsed: $('#technologiesUsed').val()
    };

    ajax('post', '/api/proposals', data, DataType.JSON, function() { loadPage(); })
}

function withdraw(voteId)
{
    showAjaxLoader();

    ajax('delete', '/api/votes?voteId=' + voteId, '', DataType.DEFAULT, function() { loadPage(); });
}

function vote(proposalId, weight)
{
    showAjaxLoader();

    ajax('post', '/api/votes?proposalId=' + proposalId + '&weight=' + weight, '', DataType.DEFAULT, function() { loadPage(); });
}

function loadPage()
{
    showAjaxLoader();

    resetAddProposalForm();

    ajax('get', '/api/backers', '', DataType.DEFAULT, function(backer) {
        fetchTmpl(BACKER_TMPL_URL, function(tmpl) {
            addFriendlyLabel(backer);

            var renderedHtml = _.template(tmpl, backer);
            $('.backerTmpl-rendered').html(renderedHtml);

            ajax('get', '/api/proposals', '', DataType.DEFAULT, function(proposals) {
                //Apply current backer information to the returned list of proposals
                applyCurrentBackerContext(proposals, backer);

                //Sort the proposals by rating descending
                proposals.sort(function(a, b) { return a.rating < b.rating; });

                fetchTmpl(PROPOSALS_TMPL_URL, function(tmpl) {
                    var renderedHtml = _.template(tmpl, { proposals: proposals, currentBacker: backer });
                    $('.proposalsTmpl-rendered').html(renderedHtml);

                    hideAjaxLoader();
                });
            });
        });
    });
}

function addFriendlyLabel(currentBacker)
{
    _.each(currentBacker.remainingVotes, function(remainingVote) {
        remainingVote.voteType.friendlyLabel = toStartCase(remainingVote.voteType.label);
    });
}

/**
 * Adds context information to a list of proposals based on the currently logged in backer.
 *
 * It also sums up all the vote weights for each proposal
 *
 * @param proposals
 * @param currentBacker
 */
function applyCurrentBackerContext(proposals, currentBacker)
{
    for (var i = 0; i < proposals.length; i++) {
        var proposal = proposals[i];

        var rating = 0;
        var hasUserVoted = false;
        var userVote = null;

        for (var j = 0; j < proposal.votes.length; j++) {
            var vote = proposal.votes[j];

            rating += vote.voteType.weight;

            if (vote.userId == currentBacker.userId) {
                hasUserVoted = true;
                userVote = vote;
            }
        }

        proposal.rating = rating;
        proposal.hasUserVoted = hasUserVoted;
        proposal.userVote = userVote;
    }
}

function toStartCase(str)
{
    return str.substr(0, 1) + str.toLowerCase().substring(1);
}