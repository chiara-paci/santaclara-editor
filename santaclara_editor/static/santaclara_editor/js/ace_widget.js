$(function(){
    var mutationHandler = function (mutationRecords) {
	mutationRecords.forEach ( function (mutation) {
	    if (mutation.type!="childList") return;
	    if (mutation.addedNodes.length==0) return;

	    $(mutation.addedNodes).each(function(){
		$(this).find(".santa-clara-editor").each(function(){
		    var ta_id=$(this).attr("id").replace(/^santa_clara_/,"");
		    var name=$("#"+ta_id+"-label").attr("for").replace(/^label_/,"");

		    console.log($(this),ta_id,name);
		    
		    $(this).santa_clara_editor({
			textarea_id: ta_id,
			textarea_name: name
		    });
		});
	    });

	});
    };

    var MutationObserver    = window.MutationObserver || window.WebKitMutationObserver;
    var myObserver          = new MutationObserver (mutationHandler);
    var obsConfig           = { childList: true, characterData: true, attributes: true, subtree: true };
    
    $(".santa_clara_text_editor").each(function(){
	console.log($(this));
	
	var ta_id=$(this).data("ta_id");
	var name=$(this).data("ta_name");
	
	/*
	$(this).santa_clara_editor({
	    textarea_id: ta_id,
	    textarea_name: name
	});


	var form=$("#"+this.textarea_id).closest("form");
	form.submit( function(event){
	    var text=self.get_text();
	    var ta_name=$("#"+ta_id+"-label").attr("for").replace(/^label_/,"");
	    
	    var ta_html="<textarea name=\""+ta_name+"\"";
	    ta_html+=" id=\""+ta_id+"\">";
	    ta_html+=text;
	    ta_html+="</textarea>";
	    $("#"+ta_id).remove();
	    $(this).append(ta_html);
	    
	    return true;
	});
	*/

    });
	
    $("form").each( function () {
	myObserver.observe (this, obsConfig);
    });


});

