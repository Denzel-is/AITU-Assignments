public class SpaceMissionFacade {
    private final FuelSystem fuelSystem;
    private final NavigationSystem navigationSystem;
    private final LifeSupportSystem lifeSupportSystem;
    private final EngineSystem engineSystem;

    public SpaceMissionFacade() {
        this.fuelSystem = new FuelSystem();
        this.navigationSystem = new NavigationSystem();
        this.lifeSupportSystem = new LifeSupportSystem();
        this.engineSystem = new EngineSystem();
    }

    public void launchMission(String destination, int fuelLiters) {
        System.out.println("--- Starting mission to " + destination + " ---");

        int requiredFuel = navigationSystem.calculateRequiredFuel(destination);
        if (requiredFuel < 0) {
            System.out.println("Mission aborted: unknown destination " + destination + ".");
            return;
        }

        fuelSystem.loadFuel(fuelLiters);
        if (!fuelSystem.hasEnoughFuel(requiredFuel)) {
            System.out.println("Mission aborted: need " + requiredFuel + " liters, but only have " + fuelSystem.getCurrentFuel() + " liters.");
            abortMission();
            return;
        }

        navigationSystem.lockTrajectory(destination);
        lifeSupportSystem.pressurizeCabin();
        lifeSupportSystem.activateOxygenSupply();
        engineSystem.warmUp();

        if (engineSystem.ignite()) {
            fuelSystem.consumeFuel(requiredFuel);
            System.out.println("Mission status: spacecraft reached " + destination + " successfully!");
        }
    }

    public void abortMission() {
        System.out.println("--- Executing safe abort sequence ---");
        engineSystem.shutDown();
        lifeSupportSystem.switchToStandby();
        navigationSystem.resetTrajectory();
        fuelSystem.drainFuel();
    }
}
