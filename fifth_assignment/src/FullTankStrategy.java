public class FullTankStrategy implements FuelStrategy {
    private static final double TANK_CAPACITY_LITERS = 200;

    @Override
    public double calculateFuel(double requiredFuel) {
        return Math.ceil(requiredFuel / TANK_CAPACITY_LITERS) * TANK_CAPACITY_LITERS;
    }
}
