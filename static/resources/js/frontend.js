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

ajax.setAjaxLoader($('.ajax-loader'));

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

function showLoginModal()
{
    $('#loginModal').modal();
}