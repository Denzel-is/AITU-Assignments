public class SpaceMission {
    private final double requiredFuel;
    private FuelStrategy strategy;

    public SpaceMission(double requiredFuel, FuelStrategy strategy) {
        this.requiredFuel = requiredFuel;
        this.strategy = strategy;
    }

    public void setStrategy(FuelStrategy strategy) {
        this.strategy = strategy;
    }

    public double calculateFuel() {
        return strategy.calculateFuel(requiredFuel);
    }
}
