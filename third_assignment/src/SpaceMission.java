public abstract class SpaceMission {
    protected final String destination;
    protected SpaceTransport transport;

    public SpaceMission(String destination, SpaceTransport transport) {
        this.destination = destination;
        this.transport = transport;
    }

    public void setTransport(SpaceTransport transport) {
        this.transport = transport;
    }

    public abstract void execute();
}
