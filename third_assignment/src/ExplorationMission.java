public class ExplorationMission extends SpaceMission {
    public ExplorationMission(String destination, SpaceTransport transport) {
        super(destination, transport);
    }

    @Override
    public void execute() {
        transport.flyTo(destination);
        System.out.println("Exploration mission: study " + destination + ".");
    }
}
