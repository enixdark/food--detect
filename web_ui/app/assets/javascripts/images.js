$(form).bind("ajax:success", function(){
  if ( $(this).data('remotipartSubmitted') )
});
$(form).on("ajax:remotipartComplete", function(e, data){
  console.log(e, data)
});