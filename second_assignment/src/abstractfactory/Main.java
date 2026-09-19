package src.abstractfactory;

import src.factorymethod.MissionCreator;
import src.factorymethod.CargoMissionCreator;
import src.factorymethod.ExplorationMissionCreator;

import src.abstractfactory.MarsEquipmentFactory;
import src.abstractfactory.MoonEquipmentFactory;
import src.abstractfactory.SpaceEquipmentFactory;
import src.abstractfactory.MissionControl;

public class Main {

    public static void main(String[] args) {
        System.out.println("...---...Factory Method...---...");
        
        MissionCreator creator = new ExplorationMissionCreator();
        creator.lounchMission();
        
        System.out.println();
        
        creator = new CargoMissionCreator();
        creator.lounchMission();

        System.out.println();
        System.out.println();
        
        System.out.println("...---...Abstract Factory...---...");
        SpaceEquipmentFactory factory = new MarsEquipmentFactory();
        MissionControl missionControl = new MissionControl(factory);

        missionControl.startMission();
        System.out.println();

        factory = new MoonEquipmentFactory();
        missionControl= new MissionControl(factory);
        missionControl.startMission();
        System.out.println();
    }
}