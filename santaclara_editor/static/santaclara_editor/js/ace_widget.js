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
    
    var EDITOR_DICT = {};

    $(".santa_clara_text_editor").each(function(){
	console.log($(this));
	var ta_id=$(this).data("ta_id");
	var name=$(this).data("ta_name");
	var santa_clara_text_editor_id=$(this).attr("id");

	var editor=ace.edit(santa_clara_text_editor_id);
	var jq_editor_box=$(this).parent();

	EDITOR_DICT[santa_clara_text_editor_id]=editor;

	editor.setTheme("ace/theme/eclipse");
	editor.getSession().setMode("ace/mode/plain_text");

	editor.getSession().setUseWrapMode(true);
	editor.setShowPrintMargin(false);

	editor.on("change",function(event){
	    jq_editor_box.addClass("modified");
	});
	
	editor.commands.addCommand({
	    name: 'Move to cursor to  the start of the current line.',
	    bindKey: {win: 'Ctrl-A',  mac: 'Command-A'},
	    exec: function(editor) {
		editor.navigateLineStart();
		editor.focus();
	    },
	    readOnly: false // false if this command should not apply in readOnly mode
	}); 

	editor.commands.addCommand({
	    name: 'Move to cursor to the end of the current line.',
	    bindKey: {win: 'Ctrl-E',  mac: 'Command-E'},
	    exec: function(editor) {
		editor.navigateLineEnd();
		editor.focus();
	    },
	    readOnly: false // false if this command should not apply in readOnly mode
	}); 

	editor.commands.addCommand({
	    name: 'Move to cursor to  the end of the current file.',
	    bindKey: {win: 'Ctrl-G',  mac: 'Command-G'},
	    exec: function(editor) {
		editor.gotoLine(editor.getSession().getLength());
		editor.focus();
	    },
	    readOnly: false // false if this command should not apply in readOnly mode
	}); 

	editor.commands.addCommand({
	    name: 'Move to cursor to the start of the current file.',
	    bindKey: {win: 'Ctrl-<',  mac: 'Command-<'},
	    exec: function(editor) {
		editor.gotoLine(0);
		editor.focus();
	    },
	    readOnly: false // false if this command should not apply in readOnly mode
	}); 

	editor.commands.addCommand({
	    name: 'Remove to line end.',
	    bindKey: {win: 'Ctrl-k',  mac: 'Command-k'},
	    exec: function(editor) {
		editor.removeToLineEnd();
		editor.focus();
	    },
	    readOnly: false // false if this command should not apply in readOnly mode
	}); 

	editor.commands.addCommand({
	    name: 'Remove word right.',
	    bindKey: {win: 'Alt-d',  mac: 'Alt-d'},
	    exec: function(editor) {
		editor.removeWordRight();
		editor.focus();
	    },
	    readOnly: false // false if this command should not apply in readOnly mode
	}); 

	var form=$(this).closest("form");
	var ta_name=$(this).data("ta_name");
	var ta_id=$(this).data("ta_id");

	form.submit( function(event){
	    var text=editor.getSession().toString();
	    var ta_html="<textarea name=\""+ta_name+"\"";
	    ta_html+=" id=\""+ta_id+"\">";
	    ta_html+=text;
	    ta_html+="</textarea>";
	    $(this).append(ta_html);
	    return true;
	});

    });

    $(".santa_clara_text_editor_button_simple").click(function(event){
	event.preventDefault();
	var tag=$(this).data("tag");
	var parent=$(this).parent();
	var santa_clara_text_editor_id=parent.data("santa_clara_text_editor_id");
	var editor=EDITOR_DICT[santa_clara_text_editor_id];

	var range=editor.getSelectionRange();

	editor.clearSelection();

	editor.moveCursorTo(range.end.row,range.end.column,true);
	editor.insert("[/"+tag+"]");

	editor.moveCursorTo(range.start.row,range.start.column,true);
	editor.insert("["+tag+"]");

	editor.moveCursorTo(range.end.row,range.end.column+5+2*tag.length,true);
	editor.focus();

    });

    $(".santa_clara_text_editor_button_single").click(function(event){
	event.preventDefault();
	var tag=$(this).data("tag");
	var parent=$(this).parent();
	var santa_clara_text_editor_id=parent.data("santa_clara_text_editor_id");
	var editor=EDITOR_DICT[santa_clara_text_editor_id];
	editor.insert("["+tag+"/]");
	editor.focus();
    });
    
    $(".santa_clara_text_editor_button_function").click(function(event){
	event.preventDefault();
	var tag=$(this).data("tag");
	var parent=$(this).parent();
	var santa_clara_text_editor_id=parent.data("santa_clara_text_editor_id");
	var editor=EDITOR_DICT[santa_clara_text_editor_id];
	switch (tag) {
	case "action_upper": 
	    editor.toUpperCase();
	    break;
	case "action_lower": 
	    editor.toLowerCase();
	    break;
	}
    });
    
    
    $("form").each( function () {
	myObserver.observe (this, obsConfig);
    });

    

});

