package src.factorymethod;

public abstract class MissionCreator {

    public abstract SpaceMission createMission();

    public void lounchMission() {
        System.out.println("Preparing the Mission");

        SpaceMission mission = createMission();
        mission.start();
    }
}