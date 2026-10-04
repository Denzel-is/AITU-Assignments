public class CargoMission extends SpaceMission {
    public CargoMission(String destination, SpaceTransport transport) {
        super(destination, transport);
    }

    @Override
    public void execute() {
        transport.flyTo(destination);
        System.out.println("Cargo mission: deliver supplies to " + destination + ".");
    }
}
