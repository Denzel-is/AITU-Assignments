public class LifeSupportSystem {
    private boolean cabinPressurized;

    public void pressurizeCabin() {
        cabinPressurized = true;
        System.out.println("LifeSupportSystem: cabin pressurized.");
    }

    public void activateOxygenSupply() {
        if (cabinPressurized) {
            System.out.println("LifeSupportSystem: oxygen supply active.");
        }
    }

    public void switchToStandby() {
        cabinPressurized = false;
        System.out.println("LifeSupportSystem: switched to standby mode.");
    }
}
