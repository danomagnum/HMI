var DEBUG = 0;
var DEBUG_NOREFRESH = 0;

function find_parent(element){
	p = element.parentElement;
	if (p){
		if (p.classList.contains('parent')){
			return resolve_child_path(p);
		}else{
			return find_parent(p);
		};
	}else{
		return '';

	};
};

function resolve_child_path(element){
	var tagpath = "";
	if (element.hasAttribute("data-target")){
		tagpath = element.getAttribute("data-target");
	}else{
		return "";
	};

	if (element.classList.contains('child')){
		return find_parent(element) + "." + tagpath;

	}else{
		return tagpath;

	};

};


function update_element_bulk(element, response){
	// This function is like the other update element function but
	// the response here will have the driver/ at the beginning of the tag path.
	// The goal is to have less requests to the base server by combining them.
	var tagpath = element.getAttribute("data-target");
	var prefix = ""
	if (element.hasAttribute("data-prefix")){
		prefix = element.getAttribute("data-prefix");
	}
	var postfix = ""
	if (element.hasAttribute("data-postfix")){
		postfix = element.getAttribute("data-postfix");
	}
	var tagname = tagpath;
	var newdata =  response[tagname];

	if (newdata == undefined){
		return;
	};


	if (element.classList.contains('parent')){
		var subelements = element.getElementsByClassName("subitem");
		[].forEach.call(subelements, function(subelement) {
		update_element(subelement, newdata);
		});
	}else{
		if (element.hasAttribute("value")){
			if (document.activeElement == element) return;
			element.value = newdata;
		}else if(element.hasAttribute("data-value")){
			element.setAttribute("data-value", newdata);
		}else{
			if (Array.isArray(newdata)){
				element.innerHTML = "";
				newdata.forEach(function(item){
					element.innerHTML += prefix;
					element.innerHTML += item;
					element.innerHTML += postfix;
				})
			}else{
				element.innerHTML = "";
				element.innterHTML += prefix;
				element.innerHTML += newdata;
				element.innterHTML += postfix;
			}

		}
		if (element.classList.contains("multistate_indicator")){
			update_indicator(element);
		}
		if (element.classList.contains("graph")){
			update_graph(element);
		}
	}

	if (element.hasAttribute("onchange")){
		element.onchange();
	}

};



function update_element(element, response){
	var tagpath = element.getAttribute("data-target");
	var prefix = ""
	if (element.hasAttribute("data-prefix")){
		prefix = element.getAttribute("data-prefix");
	}
	var postfix = ""
	if (element.hasAttribute("data-postfix")){
		postfix = element.getAttribute("data-postfix");
	}
	var tagname = tagpath.substring(tagpath.indexOf('/') + 1);
	var newdata =  response[tagname];


	if (element.classList.contains('parent')){
		var subelements = element.getElementsByClassName("subitem");
		[].forEach.call(subelements, function(subelement) {
		update_element(subelement, newdata);
		});
	}else{
		if (element.hasAttribute("value")){
			element.value = newdata;
		}else if(element.hasAttribute("data-value")){
			element.setAttribute("data-value", newdata);
		}else{
			if (Array.isArray(newdata)){
				element.innerHTML = "";
				newdata.forEach(function(item){
					element.innerHTML += prefix;
					element.innerHTML += item;
					element.innerHTML += postfix;
				})
			}else{
				element.innerHTML = "";
				element.innterHTML += prefix;
				element.innerHTML += newdata;
				element.innterHTML += postfix;
			}

		}
		if (element.classList.contains("multistate_indicator")){
			update_indicator(element);
		}
		if (element.classList.contains("graph")){
			update_graph(element);
		}
	}

	if (element.hasAttribute("onchange")){
		element.onchange();
	}

};

function add_datapoint(element){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function() {
		if (this.readyState == 4 && this.status == 200) {
			var response = JSON.parse(this.responseText);
			update_element(element, response);
		}
	};

	xmlhttp.overrideMimeType("application/json");
	var path =  "/read/" + element.getAttribute("data-target");
	xmlhttp.open("GET", path);
	xmlhttp.send(null);
};

function refresh_all_data(response){
	var elements = document.getElementsByClassName("autoload_value");

	[].forEach.call(elements, function(element) {
		update_element_bulk(element, response);
	});
};



function get_all_datapoints(){
	var elements = document.getElementsByClassName("autoload_value");
	paths = [];
	[].forEach.call(elements, function(element){
		path = element.getAttribute("data-target");
		if (path !== null){
			paths.push(path);
		};
	});
	//for (element in elements){
		//e = elements[element];
		//paths.push(elements[element].getAttribute("data-target"));
	//}

	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function() {
		if (this.readyState == 4 && this.status == 200) {
			var response = JSON.parse(this.responseText);
			refresh_all_data(response);
		}
	};

	xmlhttp.overrideMimeType("application/json");
	var path =  "/read_multi/"
	xmlhttp.open("POST", path);
	xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(paths));
};




function refresh_data(){
	var elements = document.getElementsByClassName("autoload_value");

	[].forEach.call(elements, function(element) {
		add_datapoint(element);
	});
};

function update_indicator(element){
	var sel = element.selectedIndex;
	if (sel == -1){
		//Something went wrong with the index
		return
	}
	var newclass = element.options[element.selectedIndex].className;

	//element.className = "multistate_indicator";
	element.className = element.getAttribute("data-baseclass");

	if (newclass){
		element.classList.add(newclass);
	};
}


function shiftContext(ctx, w, h, dx, dy) {
	var clamp = function(high, value) { return Math.max(0, Math.min(high, value)); };
	var imageData = ctx.getImageData(clamp(w, -dx), clamp(h, -dy), clamp(w, w-dx), clamp(h, h-dy));
	ctx.clearRect(0, 0, w, h);
	ctx.putImageData(imageData, 0, 0);
}


function update_graph(element){
	var ctx = element.getContext( "2d" );
	var w = element.width;
	var h = element.height;
	var shift = 1;
	var y0 = 0;
	var y1 = 0;
	var val = parseFloat(element.innerHTML);
	var secs = 60;
	var pencolor = "#000000";


	if (element.hasAttribute("data-pencolor")){
		pencolor = element.getAttribute("data-pencolor") ;
	}

	if (element.hasAttribute("data-secs")){
		secs = element.getAttribute("data-secs") ;
	}
	shift = w / secs;
	
	if (! element.hasAttribute("data-y0")){
		if ( element.hasAttribute("data-min")){
			y0 = element.getAttribute("data-min") ;
		}

		if (val < y0){
			element.setAttribute("data-min", val);
		}
	}else{
		y0 = element.getAttribute("data-y0");
	}
	
	if (! element.hasAttribute("data-y1")){
		if (element.hasAttribute("data-max")){
			y1 = element.getAttribute("data-max") ;
		}

		if (val > y1){
			element.setAttribute("data-max", val);
		}
	}else{
		y1 = element.getAttribute("data-y1");
	}



	var last = element.getAttribute("data-last");

	var dy = y1 - y0;


	var drawpos = (val - y0) / dy * h;

	shiftContext(ctx, w, h, -shift, 0);   
	ctx.beginPath();
	ctx.moveTo(w-shift,last);
	ctx.lineTo(w, drawpos);
	ctx.strokeStyle = pencolor;
	ctx.stroke();

	element.setAttribute("data-last", drawpos);

}



function setup_indicators(){
	var elements = document.getElementsByClassName("multistate_indicator");
	[].forEach.call(elements, function(element) {
		/* logic here */
		element.setAttribute("onchange", "update_indicator(this)");
		element.setAttribute("data-baseclass", element.className);
		update_indicator(element);

		if (!DEBUG){
			element.setAttribute('disabled', 1);
		};
	});

};

function pb_momentary_press(element){
	var xmlhttp = new XMLHttpRequest();
	target = resolve_child_path(element)

	var path =  "/write/" + target
	var params = 'value=' + element.getAttribute("data-press");
	xmlhttp.open("POST", path, true);
	xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	xmlhttp.send(params);
}

function pb_momentary_release(element){
	var xmlhttp = new XMLHttpRequest();
	target = resolve_child_path(element)
	var path =  "/write/" + target
	var params = 'value=' + element.getAttribute("data-release");
	xmlhttp.open("POST", path, true);
	xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	xmlhttp.send(params);
}

function pb_toggle(element){
	target = resolve_child_path(element)
	if (element.value == element.getAttribute("data-press")){
		element.value = element.getAttribute("data-release");
	}else{
		element.value = element.getAttribute("data-press");
	}

	var xmlhttp = new XMLHttpRequest();
	var path = "/write/" + target
	var params = 'value=' + element.value;
	xmlhttp.open("POST", path, true);
	xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	xmlhttp.send(params);
}

function input_submit(element){
	target = resolve_child_path(element)
	

	var xmlhttp = new XMLHttpRequest();
	var path = "/write/" + target
	var params = 'value=' + element.value;
	xmlhttp.open("POST", path, true);
	xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	xmlhttp.send(params);
};

function setup_inputs(){
	var elements = document.getElementsByTagName("input");
	[].forEach.call(elements, function(element) {
		/* logic here */
		/*element.setAttribute("onchange", "input_submit(this)");*/
		element.addEventListener("keyup", event=>{
			if (event.key !== "Enter") return;
			input_submit(element);
		});
	});
};




function setup_buttons(){
	var elements = document.getElementsByClassName("pb_momentary");
	[].forEach.call(elements, function(element) {
		/* logic here */
		if (! element.hasAttribute("data-press")){
			element.setAttribute("data-press", "1");
		}
		if (! element.hasAttribute("data-release")){
			element.setAttribute("data-release", "0");
		}

		element.setAttribute("onmousedown", "pb_momentary_press(this)");
		element.setAttribute("onmouseup", "pb_momentary_release(this)");
	});

	var elements = document.getElementsByClassName("pb_toggle");
	[].forEach.call(elements, function(element) {
		/* logic here */
		if (! element.hasAttribute("data-press")){
			element.setAttribute("data-press", "1");
		}
		if (! element.hasAttribute("data-release")){
			element.setAttribute("data-release", "0");
		}
		if (! element.hasAttribute("value")){
			element.value = 0;
		}

		add_datapoint(element);
		element.setAttribute("onclick", "pb_toggle(this)");

		//element.setAttribute("onmousedown", "pb_momentary_press(this)");
		//element.setAttribute("onmouseup", "pb_momentary_release(this)");
	});

};


function update_all(){
	//refresh_data();
	get_all_datapoints()
}

function startup(){
	setup_indicators();
	setup_buttons();
	setup_inputs();
	refresh_data();
	if (! DEBUG_NOREFRESH){
		setInterval(update_all, 500);
	}
}

