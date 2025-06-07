// Quest Class
export class Quest {
  /**
   * @param {string} id - Unique identifier for the quest.
   * @param {string} title - Title of the quest.
   * @param {string} description - Detailed description of the quest.
   * @param {string | number} reward - Reward for completing the quest (e.g., XP or items).
   * @param {number} progress - Progress percentage (default: 0).
   * @param {boolean} completed - Completion flag (default: false).
   */
  constructor(id, title, description, reward, progress = 0, completed = false) {
    if (!id || !title || !description || !reward) {
      throw new Error("Invalid input: All fields except progress and completed must be provided.");
    }

    this.id = id;
    this.title = title;
    this.description = description;
    this.reward = reward;
    this.progress = progress;
    this.completed = completed;
  }

  /**
   * Mark the quest as completed.
   */
  completeQuest() {
    this.progress = 100;
    this.completed = true;
    this.completionDate = new Date();
  }

  /**
   * Reset the progress of the quest.
   */
  resetProgress() {
    this.progress = 0;
    this.completed = false;
    delete this.completionDate;
  }

  /**
   * Update the progress of the quest.
   * @param {number} newProgress - New progress percentage.
   */
  updateProgress(newProgress) {
    if (newProgress < 0 || newProgress > 100) {
      throw new Error("Invalid progress: must be between 0 and 100.");
    }
    this.progress = newProgress;
    this.completed = newProgress === 100;
  }
}

// Quest Progress Tracker
export class QuestProgress {
  /**
   * @param {string} questId - ID of the associated quest.
   * @param {string} userId - ID of the user.
   * @param {number} progress - Progress percentage.
   * @param {Date | string} lastUpdated - Last updated timestamp (default: current date).
   */
  constructor(questId, userId, progress, lastUpdated = new Date()) {
    if (!questId || !userId || progress < 0 || progress > 100) {
      throw new Error("Invalid input: questId, userId, and progress must be valid.");
    }

    this.questId = questId;
    this.userId = userId;
    this.progress = progress;
    this.lastUpdated = new Date(lastUpdated);
  }

  /**
   * Update the progress and timestamp.
   * @param {number} newProgress - New progress percentage.
   */
  updateProgress(newProgress) {
    if (newProgress < 0 || newProgress > 100) {
      throw new Error("Invalid progress: must be between 0 and 100.");
    }
    this.progress = newProgress;
    this.lastUpdated = new Date();
  }
}
