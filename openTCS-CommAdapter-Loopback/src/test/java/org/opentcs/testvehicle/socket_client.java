package org.opentcs.testvehicle;

import java.io.*;
import java.net.Socket;

/**
 * @author jxl
 * @date 2021/6/22 下午1:59
 */
public class socket_client {

    public static void main(String[] args) {
        try{
            Socket socket = new Socket("127.0.0.1", 2048);
            System.out.println("客户端启动成功");
            OutputStream outputStream = socket.getOutputStream();
            InputStream inputStream = socket.getInputStream();
            byte[] bytes = new byte[1024];
            while (true){
                outputStream.write("MOVE,A|".getBytes());
                int len = inputStream.read(bytes);
                String str = new String(bytes,0,len);
                System.out.println(str);
            }


        }catch (Exception e){
            System.err.println("Error:" + e.getMessage());
        }
    }
}
