public class NavigationSystem {
    private String currentDestination;

    public int calculateRequiredFuel(String destination) {
        if ("Moon".equalsIgnoreCase(destination)) {
            return 500;
        }
        if ("Mars".equalsIgnoreCase(destination)) {
            return 1000;
        }
        return -1;
    }

    public void lockTrajectory(String destination) {
        this.currentDestination = destination;
        System.out.println("NavigationSystem: trajectory locked to " + currentDestination + ".");
    }

    public void resetTrajectory() {
        this.currentDestination = null;
        System.out.println("NavigationSystem: trajectory reset.");
    }
}
