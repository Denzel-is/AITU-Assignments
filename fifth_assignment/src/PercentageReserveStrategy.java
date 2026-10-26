public class PercentageReserveStrategy implements FuelStrategy {
    private static final double RESERVE_RATE = 0.2;

    @Override
    public double calculateFuel(double requiredFuel) {
        return requiredFuel + requiredFuel * RESERVE_RATE;
    }
}
