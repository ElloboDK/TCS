package org.opentcs.testvehicle;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * @author banana
 * @date 2021/6/23 下午1:57
 */
public class socket_server {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(2048);
            System.out.println("服务端启动成功");

            Socket socket = serverSocket.accept();
            OutputStream outputStream = socket.getOutputStream();
            InputStream inputStream = socket.getInputStream();
            byte[] bytes = new byte[1024];
            while (true){
                int len = inputStream.read(bytes);
                String str = new String(bytes,0,len);
                System.out.println(str);
                str = str.substring(0, str.length()-1);
                String[] str1 = str.split(",");
                String str2 = "ENTER," + str1[1] + "|";

                Thread.sleep(1000);
                outputStream.write(str2.getBytes());
            }
        } catch (IOException | InterruptedException e){
            System.out.println("Error: " + e.getMessage());
        }

    }
}
