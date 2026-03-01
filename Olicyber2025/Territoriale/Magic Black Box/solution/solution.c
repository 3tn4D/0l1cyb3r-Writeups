#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

unsigned char hex_final[] = { 0x31, 0x66, 0x38, 0x34, 0x65, 0x36, 0x32, 0x39, 0x30, 0x62, 0x32, 0x39, 0x61, 0x35, 0x30, 0x39, 0x35, 0x34, 0x36, 0x30, 0x37, 0x66, 0x62, 0x32, 0x61, 0x64, 0x36, 0x36, 0x31, 0x35, 0x37, 0x39, 0x36, 0x61, 0x35, 0x32, 0x32, 0x64, 0x36, 0x38, 0x38, 0x64, 0x38, 0x39, 0x61, 0x63, 0x66, 0x66, 0x65, 0x39, 0x35, 0x61, 0x37, 0x37, 0x31, 0x63, 0x65, 0x39, 0x62, 0x61, 0x30, 0x64, 0x31, 0x32, 0x62, 0x30, 0x32, 0x38, 0x38, 0x64, 0x37, 0x63, 0x00 };
unsigned char raw_final[36] = {0};
unsigned char raw_start[36] = {0};
unsigned char hex_start[72] = {0};
int random_arr[500];

void hex_to_bytes(unsigned char *output, unsigned char *input,int len){
    unsigned char curr_hex;
    
    for(int i = 0; i < len; i += 2){
        sscanf((char *)&input[i], "%2hhx", &curr_hex);

        output[i >> 1] = curr_hex;
    }

    return;
}

void bytes_to_hex(unsigned char *output, unsigned char *input, int len){
    for(int i = 0; i < len; i++){
        sprintf((char *)&output[i * 2], "%02x", (unsigned int)input[i]);
    }
    output[len*2] = 0;

    return;
}

void xor(int random_n){
    for(int i = 0; i < 36; i++){
        raw_start[i] = (unsigned char)random_n ^ raw_final[i];
    }
}

void add(int random_n){
    for (int i = 0; i < 36; i = i + 1) {
        raw_start[i] = raw_final[i] + (char)random_n;
    }
}

void sub(int random_n){
    for (int i = 0; i < 36; i = i + 1) {
        raw_start[i] = raw_final[i] - (char)random_n;
    }
}

void rotate_left(int random_n){
    for (int i = 0; i < 36; i = i + 1) {
        raw_start[i] = raw_final[(i + random_n + (int)(random_n / 36) * -36) % 36];
    }
    return;
}

void rotate_right(int random_n){
  for (int i = 0; i < 36; i = i + 1) {
    raw_start[i] = raw_final[((i - (unsigned int)(random_n + (int)(random_n / 36) * -36)) + 36) % 36];
  }
  return;
}

void magic_black_box(){
    void (*operations[5])(int) = { xor, sub, add, rotate_right, rotate_left };
    
    srand(4919);

    for(int i = 0; i < 500; i++){
        random_arr[i] = rand();
    }
    
    for(int i = 499; i >= 0; i--){
        operations[i % 5](random_arr[i]);
        for(int j = 0; j < 36; j++){
            raw_final[j] = raw_start[j];
        }
    }
}

int main(){
    hex_to_bytes(raw_final, hex_final, 72);
    magic_black_box();
    bytes_to_hex(hex_start, raw_start, 36);

    printf("%s", hex_start);
    printf("\n");
}