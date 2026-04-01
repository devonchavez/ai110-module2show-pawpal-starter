const mermaidDiagram = `
classDiagram
    class Owner {
        +String owner_name
        +int age
        +List~Pet~ pets
        +add_pet(Pet pet) void
        +remove_pet(Pet pet) void
        +list_pets() List~Pet~
        +get_all_tasks() List~Task~
        +get_pending_tasks() List~Task~
        +get_completed_tasks() List~Task~
    }

    class Pet {
        +String name
        +int age
        +String animal_type
        +String breed
        +String color
        +float weight
        +float height
        +String medical_conditions
        +Owner owner
        +List~Task~ tasks
        +describe() String
        +add_task(Task task) void
        +remove_task(Task task) void
        +list_tasks() List~Task~
        +incomplete_tasks() List~Task~
        +completed_tasks() List~Task~
    }

    class Task {
        +String description
        +String time
        +String frequency
        +int duration_minutes
        +String priority
        +bool completed
        +Pet pet
        +date due_date
        +mark_complete(bool reschedule) Task
        +mark_incomplete() void
        +is_recurring() bool
        +assign_pet(Pet pet) void
        +copy_for_next_occurrence(date due_date) Task
        +summary() String
    }

    class Scheduler {
        +List~Task~ tasks
        +String sort_by
        +add_task(Task task) void
        +get_tasks() List~Task~
        +add_pet_tasks(Pet pet) void
        +detect_conflicts(Task task) String
        +detect_same_time_conflicts() List~String~
        +filter_tasks(bool completed, String pet_name) List~Task~
        +complete_task(Task task, bool reschedule) Task
        +get_tasks_for_pet(Pet pet) List~Task~
        +get_tasks_for_owner(Owner owner) List~Task~
        +get_pending_tasks() List~Task~
        +get_completed_tasks() List~Task~
        +sort_tasks() void
        +schedule_for_pet(Pet pet, Task task) String
        +organize_by_pet() dict
        +task_summary() List~String~
    }

    Owner "1" <--> "*" Pet : owns
    Pet "1" o-- "*" Task : has
    Task "*" --> "0..1" Pet : assigned to
    Scheduler --> Task : manages
    Scheduler ..> Owner : queries for
`;

export default mermaidDiagram;
