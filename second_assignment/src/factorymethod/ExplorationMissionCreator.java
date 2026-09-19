package src.factorymethod;

public class ExplorationMissionCreator extends MissionCreator {

    @Override 
    public SpaceMission createMission(){
        return new ExplorationMission();
    }
}
