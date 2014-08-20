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
    
    $(".santa-clara-editor").each(function(){
	console.log($(this));
	
	var ta_id=$(this).data("ta_id");
	var name=$(this).data("ta_name");
	
	$(this).santa_clara_editor({
	    textarea_id: ta_id,
	    textarea_name: name
	});
    });
	
    $("form").each( function () {
	myObserver.observe (this, obsConfig);
    });


});

