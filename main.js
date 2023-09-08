/// Define Variables ///
const width = window.innerWidth;
const height = window.innerHeight;

// Main Container Element //
const container = document.getElementById('main-container');

// What is Open Booleans //
var about = false;
var project_open = false;

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
		about = false
	} else {
		about = true
	}
	aboutFadeIn(about)
}

function aboutFadeIn(e) {
	var element = document.getElementById("main-container");
	var about_cont = document.getElementById("about-text-cont")
	if (!e) {
		element.style.animation = "fadein 1.5s ease-out"
		element.style.opacity = 1
		about_cont.style.animation = "fadeout 2s ease-out"
		about_cont.style.opacity = 0
		about_cont.style.zIndex = 100
	} else {
		element.style.animation = "fadeout 2s ease-out"
		element.style.opacity = 0
		about_cont.style.display = "inline"
		about_cont.style.animation = "fadein 1.5s ease-out"
		about_cont.style.opacity = 1.0
		about_cont.style.zIndex = 300
		// Check if Project Window Open, If Yes toggle Window
		if (project_open) {
			smoothScrollTest()
		}
	}
}

// Show Graph //
function showGraph() {
	var element = document.getElementById("main-container");
	var about_cont = document.getElementById("about-text-cont")

	// If About open..
	if (about) {
		element.style.animation = "fadein 1.5s ease-out"
		element.style.opacity = 1
		about_cont.style.animation = "fadeout 2s ease-out"
		about_cont.style.opacity = 0
		about_cont.style.zIndex = 100
		about = false;
	}

	// If Project open..
	if (project_open) {
		smoothScrollTest()
	}
}

// Show Graph //
function showGraphMobile() {
	if(window.innerWidth <= 768){
		var element = document.getElementById("main-container");
		var about_cont = document.getElementById("about-text-cont")

		// If About open..
		if (about) {
			element.style.animation = "fadein 1.5s ease-out"
			element.style.opacity = 1
			about_cont.style.animation = "fadeout 2s ease-out"
			about_cont.style.opacity = 0
			about_cont.style.zIndex = 100
			about = false;
		}

		// If Project open..
		if (project_open) {
			smoothScrollTest()
		}
	}
}

function textToClipboard() {
	// Get the text field
	var copyText = document.getElementById("email-text");
	navigator.clipboard.writeText(copyText.innerText);
}

/// Event Listeners ///

// Listen for Click -> Close Project Window If Open //
addEventListener("click", (evt) => {
	var class_name = evt.target.classList[0]
	if(class_name == "section" || class_name == "s-emoji" || class_name == null ){
		if (project_open) {
			smoothScrollTest()
			var nav_bar = document.getElementById('flex-cont-url')
			nav_bar.style.animation = "fadein 1.5s ease-out"
			nav_bar.style.opacity = "1";
			nav_bar.style.pointerEvents = "auto"
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
// Reveal/Hide Graph when Header is selected //
document.getElementById("name-cont").addEventListener("click", showGraph);
// Reveal/Hide Graph when Header is selected //
document.getElementById("emoji-cont").addEventListener("click", showGraphMobile);

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




