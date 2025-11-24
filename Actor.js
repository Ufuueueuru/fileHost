class Actor {
	constructor(controls) {
		this.controls = controls;

		this.boost = 1;
		this.rotation = PI + 0.3;
		this.dx = 0;
		this.dy = 0;
		this.x = 0;
		this.y = 0;

		this.targetX = 0;
		this.targetY = 0;
		this.targetdx = 0;
		this.targetdy = 0;
		this.targetGood = true;
	}

	draw() {
		push();
		translate(200, 0);
		translate(this.dx, this.y);
		rotate(this.rotation - PI);

		fill(0);
		noStroke();
		rect(-20, -10, 40, 20);
		
		pop();

		push();
		if (this.targetGood) {
			fill(0, 150, 0);
		} else {
			fill(150, 0, 0);
		}
		rect(this.targetX - 10, this.targetY - 10, 20, 20);
		
		pop();
	}

	run() {
		this.targetX += this.targetdx - this.dx / 100;
		this.targetY += this.targetdy;

		this.targetX = constrain(this.targetX, 0, 400);
		this.targetY = constrain(this.targetY, 50, 350);
		
		let hit = dist(this.targetX, this.targetY, 200 + this.dx, this.y) < 30;
		if (this.targetX <= 0 || hit) {
			if (hit && this.targetBad) {
				for (let i = 0; i < punishAmount; i++) {
					exports.pop();
				}
			}
			this.targetX = 400;
			this.targetY = random(50, 350);
			this.targetdx = random(-2, -1);
			this.targetdy = random(-3, 3);
			this.targetGood = random(0, 1) > 0.5;
		}

		
		if (this.controls.right) {
			this.rotation -= 0.05;
			if (this.rotation < PI / 2)
				this.rotation = PI / 2;
		}
		if (this.controls.left) {
			this.rotation += 0.05;
			if (this.rotation > 3 * PI / 2)
				this.rotation = 3 * PI / 2;
		}

		this.dy += 1;
		
		this.dx *= 0.95;
		this.dy *= 0.95;

		let speed = dist(0, 0, this.dx, this.dy) + (this.controls.boost ? 0.1 : 0);
		
		let tempX = this.dx / speed;
		let tempY = this.dy / speed;
		let rotX = cos(this.rotation - PI);
		let rotY = sin(this.rotation - PI);

		let dot = tempX * rotX + tempY * rotY;
		speed = (dot + 0.05) * speed;
		let newDir = (atan2(this.dy, this.dx) + PI / 2 + this.rotation * 10) / 11;
		if (this.controls.boost && this.boost > 0) {
			speed += 5 / 8;
			this.dy -= 1 / 16;
			this.boost -= 1 / 256;
		}
		if (!this.controls.boost) {
			this.boost += 1 / 256;
		}
		this.boost = constrain(this.boost, 0, 1);
		this.dx = cos(newDir - PI) * speed;
		this.dy = sin(newDir - PI) * speed;

		this.dy += 2;

		this.dx = constrain(this.dx, -50, 50);
		this.dy = constrain(this.dy, -5, 5);
		
		this.x += this.dx;
		this.y += this.dy;

		this.y = constrain(this.y, 0, 400);
		
		if (this.y >= 400) {
			this.dy = 0;
			this.dx = 0;
		}
		this.dy = constrain(this.dy, -5, 5);
		this.rotation = (this.rotation % (2 * PI) + 2 * PI) % (2 * PI);
	}

	getState() {
		return {
			y: round(this.y / 400 * 256) / 256,
			dy: round((this.dy + 5) / 10 * 256) / 256,
			dx: round((this.dx + 50) / 100 * 256) / 256,
			rotation: round((this.rotation - PI / 2) / PI * 256) / 256,
			boost: round(this.boost * 256) / 256,
			targetX: round(this.targetX / 400 * 256) / 256,
			targetY: round((this.targetY - 50)  / 300 * 256) / 256,
			targetdx: round((this.targetdx + 2) * 256) / 256,
			targetdy: round((this.targetdy + 3) / 6 * 256) / 256,
			targetGood: this.targetGood ? 1 : 0
		};
	}
}