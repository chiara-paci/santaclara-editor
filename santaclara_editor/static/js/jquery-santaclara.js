(function($){
 

    /****
	 <form ...>
	 ...
	 <div id="{{div_id}}">{{text}}</div>
	 ...
	 </form>
         <script type="text/javascript">
             $("#{{div_id}}").santa_clara_editor({
                 textarea_id: "{{ta_id}}",
                 textarea_name: {{form_field_name}}"
             });
         </script>'

	 Il form al momento del submit si ritroverà con un campo del tipo:

	 <textarea name="{{form_field_name}}" id="{{ta_id}}">{{text}}</textarea>

     ****/

    $.widget("sc.santa_clara_editor",{
	options: {
	    editor_rows: 50,
	    editor_cols: 100,
	    textarea_id: "",
	    textarea_name: "",
	    update_rate: 2000
	},

	_create: function(){
	    var self=this;
	    var el=self.element;
	    var opts=self.options;
	    var old_html;
	    var html="";
	    var prefix=el.attr("id");
	    var ta_id;

	    /* variables */
	    if (prefix) { prefix+="-"; }
	    prefix+="sc-editor-";
	    if (opts.textarea_id)
		ta_id=opts.textarea_id;
	    else
		ta_id=prefix+"textarea";

	    if ($("#"+ta_id+"-resizable").length) 
		old_html=self.get_text();
	    else
		old_html=el.html();

	    /* DOM */

	    if (!old_html) old_html="\n";

	    if (opts.textarea_name) {
		html+='<label id="'+ta_id+'-label" for="label_'+opts.textarea_name+'"></label>';
	    }
	    html+=self._toolbar(prefix,ta_id+"-editable");
	    html+='<div id="'+ta_id+'-resizable"><div id="'+ta_id+'-editable" class="santa-clara-textarea"';
	    html+='>'+self._syntax_highlight(old_html)+'</div></div>';
	    el.html(html);
	    $("#"+ta_id+"-editable").attr("contenteditable","true");
	    $("#"+ta_id+"-resizable").resizable({alsoResize: "#"+ta_id+'-editable',
						 minHeight: 200,
						 minWidth: 200});
	    $("#"+ta_id+"-editable").css({"height":opts.editor_rows+'em',
	    				  "width":opts.editor_cols+'%'});
	    $("#"+ta_id+"-resizable").css({
		"padding-bottom":'1em',
		"padding-right":'2em'
	    });

	    /* attributes */

	    this.textarea_id=ta_id+"-editable";
	    this.last_modify_time=0;

	    /* form submit */

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

	    /* toolbar events */

	    el.find('a[data-type="simple"]').click(function(event){
		var tag=$(this).data("tag");
		event.preventDefault();
		self._on_selection_add_tag("["+tag+"]","[/"+tag+"]");
	    });

	    el.find('a[data-type="single"]').click(function(event){
		var tag=$(this).data("tag");
		event.preventDefault();
		self._at_cursor_insert_text("["+tag+"/]");
	    });

	    el.find('a[data-type="function"]').click(function(event){
		var tag=$(this).data("tag");

		var actions={
		    "action_upper": function(text){  
			return text.toUpperCase();
		    },
		    "action_lower": function(text){  
			return text.toLowerCase();
		    }
		};
		self._on_selection_exec_function(actions[tag]);
	    });

	    /* cut/copy/paste event */

	    $("#"+this.textarea_id).bind("cut paste",function(event){
		self.last_modify_time=$.now();
		setTimeout(function(){
		    var when_typed=$.now();
		    if (when_typed>self.last_modify_time) 
			self.update_syntax_highlight();
		    
		},opts.update_rate);
	    });

	    /* keyboard event */

	    $("#"+this.textarea_id).keypress(function(event){
		if (event.which==0) return;
		var special= [ "<", ">", "Enter" ];

		self.last_modify_time=$.now();
		
		setTimeout(function(){
		    var when_typed=$.now();
		    if (when_typed>self.last_modify_time) 
			self.update_syntax_highlight();
		},opts.update_rate);
		
		if (jQuery.inArray(event.key,special)==-1) return;
		event.preventDefault();

		switch (event.key) {
		case "<":
		    self._at_cursor_insert_text("&lt;");
		    return;
		case ">":
		    self._at_cursor_insert_text("&gt;");
		    return;
		case "Enter":
		    self._at_cursor_insert_text("\n");
		    return;
		};

	    });

	}, // _create

	_toolbar: function(prefix,ta_id){
	    var html="";
	    var buttons=[
		{tag:"left", tooltip: "align left",type:"simple",
		 txt: '<i class="editor-button fa fa-align-left"></i>' }, 
		{tag:"center", tooltip:"align center",type:"simple",
		 txt:'<i class="editor-button fa fa-align-center"></i>' },
		{tag:"right", tooltip:"align right",type:"simple",
		 txt:'<i class="editor-button fa fa-align-right"></i>' },
		{tag:"justify", tooltip:"justify",type:"simple",
		 txt:'<i class="editor-button fa fa-align-justify"></i>' },
		{tag:"sep"},
		{tag:"vspace", tooltip:"add vertical space",type:"single",
		 txt:'<i class="editor-button fa fa-resize-vertical"></i>' },
		{tag:"hspace", tooltip:"add horizontal space",type:"single",
		 txt:'<i class="editor-button fa fa-resize-horizontal"></i>' },
		{tag:"sep"},
		{tag:"b", tooltip:"bold",type:"simple",
		 txt:'<b><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">B</span></b>' },
		{tag:"i", tooltip:"italic",type:"simple",
		 txt:'<i><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">I</span></i>' },
		{tag:"s", tooltip:"linethrough",type:"simple",
		 txt:'<span class="editor-button linethrough" style="padding-left:.2em;padding-right:.2em;">S</span>' },
		{tag:"u", tooltip:"underline",type:"simple",
		 txt:'<span class="editor-button underline" style="padding-left:.2em;padding-right:.2em;">U</span>' },
		{tag:"o", tooltip:"overline",type:"simple",
		 txt:'<span class="editor-button overline" style="padding-left:.2em;padding-right:.2em;">O</span>' },
		{tag:"t", tooltip:"terminal type",type:"simple",
		 txt:'<tt><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">T</span></tt>' },
		{tag:"sc", tooltip:"smallcaps",type:"simple",
		 txt:'<span class="editor-button smallcaps" style="padding-left:.2em;padding-right:.2em;">SC</span>' },
		{tag:"sep"},
		{tag:"code",  tooltip:"code",     type:"simple",txt:'<i class="editor-button fa fa-file"></i>' },
		{tag:"term",  tooltip:"terminal", type:"simple",txt:'<i class="editor-button fa fa-desktop"></i>' },
		{tag:"quote", tooltip:"quote",    type:"simple",txt:'<i class="editor-button fa fa-quote-right"></i>' },
		{tag:"sep"},
		{tag:"action_upper", tooltip:"upper case",type:"function",txt:'a⇾A' },
		{tag:"action_lower", tooltip:"lower case",type:"function",txt:'A⇾a' }
	    ];

	    html='<div class="santa-clara-toolbar">';
	    buttons.forEach(function(b){
		if (b.tag=="sep") {
		    html+=' <span class="hspace" style="padding-left:.5em;"></span>';
		    return;
		}
		html+=' <a id="'+prefix+b.tag+'" data-target="'+ta_id+'" data-tag="'+b.tag+'"';
		html+=' data-type="'+b.type+'" href=""';
		html+=">";
		html+=b.txt+'<span class="tooltip">'+b.tooltip+'</span></a>';
	    });
	    html+="</div>";
	    return html;
	}, // _toolbar

	/*** syntax highlight ***/
	
	_remove_syntax_highlight: function(text){
	    var patt_tag=new RegExp("<.*?>","gi");
	    var ret=text;
	    ret=text.replace(patt_tag,"");
	    ret=ret.replace("&gt;",">");
	    ret=ret.replace("&lt;","<");
	    return ret;
	},

	_syntax_highlight: function(text){
	    var patt_open=new RegExp("\\[([a-zA-Z0-9]+)([^a-zA-Z0-9\\]].*?[^/])\\]","gi");
	    var patt_open_simple=new RegExp("\\[([a-zA-Z0-9]+)\\]","gi");
	    var patt_close=new RegExp("\\[/([a-zA-Z0-9]+)\\]","gi");
	    var patt_single=new RegExp("\\[([a-zA-Z0-9]+)([^a-zA-Z0-9\\]]?.*?)/\\]","gi");
	    var patt_return=new RegExp("\\n","gi");
	    var ret=text;
	    ret=ret.replace("<","&lt;");
	    ret=ret.replace(">","&gt;");
	    ret=ret.replace(patt_single,'<span class="santa-clara-syntax-highlight santa-clara-sh-$1">[$1$2/]</span>');
	    ret=ret.replace(patt_open,'<span class="santa-clara-syntax-highlight santa-clara-sh-$1">[$1$2]');
	    ret=ret.replace(patt_open_simple,'<span class="santa-clara-syntax-highlight santa-clara-sh-$1">[$1]');
	    ret=ret.replace(patt_close,'[/$1]</span>');
	    return ret;
	},

	/*** cursor positions ***/

	_get_selection: function(test_balancing,all) {
	    var start=-1;
	    var end=-1;
	    var savedRange;

	    if ('undefined' === typeof all)
		all=false;

	    if ('undefined' === typeof test_balancing)
		test_balancing=false;

	    if(window.getSelection)  //non IE Browsers
		savedRange = window.getSelection().getRangeAt(0);
	    else if(document.selection) //IE
		savedRange = document.selection.createRange();  
	    else {
		ret = { 
		    start: -1,
		    start_container: null,
		    end: -1,
		    end_container: null,
		    equals: true
		};
		if (all) ret.single=true;
		return ret;
	    }

	    var jq_ancestor=$(savedRange.commonAncestorContainer);
	    var ret;

	    if ( (jq_ancestor.attr("id")!=this.textarea_id) &&
		 ( $('#'+this.textarea_id).has(jq_ancestor).length == 0 ) ) {
		ret = { 
		    start: -1,
		    start_container: null,
		    end: -1,
		    end_container: null,
		    equals: true
		};
		if (all) ret.single=true;
		if (test_balancing) ret.balanced=true;
		return ret;
	    }

	    if (savedRange.startContainer == savedRange.endContainer) {
		ret = { 
		    equals: true,
		    start: savedRange.startOffset,
		    start_container: $(savedRange.startContainer),
		    end: savedRange.endOffset
		};
		ret.end_container=ret.start_container;
		if (all) ret.single=true;
		if (test_balancing) ret.balanced=true;
		return ret;
	    }

	    ret = { 
		equals: false,
		start: savedRange.startOffset,
		start_container: $(savedRange.startContainer),
		end: savedRange.endOffset,
		end_container: $(savedRange.endContainer)
	    };

	    if ((!test_balancing)&&(!all)) return ret;

	    var next=savedRange.startContainer;
	    var prev=savedRange.endContainer;
	    var s_sibling=new Array();
	    var e_sibling=new Array();
	    var s_num=0,e_num=0;
	    var s_balanced=true,e_balanced=true;

	    s_sibling[s_num]=savedRange.startContainer;
	    e_sibling[e_num]=savedRange.endContainer;

	    while ( next.nextSibling ) {
		if (next==savedRange.endContainer) break;
		if ($(next).has($(savedRange.endContainer)).length != 0){
		    s_balanced=false;
		    break;
		}  
		s_num+=1;
		next=next.nextSibling;
		s_sibling[s_num]=next;
	    }
	    s_num+=1;

	    while ( prev.previousSibling ) {
		if (prev==savedRange.startContainer) break;
		if ($(prev).has($(savedRange.startContainer)).length != 0){
		    e_balanced=false;
		    break;
		}  
		prev=prev.previousSibling;
		e_num+=1;
		e_sibling[e_num]=prev;
	    }
	    e_num+=1;
	    e_sibling.reverse();

	    ret = { 
		equals: false,
		start: savedRange.startOffset,
		start_container: $(savedRange.startContainer),
		end: savedRange.endOffset,
		end_container: $(savedRange.endContainer)
	    };

	    if (test_balancing) ret.balanced=s_balanced && e_balanced;

	    if (!all) return ret;
	    ret.single=false;
	    if (!s_balanced) {
		ret.all_container=s_sibling;
		ret.num_container=s_num;
	    }
	    else {
		ret.all_container=e_sibling;
		ret.num_container=e_num;
	    }
	    return ret;

	},

	_get_cursor: function() {
	    var savedRange;

	    if(window.getSelection) { //non IE Browsers
		savedRange = window.getSelection().getRangeAt(0);
	    }
	    else if(document.selection) {//IE
		savedRange = document.selection.createRange();  
	    } 

	    var jq_ancestor=$(savedRange.commonAncestorContainer);
	    var ret;

	    if ( (jq_ancestor.attr("id")!=this.textarea_id) &&
		 ( $('#'+this.textarea_id).has(jq_ancestor).length == 0 ) ) {
		ret = { 
		    pos: -1,
		    container: null,
		};
		return ret;
	    }

	    if ( $(savedRange.startContainer).attr("id")!=this.textarea_id ) {
		ret = { 
		    pos: savedRange.startOffset,
		    container: $(savedRange.startContainer),
		};
		return ret;
	    }

	    this.set_text("\n");
	    return this._get_cursor();

	},

	_set_cursor: function(container,pos){
	    var sel;
	    $("#"+this.textarea_id).focus();
	    if (document.selection) {
		document.selection.createRange();  
	    }
	    else {
		sel = window.getSelection();
	    }
	    if (!$.isArray(container)) {
		if ($(container).length)
		    sel.collapse(container,pos);
		return;
	    }

	    console.log("set_cursor",container,pos);

	    switch (container.length) {
	    case 1:
		console.log($(container[0]).text().length);
		sel.collapse(container[0],pos);
		break;
	    case 2:
		sel.collapse(container[1],0);
		break;
	    case 3:
		sel.collapse(container[2],0);
		break;
	    default:
		console.log(container.length);
		console.log(container);
		sel.collapse(container[2],0);
	    }
	},

	_split_contents_at_pos: function(parent,container,pos) {
	    var prev=new Array();
	    var next=new Array();
	    var inner,split;
	    var in_next=false;
	    var contents=parent.contents();
	    var i;
	    for (i=0;i<contents.length;i++){
		if (in_next) {
		    next.push($(contents[i]));
		    continue;
		};
		if (contents[i].nodeType==3) {
		    if (contents[i]==container.get(0)){
			inner=$(contents[i]);
			in_next=true;
			continue;
		    }
		    prev.push($(contents[i]));
		    continue
		}
		if ($(contents[i]).has(container).length!=0){
		    split=this._split_contents_at_pos($(contents[i]),container,pos);
		    prev=prev.concat(split.prev);
		    next=split.next;
		    inner=split.inner;
		    in_next=true;
		    continue;
		}
		prev.push($(contents[i]));
	    };
	    
	    return({next:next,prev:prev,inner:inner});

	},

	_split_text_at_pos: function(container,pos) {
	    var text_prev="";
	    var text_next="";
	    var i;
	    
	    if (!container) return {prev:"",next:""};

	    var text=container.text();
	    split=this._split_contents_at_pos($("#"+this.textarea_id),container,pos);
	    for(i=0;i<split.prev.length;i++) text_prev+=split.prev[i].text();
	    text_prev+=text.substring(0,pos);
	    text_next=text.substring(pos,text.length);
	    for(i=0;i<split.next.length;i++) text_next+=split.next[i].text();
	    return {prev:text_prev,next:text_next};
	},

	_split_contents_by_text: function(parent,text_prev,text_next){
	    var container=null;
	    var pos=0;
	    var i;
	    var prev_L=text_prev.length;
	    var next_L=text_next.length;
	    var contents=parent.contents();
	    var new_prev_text="";
	    var new_next_text="";
	    var in_next=false;
	    var text,obj;

	    obj=contents[0];

	    for(i=0;i<contents.length;i++) {
		text=$(contents[i]).text();
		if (in_next) {
		    new_next_text+=text;
		    continue;
		}
		if (new_prev_text.length+text.length<=prev_L){
		    new_prev_text+=text;
		    continue;
		}
		obj=contents[i];
		in_next=true;
	    }

	    if (!in_next){
		obj=contents[contents.length-1];
		container=$(obj);
		text=$(obj).text();
		pos=new_prev_text.length;
		return ({container:container,pos:pos});
	    }

	    if (obj.nodeType==3) {
		text=$(obj).text();
		container=$(obj);
		pos=text_prev.length-new_prev_text.length;
		return ({container:container,pos:pos});
	    }

	    return this._split_contents_by_text($(obj),text_prev.substring(new_prev_text.length,text_prev.length),
						text_next.substring(0,text_next.length-new_next_text.length));
	},

	/*** manipulate selection ***/

	_at_cursor_insert_text: function(text){
	    var cursor=this._get_cursor();
	    var L, old_text, new_text, new_node;
	    var visual_length=$("<div/>").html(text).text().length;

	    if (cursor.pos==-1) return;

	    console.log("ACIT0",cursor);

	    L = cursor.container.text().length;
	    old_text = cursor.container.text();
	    new_text=old_text.substring(0,cursor.pos) + text + old_text.substring(cursor.pos,L);
	    new_text=this._remove_syntax_highlight(new_text);
	    new_text=this._syntax_highlight(new_text);

	    new_node=jQuery.parseHTML(new_text);
	    cursor.container.replaceWith(new_node);

	    console.log("ACIT",L,cursor.pos+visual_length);
	    
	    this._set_cursor(new_node,cursor.pos+visual_length);

	},

	_on_selection_exec_function: function(callable) {
	    var text_area=$("#"+this.textarea_id);
	    var L = text_area.html().length;
	    var old_text = text_area.html();
	    var sel=this._get_selection(all=true);

	    if (sel.start==-1) return;
	    if (sel.end==-1) return;

	    // QUI quando _get_selection si deciderà a ritornare un elenco con all=true
	    return;

	    var new_text = old_text.substring(0,sel.start) + callable(old_text.substring(sel.start,sel.end)) + old_text.substring(sel.end,L);

	    new_text=this._remove_syntax_highlight(new_text);
	    new_text=this._syntax_highlight(new_text);

	    text_area.html(new_text);
	}, // _exec_function_on_selection

	_on_selection_add_tag: function(open_tag,close_tag) {
	    var sel=this._get_selection(test_balancing=true,all=false);

	    if (sel.start==-1) return;

	    if (sel.equals && (sel.start==sel.end)){
		this._at_cursor_insert_text(open_tag+close_tag);
		return;
	    }

	    var L, old_text, new_text, new_node, visual_length, text;
	    var visual_length;


	    if (sel.equals) {
		L = sel.start_container.text().length;
		old_text = sel.start_container.text();
		text=open_tag + old_text.substring(sel.start,sel.end) + close_tag;
		visual_length=$("<div/>").html(text).text().length;
		new_text=old_text.substring(0,sel.start) + text + old_text.substring(sel.end,L);
		new_text=this._remove_syntax_highlight(new_text);
		new_text=this._syntax_highlight(new_text);
		new_node=jQuery.parseHTML(new_text);
		sel.start_container.replaceWith(new_node);
		this._set_cursor(new_node,sel.start+visual_length);
		return;
	    }

	    if (!sel.balanced) return;

	    L = sel.start_container.text().length;
	    old_text = sel.start_container.text();
	    new_text=old_text.substring(0,sel.start) + open_tag + old_text.substring(sel.start,L);
	    sel.start_container.replaceWith(new_text);

	    L = sel.end_container.text().length;
	    old_text = sel.end_container.text();
	    text=old_text.substring(0,sel.end) + close_tag;
	    visual_length=$("<div/>").html(text).text().length;
	    new_text=text + old_text.substring(sel.end,L);
	    new_node=jQuery.parseHTML(new_text);
	    sel.end_container.replaceWith(new_node);
	    this._set_cursor(new_node,visual_length);

	    this.update_syntax_highlight();

	}, // _on_selection_add_tag

	/*** world interface ***/

	set_text: function(text) {
	    $("#"+this.textarea_id).html(this._syntax_highlight(text));
	},

	get_text: function() {
	    var dtext=$("#"+this.textarea_id).get(0);
	    var text=$("#"+this.textarea_id).text();
	    text=this._remove_syntax_highlight(text);
	    return text;
	},

	update_syntax_highlight: function() {
	    var cursor=this._get_cursor();
	    
	    console.log("USH0",cursor);
	    
	    if ($(cursor.container).attr("id")==this.textarea_id) {
		console.log("USH2");
		this.set_text("\n");
		return;
	    }
	    var cfr_text=this._split_text_at_pos(cursor.container,cursor.pos);
	    this.set_text(this.get_text());
	    var new_cursor=this._split_contents_by_text($("#"+this.textarea_id),cfr_text.prev,cfr_text.next);
	    console.log("USH1",new_cursor);
	    this._set_cursor(new_cursor.container.get(0),new_cursor.pos);
	}



    });

    /****/
 
})(jQuery);