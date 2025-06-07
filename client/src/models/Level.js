// models/Level.js

/**
 * @class Level
 * Represents a player level in the Palace of Quests game.
 */
export class Level {
  /**
   * @param {number} levelNumber - The numeric level (must be >= 1).
   * @param {number} xpRequired - The required XP to reach this level (must be >= 0).
   * @param {Array<object>} rewards - Array of reward objects (optional).
   */
  constructor(levelNumber, xpRequired, rewards = []) {
    if (!Number.isInteger(levelNumber) || levelNumber < 1) {
      throw new TypeError('levelNumber must be an integer >= 1');
    }
    if (typeof xpRequired !== 'number' || xpRequired < 0) {
      throw new TypeError('xpRequired must be a non-negative number');
    }
    if (!Array.isArray(rewards)) {
      throw new TypeError('rewards must be an array');
    }

    this.levelNumber = levelNumber;
    this.xpRequired = xpRequired;
    this.rewards = [...rewards];
  }

  /**
   * Generates an array of Level instances.
   * @param {number} maxLevel - The highest level to generate.
   * @param {number|function} xpRule - Either a fixed XP increment per level, or a function that returns XP for a level.
   * @param {function} [rewardFn] - Optional function(levelNumber) => rewardArray.
   * @returns {Level[]}
   */
  static generateLevels(maxLevel, xpRule, rewardFn) {
    if (!Number.isInteger(maxLevel) || maxLevel < 1) {
      throw new TypeError('maxLevel must be an integer >= 1');
    }
    const xpIsFn = typeof xpRule === 'function';
    const levels = [];

    for (let i = 1; i <= maxLevel; i++) {
      const xp = xpIsFn ? xpRule(i) : i * xpRule;
      const rewards = typeof rewardFn === 'function' ? rewardFn(i) : [];
      levels.push(new Level(i, xp, rewards));
    }
    return levels;
  }

  /**
   * Adds a reward to this level.
   * @param {object} reward
   */
  addReward(reward) {
    this.rewards.push(reward);
  }

  /**
   * Removes a reward by index.
   * @param {number} index
   */
  removeRewardAt(index) {
    if (index >= 0 && index < this.rewards.length) {
      this.rewards.splice(index, 1);
    }
  }

  /**
   * Returns a shallow copy of the rewards array.
   * @returns {Array<object>}
   */
  getRewards() {
    return [...this.rewards];
  }
}

export default Level;
