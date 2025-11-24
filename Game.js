class Game {
	constructor() {
		this.controls = new Controls();

		this.actor = new Actor(this.controls);
	}

	draw() {
		background(255);
		this.actor.draw();

		noFill();
		stroke(0);
		rect(10, 10, this.actor.boost * 100, 20);
	}

	run() {
		this.controls.run();

		this.actor.run();

		if (this.actor.dx === 0 && this.actor.dy === 0) {
			this.actor.y = 0;
			this.actor.boost = 1;
			for (let i = 0; i < punishAmount; i++) {
				exports.pop();
			}
		}
	}

	getState() {
		return this.actor.getState();
	}
	
	getInputs() {
		if (shouldSaveCanvas)
			saveCanvas();
		return this.controls.getOutputs();
	}
}