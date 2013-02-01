function addProposal()
{
    var valid = addProposalValidator.form();

    if (valid) {
        ajax.showAjaxLoader();

        var data = {
            name: $('#name').val(),
            description: $('#description').val(),
            technologiesUsed: $('#technologiesUsed').val()
        };

        ajax.req('post', '/api/proposals', data, DataType.JSON, function() { loadPage(); });

        return true;
    }
    else {
        return false;
    }
}

function withdraw(voteId)
{
    ajax.showAjaxLoader();

    ajax.req('delete', '/api/votes?voteId=' + voteId, '', DataType.DEFAULT, function() { loadPage(); });
}

function vote(proposalId, weight)
{
    ajax.showAjaxLoader();

    ajax.req('post', '/api/votes?proposalId=' + proposalId + '&weight=' + weight, '', DataType.DEFAULT, function() { loadPage(); });
}

function login(user, pass)
{
    ajax.showAjaxLoader();

    var successFunc = function() {
        alert('Login Successful!');
    };

    var errorFunc = function() {
        alert('Login Failed');
    };

    ajax.req('post', '/api/login?username=' + user + '&password=' + pass, '', DataType.DEFAULT, successFunc, errorFunc);

    ajax.hideAjaxLoader();
}

function loadPage()
{
    ajax.showAjaxLoader();

    resetAddProposalForm();

    ajax.req('get', '/api/backers', '', DataType.DEFAULT, function(backer) {
        fetchTmpl(BACKER_TMPL_URL, function(tmpl) {
            var renderedHtml = _.template(tmpl, backer);
            $('.backerTmpl-rendered').html(renderedHtml);

            ajax.req('get', '/api/proposals', '', DataType.DEFAULT, function(proposals) {
                //Apply current backer information to the returned list of proposals
                applyCurrentBackerContext(proposals, backer);

                //Sort the proposals by rating descending
                proposals.sort(function(a, b) { return a.rating < b.rating; });

                fetchTmpl(PROPOSALS_TMPL_URL, function(tmpl) {
                    var renderedHtml = _.template(tmpl, { proposals: proposals, currentBacker: backer });
                    $('.proposalsTmpl-rendered').html(renderedHtml);

                    ajax.hideAjaxLoader();
                });
            });
        });
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

/**
 * Returns the number of votes that have a quantity greater than zero
 * @param votes
 * @return {Number}
 */
function countRemainingVotes(votes)
{
    return _.filter(votes, function(vote) {
        return vote.quantity > 0;
    }).length;
}

/**
 * Sort of gets the username from an email address (basically it just returns whats before the '@')
 * @param email
 * @return {*}
 */
function getUsernameFromEmail(email)
{
    return email.split('@')[0];
}

/**
 * Converts to start case. E.g. "GOLD" => "Gold", "gold" => "Gold"
 * @param str
 * @return {String}
 */
function toStartCase(str)
{
    return str.substr(0, 1) + str.toLowerCase().substring(1);
}