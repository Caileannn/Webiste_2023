/// Define Variables ///
const width = window.innerWidth;
const height = window.innerHeight;

// Main Container Element //
const container = document.getElementById('main-container');
const index_cont = document.getElementById('index-text-cont');
const about_cont = document.getElementById('about-text-cont');

// What is Open Booleans //
var about = false
var index = false
var project_open = false

// JSON Data //
let data;

/// HTML Elements ///

// Hands 👉 //
const hand_R = document.querySelector("#hand-r");
const hand_L = document.querySelector("#hand-l");

// Get Center Position of Hands //
const arrowCenterR = getCenter(hand_R);
const arrowCenterL = getCenter(hand_L);

// Simulation 🌎 //
main()
subpage()

// Get Center of 👉's //
function getCenter(element) {
    const {left, top, width, height} = element.getBoundingClientRect();
    return {x: left + width / 2, y: top + height / 2}
}

// Open/Close About //
function aboutToggle() {
	// If Open...
	if (about) {
		closeActivatePages()
	} else {
		about = true
		closeActivatePages('about')
		fadeInPage('about')
	}
}

function indexToggle() {
	// If Open..
	if (index) {
		closeActivatePages()
	} else {
		index = true
		closeActivatePages('index')
		fadeInPage('index')
	}
}

// Close any active pages except the parameter passed through
function closeActivatePages(p) {
	// Check each page to see if active
	// project, about, index
	if (project_open) {
		smoothScrollTest()
	}

	if (about && (p != 'about')) {
		fadeOutPage('about')
	}

	if (index && (p != 'index')) {
		fadeOutPage('index')
	}

	fadeGraph()
}

// Fade in or our graph based on active elements
function fadeGraph() {
	var element = document.getElementById("main-container");
	if (!project_open && !about && !index) {
		element.style.animation = "fadein 1.5s ease-out"
		element.style.opacity = 1	
	} else {
		element.style.animation = "fadeout 2s ease-out"
		element.style.opacity = 0
	}
}

function fadeInPage(id) {
	// Fade In
	if (id == 'index') {
		var index_cont = document.getElementById("index-text-cont")
		index_cont.style.display = "inline"
		index_cont.style.animation = "fadein 1.5s ease-out"
		index_cont.style.opacity = 1.0
		index_cont.style.zIndex = 300
	}

	if (id == 'about') {
		var about_cont = document.getElementById("about-text-cont")
		about_cont.style.display = "inline"
		about_cont.style.animation = "fadein 1.5s ease-out"
		about_cont.style.opacity = 1.0
		about_cont.style.zIndex = 300
	}
	
}

function fadeOutPage(id) {
	// Fade Out
	if (id == 'index') {
		var index_cont = document.getElementById("index-text-cont")
		index_cont.style.animation = "fadeout 2s ease-out"
		index_cont.style.opacity = 0
		index_cont.style.zIndex = 100
		index = false
	}

	if (id == 'about') {
		var about_cont = document.getElementById("about-text-cont")
		about_cont.style.animation = "fadeout 2s ease-out"
		about_cont.style.opacity = 0
		about_cont.style.zIndex = 100
		about = false
	}
	
}

function textToClipboard() {
	// Get the text field
	var copyText = document.getElementById("email-text");
	navigator.clipboard.writeText(copyText.innerText);
}

// Listen for clik on exit, close project window if open //
addEventListener("click", (evt) => {
	if(evt.target == document.getElementById("content-exit-container")){
		if (project_open) {
			smoothScrollTest()
			var nav_bar = document.getElementById('flex-cont-url')
			nav_bar.style.animation = "fadein 1.5s ease-out"
			nav_bar.style.opacity = "1";
			var exit = document.getElementById("content-exit-container")
			exit.style.animation = "fadeout 1.5s ease-out"
			exit.style.opacity = 0;
			setTimeout(() => {
				nav_bar.style.pointerEvents = "auto"
				
			}, 1500);
		}
	}
})

// Listen for Click -> Close Project Window If Open //
addEventListener("touchstart", (evt) => {
	var class_name = evt.target.classList[0]
	if(class_name == "section" || class_name == "s-emoji" || class_name == null ){
		if (project_open) {
			smoothScrollTest()
			var nav_bar = document.getElementById('flex-cont-url')
			nav_bar.style.animation = "fadein 1.5s ease-out"
			nav_bar.style.opacity = "1";
			var exit = document.getElementById("content-exit-container")
			exit.style.animation = "fadeout 1.5s ease-out"
			exit.style.opacity = 0;
			setTimeout(() => {
				nav_bar.style.pointerEvents = "auto"
				
			}, 1500);
			
		}
	}
});

// Listen for Mouse Movement -> Move 👉 //
addEventListener("mousemove", ({clientX, clientY}) => {
    var angleR = Math.atan2(clientY - arrowCenterR.y, clientX - arrowCenterR.x);
    hand_R.style.transform = `rotate(${angleR}rad)`;
	var angleL = Math.atan2(clientY - arrowCenterL.y, clientX - arrowCenterL.x);
    hand_L.style.transform = `rotate(${angleL}rad)`;
});

// Revea/Hidel About Section & Graph //
document.getElementById("about-cont").addEventListener("click", aboutToggle);
// Revea/Hidel Index Section & Graph //
document.getElementById("index-cont").addEventListener("click", indexToggle);
// Reveal/Hide Graph when Header is selected //
document.getElementById("name-cont").addEventListener("click", closeActivatePages);
// Reveal/Hide Graph when Header is selected //
if (window.innerWidth <= 768) { document.getElementById("emoji-cont").addEventListener("click", closeActivatePages) }


addEventListener("click", (evt) => {
	if(evt.target == document.getElementById("email-arrow")){
		textToClipboard()
	}
})

// Read in JSON promise //
async function getJSON() {
	let jsondata;    
	const response = await fetch('./data.json');
	jsondata = await response.json();
	return jsondata
}




