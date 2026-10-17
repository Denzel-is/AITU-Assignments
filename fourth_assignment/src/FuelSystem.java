public class FuelSystem {
    private int currentFuel;

    public void loadFuel(int liters) {
        if (liters > 0) {
            currentFuel += liters;
        }
        System.out.println("FuelSystem: added " + liters + " liters. Total fuel: " + currentFuel + " liters.");
    }

    public int getCurrentFuel() {
        return currentFuel;
    }

    public boolean hasEnoughFuel(int requiredLiters) {
        return currentFuel >= requiredLiters;
    }

    public void consumeFuel(int liters) {
        currentFuel -= liters;
        System.out.println("FuelSystem: consumed " + liters + " liters. Remaining: " + currentFuel + " liters.");
    }

    public void drainFuel() {
        currentFuel = 0;
        System.out.println("FuelSystem: tank drained safely.");
    }
}
