public class Main {
    public static void main(String[] args) {
        FuelStrategy fixedReserve = new FixedReserveStrategy();
        FuelStrategy percentageReserve = new PercentageReserveStrategy();
        FuelStrategy fullTank = new FullTankStrategy();

        SpaceMission mission = new SpaceMission(450, fixedReserve);
        System.out.println("=== Fixed reserve ===");
        System.out.println("Fuel: " + mission.calculateFuel() + " liters.");

        mission.setStrategy(percentageReserve);
        System.out.println("\n=== Same mission with percentage reserve ===");
        System.out.println("Fuel: " + mission.calculateFuel() + " liters.");

        mission.setStrategy(fullTank);
        System.out.println("\n=== Same mission with full tanks ===");
        System.out.println("Fuel: " + mission.calculateFuel() + " liters.");
    }
}
