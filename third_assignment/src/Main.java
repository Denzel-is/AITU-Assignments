public class Main {
    public static void main(String[] args) {
        SpaceTransport rocket = new RocketTransport();
        SpaceTransport shuttle = new ShuttleTransport();

        SpaceMission exploration = new ExplorationMission("Moon", rocket);
        System.out.println("=== Exploration with rocket ===");
        exploration.execute();

        exploration.setTransport(shuttle);
        System.out.println("\n=== Same exploration with shuttle ===");
        exploration.execute();

        SpaceMission cargo = new CargoMission("Mars", shuttle);
        System.out.println("\n=== Cargo with shuttle ===");
        cargo.execute();

        cargo.setTransport(rocket);
        System.out.println("\n=== Same cargo with rocket ===");
        cargo.execute();
    }
}
