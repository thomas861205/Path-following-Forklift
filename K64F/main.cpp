#include "mbed.h"
#include "parallax.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
#include "uLCD_4DGL.h"

DigitalOut led1(LED1);
PwmOut pin12(D12), pin11(D11), buzzer(D3);
PwmOut pin13(D13);
Serial pc(USBTX, USBRX);

uLCD_4DGL uLCD(D1, D0, D2);

parallax_servo *servo0_ptr, *servo1_ptr, *servo2_ptr;



int main() {

    int displat_cnt = 0;

    bbcar_init(pin11, pin12, pin13);
    char buf[256], outbuf[256];

    uLCD.printf("\nHello uLCD World\n");

    while (1) {
        for ( int i = 0; ; i++ ) {
            buf[i] = pc.getc();

            if (buf[i] == '\n') break;
        }

        if (buf[0] == '/'){
            RPC::call(buf, outbuf);
            pc.printf("%s\r\n", outbuf);
        }
        else{
            int total_char = 0;
            int i = 0;

            // uLCD.locate(0, 0);
            // uLCD.printf("                 \n");

            // if (buf[0] == ' ' || buf[0] == '1'){
            //     total_char += 18;

            //     while(buf[i] != '\n'){
            //         uLCD.locate(total_char % 18, total_char / 18);

            //         uLCD.printf("%c",buf[i]);
            //         total_char++;
            //         i++;
            //     }

            // }
            uLCD.cls();

            
            while(buf[i] != '\n'){
                

                uLCD.locate(total_char % 18 + 1, total_char / 18);

                uLCD.printf("%c",buf[i]);
                total_char++;
                i++;
            }
        }
    }
}