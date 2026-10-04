public class RocketTransport implements SpaceTransport {
    @Override
    public void flyTo(String destination) {
        System.out.println("Rocket flies to " + destination + ".");
    }
}
