package src.abstractfactory;

public class MissionControl {

    private final Spacecraft spacecraft;
    private final Rover rover;

    public MissionControl(SpaceEquipmentFactory factory) {

        this.spacecraft = factory.spacecraft();
        this.rover = factory.rover();
    }

    public void startMission(){
        System.out.println("Starting the Mission...");
        spacecraft.lounch();
        rover.exploreSurface();
    }
}