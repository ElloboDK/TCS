package org.opentcs.testvehicle;

import org.opentcs.data.model.Vehicle;
import org.opentcs.drivers.vehicle.VehicleProcessModel;

/**
 * @author Jin xin lei
 */
public class TestVehicleModel extends VehicleProcessModel {

    public TestVehicleModel(Vehicle attachedVehicle){
        super(attachedVehicle);
    }
}
