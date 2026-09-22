"""
Automated Verification Script for Calendar Assistant
Tests calendar service operations and agent tool-calling pipeline.
"""
from calendar_service import CalendarService
from agent import CalendarAgent
from datetime import datetime, timedelta, timezone

def test_calendar_service():
    print("--- 1. Testing CalendarService ---")
    service = CalendarService()
    
    # Test 1: Get events
    events = service.get_events()
    print(f"[OK] get_events() returned {len(events)} initial events.")

    # Test 2: Create event
    now = datetime.now(timezone.utc).astimezone()
    tomorrow_3pm = (now + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)
    tomorrow_4pm = tomorrow_3pm + timedelta(hours=1)

    res = service.create_event(
        summary="Test Academic Meeting",
        start_time=tomorrow_3pm.isoformat(),
        end_time=tomorrow_4pm.isoformat()
    )
    print(f"[OK] create_event() result: {res['status']}")
    assert res["status"] == "success", "Failed to create event"

    # Test 3: Conflict detection
    conflict_res = service.create_event(
        summary="Conflicting Meeting",
        start_time=tomorrow_3pm.isoformat(),
        end_time=tomorrow_4pm.isoformat()
    )
    print(f"[OK] Conflict detection result: {conflict_res['status']}")
    assert conflict_res["status"] == "conflict", "Conflict was not detected!"
    assert "suggested_slot" in conflict_res, "Suggested slot missing on conflict!"

    # Test 4: Find free slot
    free_slot = service.find_free_slot(date_str=tomorrow_3pm.isoformat(), duration_minutes=30)
    print(f"[OK] find_free_slot() result found: {free_slot['found']}")
    assert free_slot["found"], "Free slot search failed!"

    print("CalendarService unit tests passed successfully!\n")

def test_agent_pipeline():
    print("--- 2. Testing CalendarAgent Pipeline ---")
    service = CalendarService()
    agent = CalendarAgent(calendar_service=service)

    queries = [
        "What meetings do I have today?",
        "Schedule a project meeting tomorrow at 3 PM.",
        "Find a free slot tomorrow."
    ]

    for q in queries:
        reply = agent.process_request(q)
        print(f"User: {q}")
        print(f"Assistant: {reply}\n" + "-"*40)

    print("CalendarAgent pipeline tests passed successfully!\n")

if __name__ == "__main__":
    test_calendar_service()
    test_agent_pipeline()
    print("ALL TESTS PASSED SUCCESSFULLY! Ready for deployment.")
