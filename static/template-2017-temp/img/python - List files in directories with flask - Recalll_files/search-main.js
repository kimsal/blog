var Search=(function(){var init=function(block){this.Search.init();this.Search.highlightCode();this.Search.expendCode();};var Search=(function(){var lasturl="";var processing=false;var me=this;function init(){$('#searchform').submit(function(event){event.preventDefault();me.processing=true;var searchView=($('#search-container').size()>0)?true:false;if(searchView){mixpanel.track('App_Search_Submitted',{"Query":$("#search").val()});toggleLoading('show');pushUrl($("#search").val()+" | Recalll","?q="+encodeURIComponent($("#search").val()));$.ajax({type:"GET",url:$(this).attr('action'),data:$(this).serializeArray(),success:function(data)
{toggleLoading('hide');$('#search-container').html(data);highlightCode();slimScroll();var $results_bucket=$('#main-results');Collection.Add()
Collection.Remove();Spam.Add();me.processing=false;viewMore();},error:function(data)
{processing=false;toggleLoading('hide');}});}
return false;});}
function slimScroll(){$('pre').readmore({speed:75,moreLink:'<a href="#">more</a>',lessLink:'<a href="#">less</a>'});}
function highlightCode(){$('pre').each(function(i,block){hljs.highlightBlock(block);});}
function setlast(){}
function toggleLoading(tag){var left=($(window).width()-70)/2;$('#notify').css({'left':left+'px'});if(tag=='show')
{$('#notify').removeClass('hide');$('#notify').css('display','block');}else{$('#notify').addClass('hide');$('#notify').css('display','none');}}
function viewMore(){var parent=this;if($('#view-more').size()<=0)return;$('#view-more').unbind('click').click(function(e){e.preventDefault();var self=this;$(self).html("Loading...");var page=$('.page').last().val();var data=$('#searchform').serializeArray();data.push({name:'page',value:page});mixpanel.track('App_Search_View_More_Clicked',{"Query":$("#search").val(),"Page":page});$.ajax({type:"GET",url:$('#searchform').attr('action'),data:data,success:function(data)
{$('#search-list').append(data);$(self).html("View More");highlightCode();slimScroll()
Collection.Add();Collection.Remove();Spam.Add();me.processing=false;setlast();toggleLoading('hide');},error:function(data)
{processing=false;alert("Sorry there was error processing your request. "+data);toggleLoading('hide');}});});}
return{init:init,expendCode:slimScroll,highlightCode:highlightCode,viewMore:viewMore};})();return{init:init,Search:Search};})();var Spam=(function(){var Add=function(block){$('.spam-knowledge-doc').unbind("click").click(function(e){event.preventDefault();$.ajax({type:"POST",url:$(this).attr('data-url'),data:$(this).children('form').serializeArray(),success:function(data)
{alert('Added to spam');},error:function(data)
{alert('Note added to spam');}});return false;});}
return{Add:Add};})();var Category=(function(){var Init=function(block){'use strict';var $categoryBtn=$('.category-btn');var $categoryForm=$('.category-form');var $closeCategory=$('.close-category');var $header=$('header');$categoryBtn.click(function(){$categoryForm.removeClass('closed').addClass('open');});$closeCategory.click(function(){$categoryForm.removeClass('open').addClass('closed');});};var Add=function(block){}
return{Init:Init,Add:Add}})();