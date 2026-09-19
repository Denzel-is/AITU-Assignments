package src.abstractfactory;

public class MoonEquipmentFactory implements SpaceEquipmentFactory {

    @Override 
    public Spacecraft spacecraft(){
        return  new MoonSpacecraft();
    }
    @Override 
    public  Rover rover(){
        return  new MoonRover();
    }
}
