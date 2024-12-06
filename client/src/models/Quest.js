// Quest Class
export class Quest {
  constructor(id, title, description, reward, progress = 0, completed = false) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.reward = reward; // XP or in-game items
    this.progress = progress; // Percentage of completion
    this.completed = completed;
  }

  // Mark quest as completed
  completeQuest() {
    this.progress = 100;
    this.completed = true;
  }
}

// Quest Progress Tracker
export class QuestProgress {
  constructor(questId, userId, progress, lastUpdated = new Date()) {
    this.questId = questId;
    this.userId = userId;
    this.progress = progress; // Progress percentage
    this.lastUpdated = new Date(lastUpdated);
  }
}
