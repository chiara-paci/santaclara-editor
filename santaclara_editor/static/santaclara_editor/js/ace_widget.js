$(function(){
    var EDITOR_DICT = {};

    var set_santa_clara_text_editor = function(jq_object){
	console.log(jq_object);
	var ta_id=jq_object.data("ta_id");
	var name=jq_object.data("ta_name");
	var santa_clara_text_editor_id=jq_object.attr("id");

	var editor=ace.edit(santa_clara_text_editor_id);
	var jq_editor_box=jq_object.parent();

	EDITOR_DICT[santa_clara_text_editor_id]=editor;

	editor.setTheme("ace/theme/eclipse");
	editor.getSession().setMode("ace/mode/plain_text");

	editor.getSession().setUseWrapMode(true);
	editor.setShowPrintMargin(false);

	editor.on("change",function(event){
	    console.log(jq_editor_box);
	    jq_editor_box.addClass("santa_clara_text_editor_box_modified");
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

	var form=jq_object.closest("form");
	var ta_name=jq_object.data("ta_name");
	var ta_id=jq_object.data("ta_id");

	form.submit( function(event){
	    var text=editor.getSession().toString();
	    var ta_html="<textarea name=\""+ta_name+"\"";
	    ta_html+=" id=\""+ta_id+"\">";
	    ta_html+=text;
	    ta_html+="</textarea>";
	    $(this).append(ta_html);
	    return true;
	});
    };

    var action_santa_clara_text_editor_button_simple=function(jq_object,event){
	var tag=jq_object.data("tag");
	var parent=jq_object.parent();
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
    };

    var action_santa_clara_text_editor_button_single=function(jq_object,event){
	var tag=jq_object.data("tag");
	var parent=jq_object.parent();
	var santa_clara_text_editor_id=parent.data("santa_clara_text_editor_id");
	var editor=EDITOR_DICT[santa_clara_text_editor_id];
	editor.insert("["+tag+"/]");
	editor.focus();
    };
    
    var action_santa_clara_text_editor_button_function=function(jq_object,event){
	var tag=jq_object.data("tag");
	var parent=jq_object.parent();
	var santa_clara_text_editor_id=parent.data("santa_clara_text_editor_id");
	var editor=EDITOR_DICT[santa_clara_text_editor_id];
	switch (tag) {
	case "action_upper": 
	    editor.toUpperCase();
	    break;
	case "action_lower": 
	    editor.toLowerCase();
	    break;
	case "action_bracket":
	    var range=editor.getSelectionRange();
	    editor.clearSelection();
	    editor.moveCursorTo(range.end.row,range.end.column,true);
	    editor.insert("]]");
	    editor.moveCursorTo(range.start.row,range.start.column,true);
	    editor.insert("[[");
	    editor.moveCursorTo(range.end.row,range.end.column+4,true);
	    editor.focus();
	}
    };

    /**/

    $(".santa_clara_text_editor").each(function(){
	set_santa_clara_text_editor($(this));
    });

    $(".santa_clara_text_editor_button_simple").click(function(event){
	event.preventDefault();
	action_santa_clara_text_editor_button_simple($(this),event);
    });

    $(".santa_clara_text_editor_button_single").click(function(event){
	event.preventDefault();
	action_santa_clara_text_editor_button_single($(this),event);
    });
    
    $(".santa_clara_text_editor_button_function").click(function(event){
	event.preventDefault();
	action_santa_clara_text_editor_button_function($(this),event);
    });

    /**/

    var mutationHandler = function (mutationRecords) {
	mutationRecords.forEach ( function (mutation) {
	    if (mutation.type!="childList") return;
	    if (mutation.addedNodes.length==0) return;

	    $(mutation.addedNodes).each(function(){

		$(this).find(".santa_clara_text_editor").each(function(){
		    set_santa_clara_text_editor($(this));
		});

		$(this).find(".santa_clara_text_editor_button_simple").click(function(event){
		    event.preventDefault();
		    action_santa_clara_text_editor_button_simple($(this),event);
		});
		
		$(this).find(".santa_clara_text_editor_button_single").click(function(event){
		    event.preventDefault();
		    action_santa_clara_text_editor_button_single($(this),event);
		});
		
		$(this).find(".santa_clara_text_editor_button_function").click(function(event){
		    event.preventDefault();
		    action_santa_clara_text_editor_button_function($(this),event);
		});

	    });

	});
    };

    var MutationObserver    = window.MutationObserver || window.WebKitMutationObserver;
    var myObserver          = new MutationObserver (mutationHandler);
    var obsConfig           = { childList: true, characterData: true, attributes: true, subtree: true };
    
    $("form").each( function () {
	myObserver.observe (this, obsConfig);
    });

    

});

