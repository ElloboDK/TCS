package org.opentcs.testvehicle;

import org.opentcs.data.model.Vehicle;

/**
 * @author Jin xin lei
 */
public interface TestAdapterComponentsFactory {
    TestCommAdapter createCommAdapter(Vehicle vehicle);
}
