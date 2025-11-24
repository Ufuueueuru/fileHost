class Controls {
	constructor() {
		this.right = false;
		this.left = false;

		this.boost = false;
	}

	run() {
		this.right = keyIsDown(37);
		this.left = keyIsDown(39);
		this.boost = keyIsDown(32);
	}

	getOutputs() {
		return {
			right: this.right ? 1 : 0,
			left: this.left ? 1 : 0,
			boost: this.boost ? 1 : 0
		}
	}
}