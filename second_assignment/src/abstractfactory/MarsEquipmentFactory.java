package src.abstractfactory;

public class MarsEquipmentFactory implements SpaceEquipmentFactory{

    @Override
    public Spacecraft spacecraft() {
        return  new MarsSpacecraft();
    }

    @Override
    public Rover rover() {
        return  new MarsRover();
    }
}
