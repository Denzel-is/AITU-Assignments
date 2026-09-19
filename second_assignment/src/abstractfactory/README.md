# Space Mission

This is a Java project for the Software Design Patterns course.

The project shows two creational design patterns:

* Factory Method
* Abstract Factory

## Factory Method

Factory Method is used to create different types of space missions.

The project has:

* `SpaceMission` — common interface
* `ExplorationMission`
* `CargoMission`
* `MissionCreator`
* `ExplorationMissionCreator`
* `CargoMissionCreator`

For example:

```java id="u8llxo"
public SpaceMission createMission() {
    return new ExplorationMission();
}
```

This allows the program to create different missions through a common `SpaceMission` type.

## Abstract Factory

Abstract Factory is used to create related space equipment.

There are two types of products:

* `Spacecraft`
* `Rover`

And two families:

### Mars

* `MarsSpacecraft`
* `MarsRover`

### Moon

* `MoonSpacecraft`
* `MoonRover`

Each factory creates equipment for one destination.

For example:

```java id="9ec0nj"
public Spacecraft createSpacecraft() {
    return new MarsSpacecraft();
}
```

`MissionControl` uses the factory and does not create Mars or Moon objects directly.

## Clean Code

Some Clean Code ideas used in the project:

* clear class and method names
* small methods
* separate classes for different responsibilities
* using interfaces instead of concrete classes
* object creation is kept inside factory classes

Example:

```java id="1pxict"
private final Spacecraft spacecraft;
```

instead of using a concrete class like:

```java id="ifdzmc"
private MarsSpacecraft spacecraft;
```

## Project Structure

```text id="77cv7x"
src
|
|-- Main.java
|
|-- factorymethod
|   |-- SpaceMission.java
|   |-- ExplorationMission.java
|   |-- CargoMission.java
|   |-- MissionCreator.java
|   |-- ExplorationMissionCreator.java
|   `-- CargoMissionCreator.java
|
`-- abstractfactory
    |-- Spacecraft.java
    |-- Rover.java
    |-- MarsSpacecraft.java
    |-- MarsRover.java
    |-- MoonSpacecraft.java
    |-- MoonRover.java
    |-- SpaceEquipmentFactory.java
    |-- MarsEquipmentFactory.java
    |-- MoonEquipmentFactory.java
    `-- MissionControl.java
```

Run the `Main` class to test the project.
