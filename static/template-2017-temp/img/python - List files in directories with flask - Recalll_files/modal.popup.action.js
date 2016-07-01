var ModalAction=(function(){var RemotePopupAction=function(block){$('.remote-popup-action').unbind("click").click(function(e){event.preventDefault();$('#model-header').html($(this).attr('title'));var me=this;$.ajax({type:$(this).attr('data-via'),url:$(this).attr('data-url'),data:$(this).attr('data-text'),success:function(data)
{$("#modal-content").html(data);if($(me).attr('data-header')=="false")
$('.modal-header').hide();if($(me).attr('data-width')!=undefined)
$('.modal-dialog').css("width",$(me).attr('data-width'));$('#modalPopup').modal('show');bindSubmit();},error:function(data)
{$("#modal-content").html(data);}});return false;});function bindSubmit(){$(".form-submit-action").submit(function(event){event.preventDefault();var submit=$(this).children('#submit');submit.button('loading');$.ajax({type:$(this).attr('method'),url:$(this).attr('action'),data:$(this).serializeArray(),success:function(data)
{$("#modal-content").html(data);submit.button('reset')
bindSubmit();},error:function(data)
{submit.button('reset')}});return false;});}}
var PopupAction=function(block){$('.popup-action').unbind("click").click(function(e){event.preventDefault();$('#model-header').html($(this).attr('target-title'));$.ajax({type:$(this).attr('target-method'),url:$(this).attr('target-remote'),data:$(this).attr('target-data'),success:function(data)
{$("#modal-content").html(data);$('#modalPopup').modal('show')},error:function(data)
{$("#modal-content").html(data);}});return false;});}
return{popupAction:PopupAction,remotePopupAction:RemotePopupAction}})();