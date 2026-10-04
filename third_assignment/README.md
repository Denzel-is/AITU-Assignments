# Assignment #3 - Bridge Pattern

Topic: space missions. A simple Java console example with no external libraries.
Flights and mission tasks are simulated by printing messages.

Before submission, check that this topic was not used in your lecture and is
unique in your group. The repository alone cannot confirm these requirements.

## 1. The idea from scratch

There are two separate questions:

- **What do we do?** Explore a destination or deliver supplies. This is the mission type.
- **How do we travel?** Use a rocket or a shuttle. This is the transport implementation.

Any mission can use either transport:

| Mission type | Rocket | Shuttle |
| --- | --- | --- |
| Exploration | Yes | Yes |
| Cargo delivery | Yes | Yes |

Without Bridge, we could create a class for each combination, such as
`ExplorationWithRocket`, `ExplorationWithShuttle`, `CargoWithRocket`, and
`CargoWithShuttle`. Each new transport would require more combination classes.

Instead, missions and transports are separate. A mission holds a reference to a
transport and calls it through the common `SpaceTransport` interface.
This reference is the bridge between the two sides.

**Bridge allows mission types and transport implementations to evolve independently.**
Pattern reference: [Refactoring.Guru - Bridge](https://refactoring.guru/design-patterns/bridge).

## 2. Java basics used in this example

- **Class:** a description of an object. `RocketTransport` describes a rocket transport.
- **Object:** an instance of a class. `new RocketTransport()` creates a rocket.
- **Method:** an action an object can perform. `flyTo("Moon")` simulates a flight to the Moon.
- **Field:** data stored inside an object. `transport` holds the selected transport reference.
- **Constructor:** code that runs when an object is created and initializes its fields.
- **Interface:** a contract declaring methods that implementing classes must provide.
  `SpaceTransport` declares `flyTo`.
- **Abstract class:** a base class that cannot be instantiated directly.
  You cannot write `new SpaceMission(...)`, but you can write `new CargoMission(...)`.
- **`extends`:** inheritance from a class. `CargoMission` inherits fields and
  `setTransport` from `SpaceMission`.
- **`implements`:** implementation of an interface. Both transports implement `SpaceTransport`.
- **`@Override`:** marks a method that implements or overrides a method from an interface or parent class.
- **`super(...)`:** calls the parent class constructor.
- **`this.transport`:** the field of the current object; `transport` on the right
  side of the assignment is the method parameter.
- **`protected`:** lets subclasses access a parent class field.
- **`final`:** prevents reassignment of `destination` after initialization.

## 3. Required Bridge roles

| Requirement | File | Responsibility |
| --- | --- | --- |
| Abstraction | `src/SpaceMission.java` | Abstract class holding `SpaceTransport transport` |
| Refined Abstraction 1 | `src/ExplorationMission.java` | Performs exploration |
| Refined Abstraction 2 | `src/CargoMission.java` | Delivers supplies |
| Implementor | `src/SpaceTransport.java` | Interface declaring the low-level `flyTo` operation |
| Concrete Implementor 1 | `src/RocketTransport.java` | Implements flight by rocket |
| Concrete Implementor 2 | `src/ShuttleTransport.java` | Implements flight by shuttle |
| Client | `src/Main.java` | Composes objects and switches transport at runtime |

Class relationships:

```text
SpaceMission --------------------> SpaceTransport
     ^                             (interface)
     |                                  ^
     +-- ExplorationMission             |
     +-- CargoMission                   +-- RocketTransport
                                        +-- ShuttleTransport
```

The arrow to the right means that a mission **holds a reference** to a transport.
The upward arrows represent class inheritance or interface implementation.

## 4. Understanding the main example

```java
SpaceTransport rocket = new RocketTransport();
SpaceTransport shuttle = new ShuttleTransport();

SpaceMission exploration = new ExplorationMission("Moon", rocket);
exploration.execute();

exploration.setTransport(shuttle);
exploration.execute();
```

1. Create two transport objects: a rocket and a shuttle.
2. Create an exploration mission with a destination and the rocket transport.
3. `execute()` calls `transport.flyTo(destination)` and prints the exploration task.
4. `setTransport(shuttle)` replaces the transport reference inside the same mission.
5. Call `execute()` again. Java now calls the shuttle's `flyTo` implementation.

The `exploration` object remains the same. No second `new ExplorationMission` is
needed. Only its `transport` field changes.

The variable has type `SpaceTransport`, but the actual object can be a rocket or
a shuttle. Java selects the method implementation based on the actual object.
This is **polymorphism**.

The mission only calls the common `flyTo` method. It does not need to check the
transport type or know how the transport works internally.

`execute()` is a high-level operation: fly and perform the mission task.
`flyTo()` is a lower-level operation: fly to the destination.

## 5. Run in Windows PowerShell

Install a JDK that provides the `javac` and `java` commands.
Open a terminal in the repository root directory, `AITU`, and run:

```powershell
cd third_assignment
javac -d out src\*.java
java -cp out Main
```

- `javac` compiles `.java` source files into `.class` files.
- `-d out` places the compiled files in the `out` directory.
- `java -cp out Main` runs the `main` method in the `Main` class.
- `out` is ignored by Git; the submission contains source files.

Expected output:

```text
=== Exploration with rocket ===
Rocket flies to Moon.
Exploration mission: study Moon.

=== Same exploration with shuttle ===
Shuttle flies to Moon.
Exploration mission: study Moon.

=== Cargo with shuttle ===
Shuttle flies to Mars.
Cargo mission: deliver supplies to Mars.

=== Same cargo with rocket ===
Rocket flies to Mars.
Cargo mission: deliver supplies to Mars.
```

## 6. Clean Code principles and justification

| Principle | Application and benefit |
| --- | --- |
| Single Responsibility (SRP) | Missions define their tasks, transports handle flight, and `Main` assembles the example. Each class has a focused responsibility. |
| Meaningful names | `SpaceMission`, `SpaceTransport`, `execute`, `flyTo`, and `setTransport` describe their purposes and distinguish the two Bridge sides. |
| Small classes and methods | Each transport has one short method. Each mission subclass has a constructor and a short `execute` method. The code is easy to read. |
| Open/Closed Principle (OCP) | A new transport, such as `ProbeTransport`, can be added without changing mission classes. A new mission type does not require changing transports. |
| Dependency Inversion (DIP) | `SpaceMission` depends on the `SpaceTransport` interface rather than `RocketTransport`. Missions can use any implementation of that interface. |
| Hiding implementation details | After selecting a transport, `Main` uses `execute` and `setTransport`. Flight details belong to transport classes, so the client does not manage their internal steps. |

`Main` knows the concrete classes because it must select and create objects.
Mission classes depend only on the interface, which makes transport replacement possible.

## 7. Defense preparation

A short explanation:

> My example uses the Bridge pattern for space missions. SpaceMission is the
> abstraction. ExplorationMission and CargoMission are refined abstractions.
> SpaceTransport is the implementor interface. RocketTransport and
> ShuttleTransport are concrete implementors. A mission holds a transport
> reference and delegates flying to it. Main changes the transport of the
> same mission object at runtime. Mission types and transports can be
> extended independently.

Possible questions:

- **Where is the bridge?** In the `protected SpaceTransport transport` field of `SpaceMission`.
- **What is composition here?** One object holds a reference to another:
  a mission holds a transport and calls its methods.
- **How do you add a transport?** Create a class implementing `SpaceTransport`,
  implement `flyTo`, and pass an instance to the mission constructor or `setTransport`.
- **How do you add a mission?** Extend `SpaceMission` and implement `execute`.
- **How do you demonstrate runtime switching?** Show `setTransport` between two
  `execute` calls. The mission object is not recreated.
- **Why use an abstract class?** It stores shared fields and the transport setter,
  while subclasses define their specific mission tasks.
- **Why is this Bridge?** Two groups evolve independently: mission types and
  transport implementations. One group uses the other through a reference.
  An interface alone does not prove that a design uses Bridge.
- **How is it different from Factory Method?** Factory Method handles object
  creation. Bridge separates two sides of behavior and connects them using composition.
- **How is it different from Strategy?** Their structures can look similar.
  Strategy focuses on interchangeable algorithms; this example focuses on
  independent mission and transport hierarchies. A setter alone does not define a pattern.

Suggested reading order: `SpaceTransport`, both transports, `SpaceMission`,
both mission subclasses, and finally `Main`.
