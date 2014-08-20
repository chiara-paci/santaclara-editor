$(function(){
    var append_interceptor = function(obj,method,arguments){
	console.log(method);
	console.log(obj);
	console.log(arguments);
    };

    /* $("#santa_clara_'+ta_id+'").closest("form").hook("append",append_interceptor);\n'
       #$("#santa_clara_'+ta_id+'").closest("form").hook("insertBefore",append_interceptor);\n' */

    function mutationHandler (mutationRecords) {
	console.log("mutationHandler:");
	
	mutationRecords.forEach ( function (mutation) {
	    if (mutation.addedNodes.length==0) return;
	    console.log("BEGIN",mutation);
            console.log("added len",mutation.addedNodes.length);
	    var new_nodes=$(mutation.addedNodes);
	    new_nodes.each(function(){
		console.log ($(this).is("div.santa-clara-editor"),$(this));
	    });
	    console.log("END");

	} );
    }

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

	$(this).closest("fieldset").parent().parent().each( function () {
	    myObserver.observe (this, obsConfig);
	});

	
    });

    /*
    var targetNodes         = $(".santa-clara-editor");

    var MutationObserver    = window.MutationObserver || window.WebKitMutationObserver;
    var myObserver          = new MutationObserver (mutationHandler);
    var obsConfig           = { childList: true, characterData: true, attributes: true, subtree: true };

    //--- Add a target node to the observer. Can only add one node at a time.
    targetNodes.each ( function () {
	myObserver.observe (this, obsConfig);
    } );
    */


});

/*
var parent_id=$("#santa_clara_'+ta_id+'").closest("fieldset").parent().attr("id");
console.log($("#"+parent_id));
$("#"+parent_id).parent().parent().hook("append",append_interceptor);
$("#"+parent_id).parent().parent().hook("after",append_interceptor);
$("#"+parent_id).parent().hook("append",append_interceptor);
$("#"+parent_id).parent().hook("after",append_interceptor);
$("#"+parent_id).hook("after",append_interceptor);
$("#"+parent_id).hook("append",append_interceptor);

$("#santa_clara_'+ta_id+'").santa_clara_editor({'
textarea_id: "'+ta_id+'",'
						textarea_name: "'+name+'"'
});'
*/						
