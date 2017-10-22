$(document).on('ready', function () {
				
	$('.yay').on('click', function() {
		alert('Yay! You\'re here!')
	});
	
	$('.add-app').on('click', function() {
		$('input.add-form').val(null);
	});
	
	$('.app-table').DataTable();
	
	$('[data-toggle=tooltip]').tooltip({
	    selector: '',
	    placement: 'left',
	    container:'body'
	  });

});