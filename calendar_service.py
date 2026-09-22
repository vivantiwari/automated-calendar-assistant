import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional

def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO datetime string with timezone awareness."""
    clean_str = dt_str.replace('Z', '+00:00')
    try:
        dt = datetime.fromisoformat(clean_str)
        if dt.tzinfo is None:
            dt = dt.astimezone()
        return dt
    except ValueError:
        # Fallback for standard date-time string
        dt = datetime.strptime(clean_str[:19], "%Y-%m-%dT%H:%M:%S")
        return dt.astimezone()


class CalendarService:
    """
    Self-Contained In-Memory Calendar Service.
    Does NOT require Google Cloud credentials or OAuth tokens.
    Implements all standard calendar operations:
    - create_event
    - get_events
    - check_availability
    - find_free_slot
    """
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self._next_id = 1
        self._seed_default_events()

    def _seed_default_events(self):
        """Seed initial default events for demonstration."""
        now = datetime.now(timezone.utc).astimezone()
        today_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
        today_10am = today_9am + timedelta(hours=1)
        today_2pm = now.replace(hour=14, minute=0, second=0, microsecond=0)
        today_230pm = today_2pm + timedelta(minutes=30)

        self.events = [
            {
                "id": "event_1",
                "summary": "Team Standup",
                "start": today_9am.isoformat(),
                "end": today_10am.isoformat(),
                "description": "Daily sync with development team"
            },
            {
                "id": "event_2",
                "summary": "Client Catchup",
                "start": today_2pm.isoformat(),
                "end": today_230pm.isoformat(),
                "description": "Status update call"
            }
        ]
        self._next_id = 3

    def get_events(self, time_min: Optional[str] = None, time_max: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve calendar events within specified datetime window."""
        now = datetime.now(timezone.utc).astimezone()
        
        start_dt = parse_datetime(time_min) if time_min else now
        end_dt = parse_datetime(time_max) if time_max else start_dt + timedelta(days=7)

        results = []
        for ev in self.events:
            ev_start = parse_datetime(ev["start"])
            ev_end = parse_datetime(ev["end"])
            if ev_end > start_dt and ev_start < end_dt:
                results.append(ev)
        return results

    def check_availability(self, start_time: str, end_time: str) -> Dict[str, Any]:
        """Check whether a requested time slot is free."""
        req_start = parse_datetime(start_time)
        req_end = parse_datetime(end_time)

        if req_start >= req_end:
            return {"available": False, "reason": "End time must be after start time."}

        existing_events = self.get_events(
            time_min=req_start.isoformat(),
            time_max=req_end.isoformat()
        )

        conflicts = []
        for ev in existing_events:
            ev_start = parse_datetime(ev["start"])
            ev_end = parse_datetime(ev["end"])
            
            # Check overlap
            if req_start < ev_end and req_end > ev_start:
                conflicts.append(ev)

        if conflicts:
            return {
                "available": False,
                "conflicts": conflicts,
                "message": f"Conflict detected with {len(conflicts)} existing event(s)."
            }

        return {
            "available": True,
            "conflicts": [],
            "message": "Time slot is available."
        }

    def find_free_slot(self, date_str: str, duration_minutes: int = 30) -> Dict[str, Any]:
        """Find an available free slot on a specific date (between 9 AM and 6 PM)."""
        try:
            target_date = parse_datetime(date_str).date()
        except Exception:
            target_date = datetime.now(timezone.utc).astimezone().date()

        local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        work_start = datetime.combine(target_date, datetime.min.time()).replace(hour=9, minute=0, tzinfo=local_tz)
        work_end = datetime.combine(target_date, datetime.min.time()).replace(hour=18, minute=0, tzinfo=local_tz)

        day_events = self.get_events(
            time_min=work_start.isoformat(),
            time_max=work_end.isoformat()
        )

        current_candidate = work_start
        step = timedelta(minutes=30)
        slot_duration = timedelta(minutes=duration_minutes)

        while current_candidate + slot_duration <= work_end:
            candidate_end = current_candidate + slot_duration
            
            is_free = True
            for ev in day_events:
                ev_start = parse_datetime(ev["start"])
                ev_end = parse_datetime(ev["end"])
                if current_candidate < ev_end and candidate_end > ev_start:
                    is_free = False
                    current_candidate = max(current_candidate + step, ev_end)
                    break

            if is_free:
                return {
                    "found": True,
                    "start_time": current_candidate.isoformat(),
                    "end_time": candidate_end.isoformat(),
                    "duration_minutes": duration_minutes,
                    "date": target_date.isoformat()
                }

        return {
            "found": False,
            "message": f"No free slot of {duration_minutes} minutes available on {target_date.isoformat()} between 9 AM and 6 PM."
        }

    def create_event(self, summary: str, start_time: str, end_time: str, description: str = "") -> Dict[str, Any]:
        """Create a new calendar event after checking for conflicts."""
        avail = self.check_availability(start_time, end_time)
        if not avail["available"]:
            req_start = parse_datetime(start_time)
            req_end = parse_datetime(end_time)
            duration = int((req_end - req_start).total_seconds() / 60)
            if duration <= 0:
                duration = 30
            
            alt_slot = self.find_free_slot(date_str=start_time, duration_minutes=duration)
            
            return {
                "status": "conflict",
                "message": "The requested time slot is occupied by an existing event.",
                "conflicts": avail.get("conflicts", []),
                "suggested_slot": alt_slot
            }

        req_start_dt = parse_datetime(start_time)
        req_end_dt = parse_datetime(end_time)

        event_id = f"event_{self._next_id}"
        self._next_id += 1

        new_event = {
            "id": event_id,
            "summary": summary,
            "start": req_start_dt.isoformat(),
            "end": req_end_dt.isoformat(),
            "description": description
        }
        self.events.append(new_event)

        return {
            "status": "success",
            "event": new_event
        }
