#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

unsigned char arr_enc_flag[48] = { 0xe7, 0x8e, 0x9a, 0x5c, 0xba, 0xe0, 0xb5, 0x4e, 0x73, 0x5d, 0xca, 0xdf, 0xdd, 0x75, 0x3d, 0xb6, 0xfe, 0x07, 0x9f, 0x92, 0x6f, 0xf4, 0x6b, 0xb0, 0x89, 0x0f, 0x28, 0x0d, 0x65, 0x64, 0x98, 0x33, 0xe3, 0xf9, 0x84, 0xc3, 0xb3, 0x8f, 0x50, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
char *enc_flag = (char *)arr_enc_flag;

char xor_key[48] = { 0xbe, 0xc0, 0xc9, 0x76, 0xf5, 0xab, 0xf6, 0x09, 0x56, 0x19, 0x85, 0xfd, 0xe1, 0x4d, 0x0e, 0x83, 0xe3, 0x46, 0xa8, 0xa6, 0x5b, 0xcb, 0x7c, 0x8b, 0xbe, 0x33, 0x1c, 0x24, 0x74, 0x51, 0xb3, 0x1b, 0xcb, 0xca, 0x8f, 0xec, 0x98, 0xbf, 0x78, 0x5b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

long check_len(char *data) {
    char *i = data;
    while (*i != '\0') {
        i = i + 1;
    }
    return (long)i - (long)data;
}

void to_lower(char *buf, unsigned short len) {
    for (int i = 0; i < len; i++) {
        if (buf[i] > '@' && buf[i] < '[') {
            buf[i] = buf[i] + 32;
        }
    }
    return;
}

void swap_pairs(char *data){
    int i = 0;
    while(i < check_len(data)){
        data[i] = data[i] + data[(long)i + 1];
        data[(long)i + 1] = data[(long)i + 1] + data[i];
        data[i] = data[(long)i + 1] - data[i];
        data[(long)i + 1] = (data[(long)i + 1] - data[i]) - data[i];
        i = i + 2;
    }

    return;
}

void replace_char(char *buf, int *data){
    for(int i = 0; buf[i] != '\0'; i++){
        if((buf[i]- data[0] & 0xffU) == 0){
            buf[i] = ((char)data[1] - (char)data[0]) + buf[i];
        }
    }

    return;
}

void xor(char *buf,long n){
  unsigned long curr_len;
  int i;
  
  i = 0;
  while( true ) {
    curr_len = check_len(buf);
    if (curr_len <= (unsigned long)(long)i) break;
    buf[i] = buf[i] & ~*(char *)(i + n) | ~buf[i] & *(char *)(i + n);
    i = i + 1;
  }
  return;
}

void decrypt(char *buf, char key){
    for(int i = 0; buf[i] != '\0'; i++){
        buf[i] -= (char)0x1438;
        buf[i] -= key;
        buf[i] += (char)(i + 0x1438);
    }
    return;
}

void rotate_right(char *str, int data) {
    long len = check_len(str);
    int shift = (int)((unsigned long)(long)data % len);
    char *buf = calloc(1, len + 1);
    
    int i = 0;
    for (int r = len - shift; r < len; r++) {
        buf[i++] = str[r];
    }
    for (int r = 0; r < len - shift; r++) {
        buf[i++] = str[r];
    }
    
    buf[len] = '\0';
    strcpy(str, buf);
    free(buf);
    return;
}

int main(){
    int substitution_table[8];
    substitution_table[7] = 122;
    substitution_table[6] = 64;

    swap_pairs(xor_key);
    
    swap_pairs(enc_flag);
    replace_char(enc_flag, (substitution_table + 6));
    xor(enc_flag, (long)xor_key);
    swap_pairs(enc_flag);
    decrypt(enc_flag, (char)0x84ba7800);
    to_lower(enc_flag, 0x0a);
    to_lower((enc_flag + 0x0a), check_len(enc_flag+0x0a));
    // rotate_right(enc_flag, 0x10);

    for(int i = 0; enc_flag[i] != '\0'; i++){
        if(enc_flag[i] == 's'){
            enc_flag[i] = '$';
        }
    }

    substitution_table[1] = 48;
    substitution_table[0] = 111;
    substitution_table[3] = 51;
    substitution_table[2] = 101;
    substitution_table[5] = 52;
    substitution_table[4] = 97;
    replace_char(enc_flag, (substitution_table + 4));
    replace_char(enc_flag, (substitution_table + 2));
    replace_char(enc_flag, substitution_table);
    substitution_table[1] = 95;
    substitution_table[0] = 45;
    substitution_table[3] = 33;
    substitution_table[2] = 105;
    substitution_table[5] = 55;
    substitution_table[4] = 116;
    replace_char(enc_flag, (substitution_table + 4));
    replace_char(enc_flag, (substitution_table + 2));
    replace_char(enc_flag, substitution_table);
    // rotate_right(enc_flag, 0x10);

    for(int i = 0; i < 48; i++){
        printf("%c", enc_flag[i]);
    }
    printf("\n");

    // y0u_$p!n_my_h34d_r!gh7_r0und_r!gh7_r0und

    return 0;
}