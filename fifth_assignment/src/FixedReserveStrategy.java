public class FixedReserveStrategy implements FuelStrategy {
    private static final double RESERVE_LITERS = 100;

    @Override
    public double calculateFuel(double requiredFuel) {
        return requiredFuel + RESERVE_LITERS;
    }
}
