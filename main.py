from pawpal_system import *


def test_from_step_2():
    favorite_food : set[str] = ("Tuna cans", "Canip")
    Loki : Pet = Pet("loki","3", favorite_food, None, None)
    Goido : Pet = Pet("Goido", "2", favorite_food, None, None)
    all_pets : list[Pet] = []
    all_pets.append(Loki)
    all_pets.append(Goido)
    Alex : Owner = Owner("Alex", all_pets)
    feeding = Feeding(date(2026,7,7), time(11,0), "cat food")
    walk = PetWalk(date(2026,7,7), time(12,0), 30, 1.5)
    meds = Medication(date(2026,7,7), time(13,0), "Meloxicam", 1)
    vet = VetVisit("Dentist cat visit", "Loki needs a detist check up",
                   date(2026,7,7), time(13,0), "vaccine report", 60)
    Loki.add_task(feeding)
    Loki.add_task(walk)
    Loki.add_task(meds)
    Loki.add_task(vet)

    Goido.add_task(feeding)
    Goido.add_task(walk)
    Goido.add_task(meds)

    Alex.get_todays_tasks(date(2026,7,7))



