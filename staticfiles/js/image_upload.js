function cke_img_upload(input){
    var myFormData = new FormData();
    myFormData.append('upload', input.files[0]);
    $.ajax({
      url: 'http://127.0.0.1/ckeditor/upload/',
      type: 'POST',
      processData: false, // important
      contentType: false, // important
      dataType : 'json',
      data: myFormData,
      success: function (success_data) {
        ckeditor_field = $('.' + $(input).attr('id').replace('img_','')).prev()
        if (ckeditor_field[0]){
            CKEDITOR.instances[ckeditor_field.attr('id')].insertHtml(jQuery('<img/>', {src: success_data['url']}).attr('data-cke-saved-src',success_data['url']).prop('outerHTML'));
        }
      },
      error: function (error_data) {
         console.log(error_data)
      }
    });
}

function load_image_in_cke(input){

    if (input.files && input.files[0]) {

    file_extension = input.files[0].name.substring(input.files[0].name.lastIndexOf('.') + 1).toLowerCase();

    if (file_extension == "png" || file_extension == "jpeg" || file_extension == "jpg"){
        var reader = new FileReader();
        reader.onload = function (e) {
            cke_img_upload(input)
        }
        reader.readAsDataURL(input.files[0]);
    }
    else{
        show_error_toaster('Only jpg/png formats are supported !!');
    }
  }
}

CKEDITOR.on('instanceReady', function(event) {
    var cke_toolbox = $('.' + event.editor.id).find('.cke_toolbox')
    cke_toolbox.find('.cke_button__image').closest('.cke_toolbar').remove()
    cloned_copy = $('#custom_img_cke').clone().css('display','initial')
    cloned_copy.find('input').attr('id','img_'+event.editor.id)
    cke_toolbox.append(cloned_copy)
});