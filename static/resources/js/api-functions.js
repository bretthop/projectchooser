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
            var renderedHtml = _.template(tmpl, backer);
            $('.backerTmpl-rendered').html(renderedHtml);

            ajax('get', '/api/proposals', '', DataType.DEFAULT, function(proposals) {
                fetchTmpl(PROPOSALS_TMPL_URL, function(tmpl) {
                    var renderedHtml = _.template(tmpl, { proposals: proposals, currentBacker: backer });
                    $('.proposalsTmpl-rendered').html(renderedHtml);

                    hideAjaxLoader();
                });
            });
        });
    });
}