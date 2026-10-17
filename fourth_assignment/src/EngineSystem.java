public class EngineSystem {
    private boolean warmedUp;

    public void warmUp() {
        warmedUp = true;
        System.out.println("EngineSystem: main engines warmed up.");
    }

    public boolean ignite() {
        if (!warmedUp) {
            System.out.println("EngineSystem: cannot ignite cold engines.");
            return false;
        }
        System.out.println("EngineSystem: main engines ignited! Liftoff!");
        return true;
    }

    public void shutDown() {
        warmedUp = false;
        System.out.println("EngineSystem: engines shut down.");
    }
}
