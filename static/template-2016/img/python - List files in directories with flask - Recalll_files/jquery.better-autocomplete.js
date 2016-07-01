(function($){$.fn.betterAutocomplete=function(method){var methods={init:function(resource,options,callbacks){var $input=$(this),bac=new BetterAutocomplete($input,resource,options,callbacks);$input.data('better-autocomplete',bac);bac.enable();},enable:function(bac){bac.enable();},disable:function(bac){bac.disable();},destroy:function(bac){bac.destroy();}},args=Array.prototype.slice.call(arguments,1);this.each(function(){switch(method){case'init':methods[method].apply(this,args);break;case'enable':case'disable':case'destroy':var bac=$(this).data('better-autocomplete');if(bac instanceof BetterAutocomplete){methods[method].call(this,bac);}
break;default:$.error(['Method',method,'does not exist in jQuery.betterAutocomplete.'].join(' '));}});return this;};var BetterAutocomplete=function($input,resource,options,callbacks){var lastRenderedQuery='',cache={},cacheOrder=[],cacheSize=0,timer,activeRemoteCalls=[],disableMouseHighlight=false,inputEvents={},isLocal=($.type(resource)!='string'),$results=$('<ul />').addClass('better-autocomplete'),hiddenResults=true,preventBlurTimer=null;var fireSelect=false;options=$.extend({charLimit:isLocal?1:1,delay:350,caseSensitive:false,cacheLimit:isLocal?0:0,remoteTimeout:10000,crossOrigin:false,selectKeys:[9,13],autoHighlight:true},options);callbacks=$.extend({},defaultCallbacks,callbacks);callbacks.insertSuggestionList($results,$input);inputEvents.focus=function(){preventBlurTimer||redraw(true);};inputEvents.blur=function(){if(preventBlurTimer){$input.focus();}
else{redraw();}};inputEvents.keydown=function(event){var index=getHighlightedIndex();if($.inArray(event.keyCode,[38,40])>=0&&$results.children().length>0){var newIndex,size=$('.result',$results).length;switch(event.keyCode){case 38:newIndex=Math.max(-1,index-1);break;case 40:newIndex=Math.min(size-1,index+1);break;}
disableMouseHighlight=true;setHighlighted(newIndex,'key',true);return false;}
else if($.inArray(event.keyCode,options.selectKeys)>=0&&!event.shiftKey&&!event.ctrlKey&&!event.altKey&&!event.metaKey){select();return event.keyCode==13;}};inputEvents.keyup=inputEvents.click=reprocess;$results.delegate('.result',{mouseenter:function(){if(disableMouseHighlight){return;}
setHighlighted($('.result',$results).index($(this)),'mouse');},mousemove:function(){disableMouseHighlight=false;},mousedown:function(){select();return false;}});$results.mousedown(function(){clearTimeout(preventBlurTimer);preventBlurTimer=setTimeout(function(){preventBlurTimer=null;},50);return false;});$results.mouseleave(function(){if(!options.autoHighlight){setHighlighted(-1);}});this.enable=function(){$input.attr('autocomplete','OFF').attr('aria-autocomplete','list');$input.bind(inputEvents);};this.disable=function(){$input.removeAttr('autocomplete').removeAttr('aria-autocomplete');$results.hide();$input.unbind(inputEvents);};this.destroy=function(){$results.remove();$input.unbind(inputEvents);$input.removeData('better-autocomplete');};var cacheResults=function(query,results){cacheSize+=results.length;while(cacheSize>options.cacheLimit&&cacheOrder.length){var key=cacheOrder.shift();cacheSize-=cache[key].length;delete cache[key];}
cacheOrder.push(query);cache[query]=results;};var setHighlighted=function(index,trigger,autoScroll){var prevIndex=getHighlightedIndex(),$resultList=$('.result',$results);$resultList.removeClass('highlight');if(index<0){return}
$resultList.eq(index).addClass('highlight')
if(prevIndex!=index){var result=getResultByIndex(index);callbacks.highlight(result,$input,trigger);}
var up=index==0||index<prevIndex,$scrollTo=$resultList.eq(index);if(!autoScroll){return;}
if($scrollTo.prev().is('.group')&&up){$scrollTo=$scrollTo.prev();}
if($scrollTo.position().top<0){$results.scrollTop($scrollTo.position().top+$results.scrollTop());}
else if(($scrollTo.position().top+$scrollTo.outerHeight())>$results.height()){$results.scrollTop($scrollTo.position().top+$results.scrollTop()+
$scrollTo.outerHeight()-$results.height());}};var getHighlightedIndex=function(){var res=$('.result.highlight',$results)
ind=$('.result',$results).index(res);return ind};var getResultByIndex=function(index){var $result=$('.result',$results).eq(index);if(!$result.length){return;}
return $result.data('result');};var select=function(){var highlighted=getHighlightedIndex();if(highlighted>=0){var result=getResultByIndex(highlighted);callbacks.select(result,$input);reprocess();fireSelect=true;hide(false);}};var fetchResults=function(query){if(isLocal){cacheResults(query,callbacks.queryLocalResults(query,resource,options.caseSensitive));redraw();}
else{activeRemoteCalls.push(query);var url=callbacks.constructURL(resource,query);callbacks.beginFetching($input);callbacks.fetchRemoteData(url,function(data){var searchResults=callbacks.processRemoteData(data);if(!$.isArray(searchResults)){searchResults=[];}
cacheResults(query,searchResults);activeRemoteCalls=$.grep(activeRemoteCalls,function(value){return value!=query;});if(!activeRemoteCalls.length){callbacks.finishFetching($input);}
redraw();},options.remoteTimeout,options.crossOrigin);}};function reprocess(event){if(fireSelect){fireSelect=false;return;}
if($.type(event)=='object'&&event.type=='keyup'&&$.inArray(event.keyCode,[38,40])>=0){return;}
var query=callbacks.canonicalQuery($input.val(),options.caseSensitive);clearTimeout(timer);timer=null;redraw();if(query.length>=options.charLimit&&!$.isArray(cache[query])&&$.inArray(query,activeRemoteCalls)==-1){$results.empty();if(isLocal){fetchResults(query);}
else{timer=setTimeout(function(){fetchResults(query);timer=null;},options.delay);}}};var redraw=function(focus){var query=callbacks.canonicalQuery($input.val(),options.caseSensitive);if(!$.isArray(cache[query])){lastRenderedQuery=null;$results.empty();}
else if(lastRenderedQuery!==query){lastRenderedQuery=query;renderResults(cache[query]);if(options.autoHighlight&&$('.result',$results).length>0){setHighlighted(0,'auto');}}
if(($input.is(':focus')||focus)&&!$results.is(':empty')){$results.filter(':hidden').show().scrollTop($results.data('scroll-top'));if(hiddenResults){hiddenResults=false;callbacks.afterShow($results);}}
else if($results.is(':visible')){hide(false);}};var hide=function(focus){$results.data('scroll-top',$results.scrollTop()).hide();if(!hiddenResults){hiddenResults=true;callbacks.afterHide($results);}}
var renderResults=function(results){$results.empty();var groups={};$.each(results,function(index,result){var output=callbacks.themeResult(result);if($.type(output)!='string'){return;}
var group=callbacks.getGroup(result);if($.type(group)=='string'&&!groups[group]){var $groupHeading=$('<li />').addClass('group').append($('<h3 />').html(group)).appendTo($results);groups[group]=$groupHeading;}
var $result=$('<li />').addClass('result').append(output).data('result',result).addClass(result.addClass);if($.type(group)!='string'&&!$results.children().first().is('.result')){$results.prepend($result);return;}
var $traverseFrom=($.type(group)=='string')?groups[group]:$results.children().first();var $target=$traverseFrom.nextUntil('.group').last();$result.insertAfter($target.length?$target:$traverseFrom);});};};var defaultCallbacks={select:function(result,$input){$input.val(result);},highlight:function(result,$input,trigger){},themeResult:function(result){var output=[];if($.type(result)=='string'){output.push('<h4>',result,'</h4>');}
if($.type(result.title)=='string'){output.push('<h4>',result.title,'</h4>');}
if($.type(result.description)=='string'){output.push('<p>',result.description,'</p>');}
return output.join('');},queryLocalResults:function(query,resource,caseSensitive){if(!$.isArray(resource)){return[];}
var results=[];$.each(resource,function(i,value){switch($.type(value)){case'string':if((caseSensitive?value:value.toLowerCase()).indexOf(query)>=0){results.push({title:value});}
break;case'object':if($.type(value.title)=='string'&&(caseSensitive?value.title:value.title.toLowerCase()).indexOf(query)>=0){results.push(value);}
else if($.type(value.description)=='string'&&(caseSensitive?value.description:value.description.toLowerCase()).indexOf(query)>=0){results.push(value);}
break;}});return results;},fetchRemoteData:function(url,completeCallback,timeout,crossOrigin){$.ajax({url:url,dataType:crossOrigin&&!$.support.cors?'jsonp':'json',timeout:timeout,success:function(data,textStatus){completeCallback(data);},error:function(jqXHR,textStatus,errorThrown){completeCallback();}});},processRemoteData:function(data){if($.isArray(data)){return data;}
else{return[];}},getGroup:function(result){if($.type(result.group)=='string'){return result.group;}},beginFetching:function($input){$input.addClass('fetching');},finishFetching:function($input){$input.removeClass('fetching');},afterShow:function($results){},afterHide:function($results){},constructURL:function(path,query){return path+(path.indexOf('?')>-1?'&':'?')+'q='+encodeURIComponent(query);},canonicalQuery:function(rawQuery,caseSensitive){var query=$.trim(rawQuery);if(!caseSensitive){query=query.toLowerCase();}
return query;},insertSuggestionList:function($results,$input){$results.width($input.outerWidth()-2).css({position:'absolute',left:$input.position().left,top:$input.position().top+$input.outerHeight()}).hide().insertAfter($input);}};var filters=$.expr[':'];if(!filters.focus){filters.focus=function(elem){return elem===document.activeElement&&(elem.type||elem.href);};}})(jQuery);