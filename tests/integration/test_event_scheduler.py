from app.scheduler import EventScheduler

def test_schedule_daily_event():
    scheduler = EventScheduler()
    event = scheduler.schedule_event("daily_reward", {"reward": "100 Gold"}, interval="24h")
    assert event["status"] == "scheduled"
    assert event["interval"] == "24h"
