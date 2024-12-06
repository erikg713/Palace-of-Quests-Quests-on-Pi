// Level Class
export class Level {
  constructor(levelNumber, xpRequired, rewards = []) {
    this.levelNumber = levelNumber;
    this.xpRequired = xpRequired;
    this.rewards = rewards; // Array of Reward objects
  }

  static generateLevels(maxLevel, xpIncrement) {
    // Dynamically generate levels
    const levels = [];
    for (let i = 1; i <= maxLevel; i++) {
      levels.push(new Level(i, i * xpIncrement));
    }
    return levels;
  }
}
