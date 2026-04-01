# PawPal+ Project Reflection

3 core user controlled actions
1. track pet information
- The app should take in as much information about the pet like name, animal type, breed, age, weight, color, feeding schedule, and any known conditions to give recomendations on when to do medical checkups/ how to medically keep up with their pet, maybe a reminder after a checkup to re enter any new infomration about the pet
2. generate a weekly do list
- the app should let the user put in a lists of tasks to be completed throughout the week and sort each tasks based off of importance, certain repetetive tasks like "take out pet", or "feed pet" will automatically be scheduled for each day of the week
3. social media aspect?
- The user is allowed to take a "picture of the day" for their pet aslong as right a little note to caption the photo.

Owner
- age, name

Pet
- age, name, color, animal type, breed, weight, height, any living conditions

Task 
- user input, time?, how urgent the task is

Scheduler
- takes in tasks, option to sort by how urgent or time of day

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I ended up including owner, pet, task, and scheduler as classes. 

Ownder, takes in owners age.

Pet, takes in pet name, age, color, animal type, animal breed, weight, height, and any medical conditions

Task, takes in a description, time, and how urgent the task is

Scheduler, creates a list of tasks, adds and sorts tasks

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
