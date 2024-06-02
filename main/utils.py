from django.utils import timezone

def calculate_time_to_event(event_date):
    """
    Calculate time remaining until an event.
    Args:
        event_date: The date of the event.
    Returns:
        str: A string representing the time remaining until the event.
    """
    now = timezone.now()
    delta = event_date - now

    if delta.total_seconds() <= 0:
        return ""
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    time_to_event = ""

    if days > 0:
        time_to_event += f"- {days} days to event"
        return time_to_event
    if hours > 0:
        time_to_event += f"- {hours} hours to event"
        return time_to_event
    if minutes > 0:
        time_to_event += f"- {minutes} minutes event"
        return time_to_event
    
    return ""
