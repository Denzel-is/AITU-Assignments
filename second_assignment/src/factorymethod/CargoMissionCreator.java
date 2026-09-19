package src.factorymethod;

public class CargoMissionCreator extends  MissionCreator{

    @Override 
    public  SpaceMission createMission(){
        return new CargoMission();
    }

}
