import sys
from datetime import date, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Feeding, Owner, Pet, Scheduler

# ---------------------------------------------------------------------------
# Sorting Correctness
# ---------------------------------------------------------------------------


def test_sort_tasks_by_time_orders_earliest_first():
    scheduler = Scheduler()
    evening = Feeding(date(2026, 7, 8), time(18, 0), 10, "medium", "wet food")
    morning = Feeding(date(2026, 7, 8), time(8, 0), 10, "medium", "dry food")
    midday = Feeding(date(2026, 7, 8), time(12, 30), 10, "medium", "treat")

    ordered = scheduler.sort_tasks_by_time([evening, morning, midday])

    assert ordered == [morning, midday, evening]


def test_sort_tasks_by_priority_orders_high_medium_low():
    scheduler = Scheduler()
    low = Feeding(date(2026, 7, 8), time(8, 0), 10, "low", "dry food")
    high = Feeding(date(2026, 7, 8), time(9, 0), 10, "high", "wet food")
    medium = Feeding(date(2026, 7, 8), time(10, 0), 10, "medium", "treat")

    ordered = scheduler.sort_tasks_by_priority([low, high, medium])

    assert ordered == [high, medium, low]


def test_sort_tasks_by_completion_orders_incomplete_first():
    scheduler = Scheduler()
    done = Feeding(date(2026, 7, 8), time(8, 0), 10, "medium", "dry food")
    done.mark_complete()
    pending = Feeding(date(2026, 7, 8), time(9, 0), 10, "medium", "wet food")

    ordered = scheduler.sort_tasks_by_completion([done, pending])

    assert ordered == [pending, done]


def test_sort_tasks_by_priority_is_stable_for_equal_priority():
    scheduler = Scheduler()
    first = Feeding(date(2026, 7, 8), time(8, 0), 10, "medium", "A")
    second = Feeding(date(2026, 7, 8), time(9, 0), 10, "medium", "B")
    third = Feeding(date(2026, 7, 8), time(10, 0), 10, "medium", "C")

    ordered = scheduler.sort_tasks_by_priority([first, second, third])

    assert ordered == [first, second, third]


def test_sort_tasks_by_priority_pushes_unknown_priority_to_end():
    scheduler = Scheduler()
    high = Feeding(date(2026, 7, 8), time(8, 0), 10, "high", "wet food")
    medium = Feeding(date(2026, 7, 8), time(9, 0), 10, "medium", "treat")
    unknown = Feeding(date(2026, 7, 8), time(10, 0), 10, "", "dry food")

    ordered = scheduler.sort_tasks_by_priority([unknown, high, medium])

    assert ordered == [high, medium, unknown]


# ---------------------------------------------------------------------------
# Conflict Detection
# ---------------------------------------------------------------------------


def test_has_time_conflict_detects_overlapping_times():
    scheduler = Scheduler()
    existing_tasks = [(time(9, 0), 30)]

    result = scheduler.has_time_conflict(existing_tasks, time(9, 15), 30)

    assert result is True


def test_has_time_conflict_allows_back_to_back_tasks():
    scheduler = Scheduler()
    existing_tasks = [(time(9, 0), 30)]

    result = scheduler.has_time_conflict(existing_tasks, time(9, 30), 30)

    assert result is False


def test_has_time_conflict_flags_duplicate_start_time():
    scheduler = Scheduler()
    existing_tasks = [(time(9, 0), 30)]

    result = scheduler.has_time_conflict(existing_tasks, time(9, 0), 15)

    assert result is True

def test_has_time_conflict_returns_false_for_separate_times():
    scheduler = Scheduler()
    existing_tasks = [(time(9, 0), 30), (time(14, 0), 20)]

    result = scheduler.has_time_conflict(existing_tasks, time(11, 0), 60)

    assert result is False


if __name__ == "__main__":

    sorting_tests = [
        test_sort_tasks_by_time_orders_earliest_first,
        test_sort_tasks_by_priority_orders_high_medium_low,
        test_sort_tasks_by_completion_orders_incomplete_first,
        test_sort_tasks_by_priority_is_stable_for_equal_priority,
        test_sort_tasks_by_priority_pushes_unknown_priority_to_end,
    ]
    for index, test in enumerate(sorting_tests, start=3):
        if test():
            print(f"test {index} ..... passed")

    conflict_tests = [
        test_has_time_conflict_detects_overlapping_times,
        test_has_time_conflict_allows_back_to_back_tasks,
        test_has_time_conflict_flags_duplicate_start_time,
        test_has_time_conflict_returns_false_for_separate_times,
    ]
    for index, test in enumerate(conflict_tests, start=3 + len(sorting_tests)):
        if test():
            print(f"test {index} ..... passed")
