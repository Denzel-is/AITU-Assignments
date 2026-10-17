# Assignment #4 - Facade Pattern

Topic: Space Mission Launch Control.

This project demonstrates the **Facade** structural design pattern in Java.

## Project Structure

```text
src
|-- Main.java
|-- SpaceMissionFacade.java
|-- FuelSystem.java
|-- NavigationSystem.java
|-- LifeSupportSystem.java
`-- EngineSystem.java
```

## Components

* **Complex Subsystem (4 classes):**
  * `FuelSystem` — manages fuel loading, checks if fuel is sufficient, and drains or consumes fuel.
  * `NavigationSystem` — calculates required fuel for a destination and locks or resets trajectory.
  * `LifeSupportSystem` — pressurizes the cabin and controls oxygen supply.
  * `EngineSystem` — warms up, ignites, and shuts down main engines.
* **Facade:**
  * `SpaceMissionFacade` — provides simple methods (`launchMission`, `abortMission`) that coordinate all four subsystem classes in the proper order.
* **Client:**
  * `Main` — interacts only with `SpaceMissionFacade` and never calls or creates subsystem classes directly.

All subsystem classes are independent and have no references back to `SpaceMissionFacade`.

## Clean Code Principles

1. **Meaningful Names:** Class and method names like `SpaceMissionFacade`, `launchMission`, `calculateRequiredFuel`, and `pressurizeCabin` clearly describe what they do.
2. **Single Responsibility Principle (SRP):** Each subsystem class handles one area (fuel, navigation, life support, engines), while `SpaceMissionFacade` only coordinates them.
3. **No Leaking of Subsystem Details:** `Main` passes only simple parameters (`destination`, `fuelLiters`) to the Facade and does not depend on any subsystem classes.
4. **Small, Focused Classes and Methods:** Every class is short and each method performs a single clear step.
5. **Proper Error Handling:** Before igniting the engines, the Facade checks if the destination is valid and if there is enough fuel. When fuel is too low, it stops the launch and runs `abortMission()`.

## How to Run

```powershell
cd fourth_assignment
javac -d out src\*.java
java -cp out Main
```
