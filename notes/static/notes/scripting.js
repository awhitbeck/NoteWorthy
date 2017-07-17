function addHeader(){

	var header = document.getElementById( "header" );
	
	var title = document.createElement("a");
	title.href = "http://127.0.0.1:8000/notes/project-list";
	title.className = "plain";
	title.innerHTML = "<br><h1 style=\"font-family:'Lato'; font-size:60px;\">Note Thing</h1>";
	header.appendChild(title);

}

function toggleElement(id){
   	// get a reference to your element, or it's container
   	var myElement = document.getElementById(id);
   	// if element is not being displayed,
   	if( myElement.style.display == 'none' ){
   		// display it
   		myElement.style.display = '';
   	}else{
		// else, hide it
		myElement.style.display = 'none';
   	}
}
