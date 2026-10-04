public class ShuttleTransport implements SpaceTransport {
    @Override
    public void flyTo(String destination) {
        System.out.println("Shuttle flies to " + destination + ".");
    }
}
