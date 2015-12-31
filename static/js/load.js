marked.setOptions({
  renderer: new marked.Renderer(),
	gfm: true,
	tables: true,
	breaks: true,
	pedantic: true,
	sanitize: false, // IMPORTANT, because we do MathJax before markdown,
	                   //            however we do escaping in 'CreatePreview'.
	smartLists: true,
	smartypants: true,
});


var Preview = {
  		delay: 50,        // delay after keystroke before updating

  		preview: null,     // filled in by Init below
  		buffer: null,      // filled in by Init below

  		timeout: null,     // store setTimout id
  		mjRunning: false,  // true when MathJax is processing
  		oldText: null,     // used to check if an update is needed

  		//
  		//  Get the preview and buffer DIV's
  		//
  		Init: function () {
    		this.preview = document.getElementById("preview");
    		this.buffer = document.getElementById("previewbuffer");
  		},

  		//
		//  Switch the buffer and preview, and display the right one.
		//  (We use visibility:hidden rather than display:none since
		//  the results of running MathJax are more accurate that way.)
		//
  		SwapBuffers: function () {
        console.log('swaped');
    		var buffer = this.preview, preview = this.buffer;
    		this.buffer = buffer; this.preview = preview;
    		buffer.style.display = "none";
    		buffer.style.position = "absolute";
    		preview.style.position = ""; 
    		preview.style.display = "";
        highlight_code();
        center_image();
        $('a[href^="http"]').each(function(){
          $(this).attr('target', '_blank');
        });
        if ($("#is_grap").text().replace(/\n/g,'') == "ture") {
          swap_grap_block();
        };
  		},

  //
  //  This gets called when a key is pressed in the textarea.
  //  We check if there is already a pending update and clear it if so.
  //  Then set up an update to occur after a small delay (so if more keys
  //    are pressed, the update won't occur until after there has been 
  //    a pause in the typing).
  //  The callback function is set up below, after the Preview object is set up.
  //
  		Update: function () {
    		if (this.timeout) {clearTimeout(this.timeout)}
    		this.timeout = setTimeout(this.callback,this.delay);
  		},

  		//
  //  Creates the preview and runs MathJax on it.
  //  If MathJax is already trying to render the code, return
  //  If the text hasn't changed, return
  //  Otherwise, indicate that MathJax is running, and start the
  //    typesetting.  After it is done, call PreviewDone.
   
  		CreatePreview: function () {
    		Preview.timeout = null;
    		if (this.mjRunning) return;
    		var text = document.getElementById("writing").value;
    		if (text === this.oldtext) return;
    		text = this.Escape(text);                       //Escape tags before doing stuff
    		this.buffer.innerHTML = this.oldtext = text;
    		this.mjRunning = true;
    		MathJax.Hub.Queue(
      			["Typeset",MathJax.Hub,this.buffer],
      			["PreviewDone",this],
      			["resetEquationNumbers", MathJax.InputJax.TeX]
    		);
  		},

  //
  //  Indicate that MathJax is no longer running,
  //  do markdown over MathJax's result, 
  //  and swap the buffers to show the results.
  //
  		PreviewDone: function () {
          console.log('Preview Done');
          this.mjRunning = false;
          text = this.buffer.innerHTML;
      // replace occurrences of &gt; at the beginning of a new line
      // with > again, so Markdown blockquotes are handled correctly
          text = text.replace(/&gt;/mg, '>').replace(/&lt;/mg, '<').replace(/&#39;/g, "'");

          this.buffer.innerHTML = marked (text);
          if (location.pathname.slice(0, 5) == '/edit' || location.pathname.slice(0, 11) == '/share/edit') {
            this.SwapBuffers();
          };
  		},

  		Escape: function (html, encode) {
    		return html
      		.replace(!encode ? /&(?!#?\w+;)/g : /&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
      		.replace(/"/g, '&quot;')
     		.replace(/'/g, '&#39;');
  		}
	};

// Preview.callback = MathJax.Callback(["CreatePreview",Preview]);
// Preview.callback.autoReset = true;  // make sure it can run more than once
// Preview.callback = MathJax.Callback(["CreatePreview",Preview]);
// Preview.callback.autoReset = true;  // make sure it can run more than once
// Preview.Init();
// Preview.Update();

//
//  Cache a callback to the CreatePreview action
//