
async function subpage() {
	// What project is it (see by URL) //
	try {
		var subpage = window.location.pathname

		// Locate project in data // 
		let json = await fetchData()

		if(subpage == "/") {
			
		} else {
			json.nodes.every(element => {
				if(subpage.match(element.subpage)) {
	
					// Activate Initial Transform, No Animation // 
					project_open = true;
	
					var move_to_selection = document.getElementById('slider-cont')
					move_to_selection.classList.add('notransition'); // Disable transitions
					move_to_selection.style.transform = 'translate('+(element.section * -50)+'%)'
					move_to_selection.offsetHeight; // Trigger a reflow, flushing the CSS changes
					move_to_selection.classList.remove('notransition'); // Re-enable transitions
					
					var element = document.getElementById("project-cont");
					element.classList.add('notransition');
					element.style.transform = "translate(0%, 0%)"
					element.offsetHeight; // Trigger a reflow, flushing the CSS changes
					element.classList.remove('notransition'); // Re-enable transitions
	
					var element = document.getElementById("main-container");
					element.classList.add('notransition');
					element.style.animation = "blurin 1.5s ease-out"
					element.style.filter = "blur(15px)"
					document.getElementById("main-container").style.opacity = "0.2";
					element.offsetHeight; // Trigger a reflow, flushing the CSS changes
					element.classList.remove('notransition'); // Re-enable transitions
	
					return false
				}
	
				return true
			});
		}
	} catch {
		console.log("Home Page")
	}
	


}