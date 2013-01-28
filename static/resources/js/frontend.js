/* Setup front end event handlers */
var addProposalValidator = $("form").validate({
    errorPlacement: function(error, element) {
        //Override errorPlacement function (this stops the automatic 'This field is required' message from showing)
        return true;
    }
});

$('#addProposalModal').on('hide', function () {
    addProposalValidator.resetForm();
    $('#addProposalModal').find('input').val('');
});

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
    $('#addProposalModal').modal();
}

function handleAddProposalClick()
{
    var success = addProposal();

    if (success) {
        $('#addProposalModal').modal('hide');
    }
}

function resetAddProposalForm()
{
    $('#name').val('');
    $('#description').val('');
    $('#technologiesUsed').val('');
}