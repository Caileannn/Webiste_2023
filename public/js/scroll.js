// Example: Function to test the smoothScroll //
function smoothScrollTest() {
	var slider_cont = document.getElementsByClassName('section')
	for(let i = 0; i < slider_cont.length; i++)
	{
		slider_cont[i].scrollTo({
			top: 0,
			behavior: 'instant'
		});
	}

	document.getElementById("project-cont").style.transform = "translate(0%, 0%)"
	// document.getElementById("project-cont").style.animation = "fadeout 1.5s ease-out"
	document.getElementById("project-cont").style.opacity = "0"
	document.getElementById("project-cont").style.display = "none"

	// If About is True, Then... Else, Return to Graph
	if (about) {
		document.getElementById("main-container").style.animation = "fadeout-about 1.5s ease-out"
		document.getElementById("main-container").style.filter = "blur(0px)"
		document.getElementById("main-container").style.opacity = "0";
	} else if (index) {
		document.getElementById("main-container").style.animation = "fadeout-about 1.5s ease-out"
		document.getElementById("main-container").style.filter = "blur(0px)"
		document.getElementById("main-container").style.opacity = "0";
	} else {
		document.getElementById("main-container").style.animation = "blurout 1.5s ease-out"
		document.getElementById("main-container").style.filter = "blur(0px)"
		document.getElementById("main-container").style.opacity = "1.0";
	}
	project_open = false;
}


