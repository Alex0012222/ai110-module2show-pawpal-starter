import sys
from datetime import date, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Feeding, Owner, Pet, Scheduler


def _make_owner_with_pet():
    pet = Pet("Loki", "3")
    owner = Owner("Alex", [pet])
    return owner, pet


def test_add_task_appends_to_pets_task_list_in_chronological_order():
    owner, pet = _make_owner_with_pet()
    scheduler = Scheduler()
    evening_feeding = Feeding(date(2026, 7, 8), time(18, 0), "wet food")
    morning_feeding = Feeding(date(2026, 7, 8), time(8, 0), "dry food")

    scheduler.add_task(owner, pet, evening_feeding)
    scheduler.add_task(owner, pet, morning_feeding)

    assert pet.get_task() == [morning_feeding, evening_feeding]
    return True


def test_complete_task_marks_it_done_and_removes_it_from_pets_list():
    owner, pet = _make_owner_with_pet()
    scheduler = Scheduler()
    feeding = Feeding(date(2026, 7, 8), time(8, 0), "dry food")
    scheduler.add_task(owner, pet, feeding)

    result = scheduler.complete_task(owner, pet, feeding)

    assert result is True
    assert feeding.get_is_complete() is True
    return True


if __name__ == "__main__":
    test1 = test_add_task_appends_to_pets_task_list_in_chronological_order()
    test2 = test_complete_task_marks_it_done_and_removes_it_from_pets_list()

    if test1:
        print("test 1 ..... passed")
    if test2:
        print("test 2 ..... passed")
