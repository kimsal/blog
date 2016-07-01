var Collection=(function(){var Init=function(block){'use strict';$('.explore-navigator').click(function(event){event.preventDefault();var data={};$.get($(this).attr('href'),data).done(function(data){$('#inner-body').html(data);Collection.Init();}).fail(function(){}).always(function(){});;});};var Add=function(block){$('.add-collection-list').unbind("click").click(function(e){event.preventDefault();if($('#search').val().length>0)
{$.ajax({type:"POST",url:$(this).attr('data-url'),data:$(this).children('form').serializeArray(),success:function(data)
{$("#side-container").html(data);},error:function(data)
{}});}
return false;});}
var Remove=function(block){$('.remove-collection-list').unbind("click").click(function(e){event.preventDefault();{$.ajax({type:"POST",url:$(this).attr('data-url'),data:$(this).children('form').serializeArray(),success:function(data)
{$("#side-container").html(data);Collection.Remove();},error:function(data)
{}});}
return false;});}
return{Init:Init,Add:Add,Remove:Remove}})();