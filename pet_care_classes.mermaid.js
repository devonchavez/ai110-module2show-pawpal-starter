const mermaidDiagram = `
classDiagram
    class Owner {
        +int age
        +String name
    }

    class Pet {
        +int age
        +String name
        +String color
        +String animalType
        +String breed
        +float weight
        +float height
        +String livingConditions
    }

    class Task {
        +String description
        +String time
        +String urgency
    }

    class Scheduler {
        +Task[] tasks
        +String sortBy
        +void addTask(Task task)
        +Task[] getTasks()
    }

    Owner "1" o-- "*" Pet : owns
    Scheduler --> Task : manages
    Scheduler ..> Pet : schedules for
`;

export default mermaidDiagram;
