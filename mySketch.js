let shouldSaveCanvas = false;

let game;

let buffer = -60;

let punishAmount = 100;

let exports = [];

let loaded = false;

let model;

function setup() {
	createCanvas(400, 400);
	background(100);

	game = new Game();

	setTimeout(async () => {
		// let text = await loadStrings("https://ufuueueuru.github.io/fileHost/flightGameData.json");
		// let json = JSON.parse(text);

		// stateLabels = []
		// for u in data[0]["state"]:
  // 			stateLabels.append(u)

		// allStates = []
		// for i in data:
		//   current = {}
  // 		for u in i["state"]:
  // 		  current[u] = i["state"][u]
  // 		allStates.append(current)

		// df = pd.DataFrame(allStates)
		
		
		model = await tf.loadLayersModel('https://ufuueueuru.github.io/fileHost/model/model.json');
		//print(model.predict([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	
		loaded = true;
	});
}

function draw() {
	if (loaded) {
		//buffer++;

		
		
		game.draw();
	
		game.run();
	
		
		//if (buffer > 0) {
		//	let inputs = game.getInputs();
		//	if ((inputs.right || inputs.left || inputs.boost) || random(0, 1) > 0.2) {
		//		exports.splice(floor(random(0, exports.length)), 0, {state: game.getState(), inputs: inputs});
		//	}
		//}
	
		//fill(0);
		//noStroke();
		//text(exports.length, 20, 50);
	
		//if (exports.length === 100000) {
			//print(exports);
		//	download(JSON.stringify(exports));
		//}
	}
}

function keyPressed(e) {
	if (e.key === "A") {
		print(exports);
	}
}