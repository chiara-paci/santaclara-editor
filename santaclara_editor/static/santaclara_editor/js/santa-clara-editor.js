
var append_interceptor = function(obj,method,arguments){
    console.log(method);
    console.log(obj);
    console.log(arguments);
};



/* $("#santa_clara_'+ta_id+'").closest("form").hook("append",append_interceptor);\n'
   #$("#santa_clara_'+ta_id+'").closest("form").hook("insertBefore",append_interceptor);\n' */

var set_santaclara_editor = function() {
    $(".santa-clara-editor").each(function(){
	console.log($(this));
	
	var ta_id=$(this).data("ta_id");
	var name=$(this).data("ta_name");
	
	$(this).santa-clara-editor({
	    textarea_id: ta_id,
	    textarea_name: name
	});
	
    });
};

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
