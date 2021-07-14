package org.opentcs.testvehicle;

import com.google.inject.assistedinject.Assisted;

import java.util.Arrays;
import java.util.List;
import static java.util.Objects.requireNonNull;
import javax.inject.Inject;
import org.opentcs.data.model.Vehicle;
import org.opentcs.data.order.Route.Step;
import org.opentcs.drivers.vehicle.BasicVehicleCommAdapter;
import org.opentcs.drivers.vehicle.LoadHandlingDevice;
import org.opentcs.drivers.vehicle.MovementCommand;
import org.opentcs.util.CyclicTask;
import org.opentcs.util.ExplainedBoolean;

/**
 * @author Jin xin lei
 */
public class TestCommAdapter extends BasicVehicleCommAdapter {

    private TestAdapterComponentsFactory componentsFactory;
    private Vehicle vehicle;
    private boolean initialized;
    private CyclicTask testTask;
    private final SocketClient socketClient;
    private String startPos;

    @Inject
    public TestCommAdapter(TestAdapterComponentsFactory componentsFactory, @Assisted Vehicle vehicle) {
        super(new TestVehicleModel(vehicle), 2, 1, "CHARGE");
        this.componentsFactory = componentsFactory;
        this.vehicle = vehicle;
        String ip = vehicle.getProperty("TestIP");
        String port = vehicle.getProperty("Port");
        this.startPos = vehicle.getProperty("StartPos");
        this.socketClient = new SocketClient(ip, port);
    }

    @Override
    public void initialize() {
        initialized = true;
        // 获取状态 位置
        if (getProcessModel().getVehicleState() != Vehicle.State.IDLE){
            getProcessModel().setVehiclePosition(startPos);
            getProcessModel().setVehicleState(Vehicle.State.IDLE);
        }
    }

    @Override
    public synchronized void enable() {
        if (isEnabled()) {
            return;
        }
        //开启线程(略)
        testTask = new TestTask();
        Thread simThread = new Thread(testTask, getName() + "-Task");
        simThread.start();
        super.enable();
    }

    @Override
    public synchronized void disable() {
        if (!isEnabled()) {
            return;
        }
        //线程停止
        testTask.terminate();
        testTask = null;
        super.disable();
    }

    @Override
    public void sendCommand(MovementCommand cmd)
            throws IllegalArgumentException {
        requireNonNull(cmd, "cmd");
    }

    @Override
    public ExplainedBoolean canProcess(List<String> operations) {
        requireNonNull(operations, "operations");

        final boolean canProcess = isEnabled();
        final String reason = canProcess ? "" : "adapter not enabled";
        return new ExplainedBoolean(canProcess, reason);
    }

    @Override
    public void processMessage(Object message) {
    }

    @Override
    protected void connectVehicle() {
    }

    @Override
    protected void disconnectVehicle() {
    }

    @Override
    protected boolean isVehicleConnected() {
        return true;
    }

    /**
     * 内部类，用于处理运行步骤
     */
    private class TestTask
            extends CyclicTask {

        private TestTask() {
            super(0);
        }

        //线程执行
        @Override
        protected void runActualTask() {
            try {

                final MovementCommand curCommand;
                synchronized (TestCommAdapter.this) {
                    curCommand = getSentQueue().peek();
                }
                if(curCommand == null){
                    Thread.sleep(1000);
                    return;
                }

                final Step curStep = curCommand.getStep();
                sendMovement(curStep);

                //运行Step，略
                if (!curCommand.isWithoutOperation()) {
                    String operation = curCommand.getOperation();
                    sendOperation(operation);
                    //运行操作（上料或者下料，略）
                }
                if (getSentQueue().size() <= 1 && getCommandQueue().isEmpty()) {
                    getProcessModel().setVehicleState(Vehicle.State.IDLE);
                }
                //更新UI
                synchronized (TestCommAdapter.this) {
                    MovementCommand sentCmd = getSentQueue().poll();
                    if (sentCmd != null && sentCmd.equals(curCommand)) {
                        getProcessModel().commandExecuted(curCommand);
                        TestCommAdapter.this.notify();
                    }
                }
            }
            catch (Exception ex) {

            }
        }

        private void sendMovement(Step step) throws Exception{
            if(step.getPath() == null){
                return;
            }
            socketClient.connect();
            String destinationPoint = step.getDestinationPoint().getName();
            getProcessModel().setVehicleState(Vehicle.State.EXECUTING);
            System.out.println("send to" + socketClient.host + ": "+ socketClient.port + ": MOVE," + destinationPoint);
            String str = socketClient.send("MOVE," + destinationPoint);
            String currentPoint = str.split(",")[1];
            getProcessModel().setVehiclePosition(currentPoint);
            getProcessModel().setVehicleState(Vehicle.State.IDLE);
            socketClient.close();
        }

        private void sendOperation(String operation){
            if (operation == ""){
                return;
            }
            socketClient.connect();
            getProcessModel().setVehicleState(Vehicle.State.EXECUTING);
            System.out.println("send to" + socketClient.host + ": "+ socketClient.port + " Operation: " + operation);
            socketClient.send(operation);
            if (operation.equals("LOAD")) {
                getProcessModel().setVehicleLoadHandlingDevices(
                        Arrays.asList(new LoadHandlingDevice("default", true)));
            }
            else if (operation.equals("UNLOAD")) {
                getProcessModel().setVehicleLoadHandlingDevices(
                        Arrays.asList(new LoadHandlingDevice("default", false)));
            }
            getProcessModel().setVehicleState(Vehicle.State.IDLE);
            socketClient.close();

        }
    }
}

