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

Some constraints that my scheduler considers is when certain tasks overlap eachother. I thought that this mattered most because when making a schedule I thought that it be most important to be meticulous and accurate to something that is able to fit your schedule. When you have tasks that you need to complete that arent accuratley planned out it can cause stalls and if youre responsible for a pet its important that they have an accurate schedule aswell.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

For on of my warning detection methods in scheduluer AI initially created a "loaded" method which used nested if statements and for loops and was able to simplify the algorithim to a single for loop but the tradeoff was that the new detection algorithim now alowed for some overlap instead of exact time detections. I think the tradeoff could be reasonable if youre looking for faster and storage safe code.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ai for refactoring, im new to using streamlit and had AI plug in the attributes of my classes into my app file. Initially it would only plug in certain methods into my app and i had to direct the AI to plug in methods i needed if i watned certain features like being able to mark tasks as complete or delete certain tasks.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I had to delete suggestions where it would trying creating its own "app sesssion" for when the program ran in my pawpal systems file since the app WAS the session started when the program ran. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
Im 8/10 confident that it works correctly. I think an edge case I would test would be to see what would happen if there were too many tasks that overlapped and maybe creating a an auto task adjuster algorithim that is able to fix the schedule according to the warnings being output.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Im really satisfied with my sorting algorithim, its really simple clean and easy to read and is able to sort the generated schedule in multiple categories.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve my UI wiring from my pawpal system file. I think what I had noticed was that initially AI wasnt pluggin in all methods that I had expected for certain fetures like being able to edit tasks and had to ask how to implement those in a way that i wanted it to (having users be able to edit tasks if a warning popped up)


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I think I learned more about what its really like to create software, Ive always been hesitant on starting a project but the process of creating the logic, having test files, creating ui to interact with the program was broken down pretty well and I hope transfers over for when I start my own project.