package org.opentcs.testvehicle;


import org.opentcs.drivers.vehicle.MovementCommand;

import java.io.*;
import java.net.Socket;


/**
 * @author Jin xin lei
 * @date 2021/6/18 下午2:09
 */
public class SocketClient {
    public static final String DEFAULT_HOST = "localhost";
    public static final int DEFAULT_PORT = 2048;
    private Socket socket;
    public String host;
    public int port;
    InputStream in;
    OutputStream out;

    public SocketClient(){
        this(SocketClient.DEFAULT_HOST, SocketClient.DEFAULT_PORT);
    }
    public SocketClient(String host){
        this(host, SocketClient.DEFAULT_PORT);
    }
    public SocketClient(int port){
        this(SocketClient.DEFAULT_HOST, port);
    }
    public SocketClient(String host, String port){
        this(host, Integer.parseInt(port));
    }

    public SocketClient(String host, int port){
        this.host = host;
        this.port = port;
    }

    public boolean connect(){
        try {
            this.socket = new Socket(host, port);
            System.out.println("客户端启动成功");
            this.in = socket.getInputStream();
            this.out = socket.getOutputStream();
            return true;
        } catch (IOException e) {
            System.out.println("Connect Error:" + e.getMessage());
        }
        return false;
    }

    public boolean close(){
        try {
            this.in.close();
            this.out.close();
            this.socket.close();
            return true;
        } catch (IOException e) {
            System.out.println("Close Connection Error:" + e.getMessage());
        }
        return false;
    }

    public void send(MovementCommand cmd){
        // TODO MovementCommand 转换为协议格式

    }

    public String send(String message){
        try {
            String msg = message + "|";
            this.out.write(msg.getBytes());
            byte[] bytes = new byte[1024];
            int len = this.in.read(bytes);
            String str = new String(bytes, 0, len-1);

            return str;
        }catch (IOException e){
            System.out.println("Error: " + e);
            return "";
        }
    }

    public static void main(String[] args){
        SocketClient s1 = new SocketClient("127.0.0.1", 2048);
        s1.connect();
        System.out.println("Connect to: " + s1);
        String msg1 = "Move,A";
        String msg2 = s1.send(msg1);
        System.out.println("send: " + msg1);
        System.out.println("receive: " + msg2);
        s1.close();
    }

}
