public class Main {
    public static void main(String[] args) {
        SpaceMissionFacade missionControl = new SpaceMissionFacade();

        System.out.println("=== Test 1: Successful launch to Moon ===");
        missionControl.launchMission("Moon", 600);

        System.out.println("\n=== Test 2: Failed launch to Mars (not enough fuel) ===");
        missionControl.launchMission("Mars", 300);
    }
}
