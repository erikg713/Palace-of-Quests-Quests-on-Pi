// QuestProgressRequest.js
export class QuestProgressRequest {
  constructor(userId, questId, progress, completed = false) {
    this.userId = userId;
    this.questId = questId;
    this.progress = progress; // Progress percentage
    this.completed = completed; // Boolean flag for completion
  }
}

import { QuestProgressRequest } from '../models/QuestProgressRequest';

const progressRequest = new QuestProgressRequest(1, 101, 50, false);
console.log(progressRequest);
