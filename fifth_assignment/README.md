# Assignment #5 - Strategy Pattern

Topic: space mission fuel planning. A simple Java console example with no external libraries.

The mission already knows its required fuel. Different strategies calculate how
much fuel to load. These are illustrative planning rules, not real flight calculations.
The example assumes a positive, finite fuel requirement and a non-null strategy.

Before submission, check that this topic was not used in your lecture and is
unique in your group. The repository alone cannot confirm these requirements.

## Pattern roles

| Role | Class | Responsibility |
| --- | --- | --- |
| Strategy | `FuelStrategy` | Declares `calculateFuel(requiredFuel)` |
| Concrete Strategy 1 | `FixedReserveStrategy` | Adds a fixed 100-liter reserve |
| Concrete Strategy 2 | `PercentageReserveStrategy` | Adds a 20% reserve |
| Concrete Strategy 3 | `FullTankStrategy` | Rounds up to complete 200-liter tanks |
| Context | `SpaceMission` | Holds a strategy and delegates the calculation |
| Client | `Main` | Creates strategies and switches the same mission at runtime |

`SpaceMission` knows only the `FuelStrategy` interface. It has no `if` or `switch`
to select a strategy. `Main` chooses it through the constructor and `setStrategy`.
All three strategies solve the same problem, but use different calculations.

## How to run

Install a JDK that provides `javac` and `java`. From the repository root:

```sh
cd fifth_assignment
javac -d out src/*.java
java -cp out Main
```

In Windows PowerShell, use `src\*.java` in the `javac` command.
Compile each assignment separately because they reuse class names such as `Main`.

Expected output:

```text
=== Fixed reserve ===
Fuel: 550.0 liters.

=== Same mission with percentage reserve ===
Fuel: 540.0 liters.

=== Same mission with full tanks ===
Fuel: 600.0 liters.
```

The same `mission` object keeps its 450-liter requirement. Only its strategy changes.

## Clean Code principles

1. **Meaningful names:** `calculateFuel`, `requiredFuel`, and `FixedReserveStrategy`
   explain the purpose without extra comments.
2. **Single Responsibility:** Each strategy owns one calculation. `SpaceMission`
   delegates it, while `Main` selects strategies and prints the results.
3. **Small classes and methods:** Each strategy has one short method, so the
   calculation is easy to read and test.
4. **Open/Closed Principle:** Add a new `FuelStrategy` implementation without
   changing `SpaceMission` or the existing strategies.
5. **Dependency Inversion:** `SpaceMission` depends on an interface, not on any
   concrete fuel strategy, allowing algorithms to be replaced at runtime.
6. **Named constants:** Reserve sizes and tank capacity have descriptive names
   instead of unexplained numbers inside the calculations.

## Extending the example

For a new minimum-reserve rule, add a class implementing `FuelStrategy` and
return `requiredFuel + Math.max(100, requiredFuel * 0.1)` from `calculateFuel`.
Select it in `Main` using `mission.setStrategy(new MinimumReserveStrategy())`.
The context and existing strategies do not need to change.
