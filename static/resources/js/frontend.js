//TODO: Move 'show/hide ajax loader' into the 'ajax' request, or make it generic so all requests (or request ques) show it
function showAjaxLoader()
{
    $('.ajax-loader').removeClass('hidden').addClass('visible');
}

function hideAjaxLoader()
{
    $('.ajax-loader').removeClass('visible').addClass('hidden');
}

function showAddProposalModal()
{
    $(".addProposalForm").dialog("open");
}

function resetAddProposalForm()
{
    $('#name').val('');
    $('#description').val('');
    $('#technologiesUsed').val('');
}