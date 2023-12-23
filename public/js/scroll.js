//// Smooth Scroll Promise 🙏////

// Smooth Scroll Promise: Move to ScrollYPos -> Then do something //
function smoothScroll(elem) {
	// Variables for Target_Y & Offset
	let offset = 600;
	let targetPosition = 0;

	elem.scrollTo({
	  top: targetPosition,
	  behavior: 'smooth'
	});
	
	return new Promise((resolve, reject) => {
	  const failed = setTimeout(() => {
		reject();
	  }, 2000);
  
	  const scrollHandler = () => {
		if (elem.scrollTop < targetPosition + offset) {
		  window.removeEventListener("scroll", scrollHandler);
		  clearTimeout(failed);
		  resolve();
		}
	  }

	  if (elem.scrollTop < targetPosition + offset) {
		clearTimeout(failed);
		resolve();
	  } else {
		elem.addEventListener("scroll", scrollHandler);
	  }
	});
  }

// Example: Function to test the smoothScroll //
function smoothScrollTest() {
	// var p = smoothScroll(document.querySelector("#project-cont")).then(() => {
	// 	document.getElementById("project-cont").style.transform = "translate(0%, 0%)"
	// 	document.getElementById("project-cont").style.display = "none"
	// 	document.getElementById("project-cont").style.opacity = "0"

	// 	// If About is True, Then... Else, Return to Graph
	// 	if (about) {
	// 		document.getElementById("main-container").style.animation = "fadeout-about 1.5s ease-out"
	// 		document.getElementById("main-container").style.filter = "blur(0px)"
	// 		document.getElementById("main-container").style.opacity = "0";
	// 	} else if (index) {
	// 		document.getElementById("main-container").style.animation = "fadeout-about 1.5s ease-out"
	// 		document.getElementById("main-container").style.filter = "blur(0px)"
	// 		document.getElementById("main-container").style.opacity = "0";
	// 	} else {
	// 		document.getElementById("main-container").style.animation = "blurout 1.5s ease-out"
	// 		document.getElementById("main-container").style.filter = "blur(0px)"
	// 		document.getElementById("main-container").style.opacity = "1.0";
	// 	}
	// 	project_open = false;
	// });
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


