// Modal focus
$('#ScrapeModal').on('shown.bs.modal', function () {
  $('#myInput').focus()
  })

// Clean SearchBox button
$(function(){
  $('#search-series-clean').on('click', function(){
    $('#search-series').val('');
    search_series();
  });
});

// Initial POST to get all series
$(function(){
  if($('#search-series').val() === ''){
    search_series(); 
  }
});

// On keyUp, update search
$(function(){
  $('#search-series').keyup(function(){
    search_series();
  });
});

// Update HTML content on success
function searchSuccess(data, textStatus, jqXHR){
  $('#series-data').html(data);
}

// AJAX call
function search_series(){
  $.ajax({
    type: 'POST',
    url: 'search/',
    data:{
      'search_text': $('#search-series').val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: searchSuccess,
    dataType: 'html'
  });
}
