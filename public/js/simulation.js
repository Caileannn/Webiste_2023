//// Simulation D3.js ////

async function main() {
	// Declare the chart dimensions and margins.
	data = await getJSON()

	// Number of Projects
	maxSections = (data.nodes).length

	// Node Variables
	let radius = 6
	let node_width = 800 / radius;

	// The force simulation mutates links and nodes, so create a copy
	// so that re-evaluating this cell produces the same result.
	const nodes = data.nodes.map(d => ({...d}));

	// Create a simulation with several forces.
	const simulation = d3.forceSimulation(nodes)
		.force("charge", d3.forceManyBody().strength(-150))
		.force("x", d3.forceX())
		.force("y", d3.forceY())
        .force("collision", d3.forceCollide().radius(node_width + 50).strength(0.01))
		.alpha(0.01)
		.alphaDecay(0)
		.velocityDecay(0.2);

	// Create the SVG container, and Center it.
	const svg = d3.create("svg")
		.attr("width", width)
		.attr("height", height)
		.attr("viewBox", [-width / 2, -height / 2, width, height])
		.attr("style", "max-width: 100%; height: auto;");
	
	const x = svg.append('g')

	const node = x
		.selectAll("images")
		.data(nodes)
		.enter()
		.append("image")
		.attr('width', function (d) {
			d.width = node_width
			return node_width
		})
		.attr("xlink:href", function (d) {
			return d.path
		})
		.attr("class", "node-gif")
		.on("mouseenter", function (d) {
			d3.select(this).transition().ease(d3.easeSin).duration(400).attr("width", node_width * 3);
			d3.select('.tooltip-name')
			.text(d.title)
			.style('display', 'block')
        })
        .on("mouseleave", function (d) {
			d3.select(this).transition().ease(d3.easeSin).duration(400).attr("width", node_width);
			d3.selectAll('.tooltip-name')
			.text(d.title)
			.style('display', 'none');
        })
		.on("click", function (event, d) {
			project_open = true;

			d3.selectAll('.tooltip-name')
			.text(d.title)
			.style('display', 'none');
			var move_to_selection = document.getElementById('slider-cont')
			var nav_bar = document.getElementById('flex-cont-url')
			move_to_selection.classList.add('notransition'); // Disable transitions
			move_to_selection.style.transform = 'translate(' + (parseInt(d.section) * -100 / maxSections) + '%)'
			move_to_selection.offsetHeight; // Trigger a reflow, flushing the CSS changes
			move_to_selection.classList.remove('notransition'); // Re-enable transitions
			
			var element = document.getElementById("project-cont");
			element.style.transform = "translate(0%, 0%)"
			element.style.animation = "fadein 1s ease-out"
			element.style.opacity = "1"
			element.style.display = "block"

			var element = document.getElementById("main-container");
			element.style.animation = "blurin 1.5s ease-out"
			element.style.filter = "blur(15px)"

			nav_bar.style.animation = "fadeout 1.5s ease-out"
			nav_bar.style.opacity = "0";
			nav_bar.style.pointerEvents = "none"
			document.getElementById("main-container").style.opacity = "0.2";

			var element = document.getElementById("content-exit-container")
			element.style.animation = "fadein 1.5s ease-out"
			element.style.opacity = 1

			// Set Index to Opened Project
			sectionIndex = parseInt(d.section)
        })
		.on("mouseover",  function (event, d) {
			// Get Position of Mouse/Node for Tooltip //
			let pos = d3.select(this).node().getBoundingClientRect();
			d3.select('.tooltip-name')
			.text(d.title)
			.style('top', pos.top + 'px')
			.style('left', pos.left + 'px');			
		})
		.on("pointerdown",  function (event, d) {
			// Get Position of Mouse/Node for Tooltip //
			let pos = d3.select(this).node().getBoundingClientRect();
			d3.select('.tooltip-name')
			.text(d.title)
			.style('display', 'block')
			d3.select(this).transition().ease(d3.easeSin).duration(400).attr("width", node_width * 3)			
		})
		.on("pointermove",  function (event, d) {
			// Get Position of Mouse/Node for Tooltip //
			let pos = d3.select(this).node().getBoundingClientRect();
			d3.select('.tooltip-name')
			.text(d.title)
			.transition()
			.style('top', pos.top + 'px')
			.style('left', pos.left + 'px');
		})
		.on("pointerup", function (event, d) {
			d3.select(this).transition().ease(d3.easeSin).duration(400).attr("width", node_width);
			d3.selectAll('.tooltip-name')
			.style('display', 'none');
		});

		
		
	container.append(svg.node())

	// Add a drag behavior.
	node.call(d3.drag()
		.on("start", dragstarted)
		.on("drag", dragged)
		.on("end", dragended));

	// Set the position attributes of links and nodes each time the simulation ticks.
	simulation.on("tick", () => {

	
	node
		.attr("x", function (d) {d.width = parseInt(d3.select(this).attr("width")); return d.x - d.width / 2})
		.attr("y", function (d) {d.width = parseInt(d3.select(this).attr("width")); return d.y - d.width / 2})
			
	simulation
		.force("collision", d3.forceCollide().radius(function (d) {return d.width + 50}).strength(0.01))
	});

	// Reheat the simulation when drag starts, and fix the subject position.
	function dragstarted(event) {
	 if (!event.active) simulation.alphaTarget(0.3).restart();
	event.subject.fx = event.subject.x;
	event.subject.fy = event.subject.y;
	}

	// Update the subject (dragged node) position during drag.
	function dragged(event) {
	event.subject.fx = event.x;
	event.subject.fy = event.y;
	}

	// Restore the target alpha so the simulation cools after dragging ends.
	// Unfix the subject position now that it’s no longer being dragged.
	function dragended(event) {
	if (!event.active) //simulation.alphaTarget(0);
	event.subject.fx = null;
	event.subject.fy = null;
	}

	setInterval(function(){simulation.alpha(0.1);},250);
}

async function fetchData() {
	return data = await getJSON()
}