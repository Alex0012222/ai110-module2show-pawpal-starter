# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - My design consist of having a calendar where users see all their Tasks. Works like a calendar and has O(1) runtime when trying to find the month/week/day but when it tries to look for a Task it has a O(n).
- What classes did you include, and what responsibilities did you assign to each?
  - I included Task -> Calendar -> User but Task has subclasses for different type of tasks, and User is being pointed by Pet and Availableschedule which are classes to handle the User's Availableschedule's set and the list of pets.
  - To break it down even further, Task has 5 subclasses (Petwalk, Feeding, Medication, VetVisit, and other). All of them share a Date and Time variable from Task. The most complex out of the bunch are Medication and VetVisit. The Medication class handles timesPerDay, drugName, doseCounter, and logDoseTaken(), VetVisit on the other hand only has requiredDocumenttion.
  - Calendar is another sophisticated class which handles the Schedule ( list(list(LinkedList<Task>)) ) and the currentTime (a string with a
    "xx-xx-xx" format).
  - User has a name, an AvailabilitySchedule set, and a Pet list.
  - Pet has name, age, favoriteFood, petType (string), foodRestrictions, and needGroom.
  - AvailabilitySchedule has an name, time, description, and duration.

**b. Design changes**

- Did your design change during implementation?
  - I had to make some changes because the logic was too complicated and hard to understand. When translating it to a real app, there were some aspects that made it
- If yes, describe at least one change and why you made it.
  I had to change the relationship between calendar and User. I also renamed everything so it aligns with step 2 planning

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
