#include "Particle.h"

SYSTEM_THREAD(ENABLED);

const pin_t MY_LED = D7;

std::string test_name = "Jack";

void morse_dot() {
    digitalWrite(MY_LED, HIGH);
    delay(500);
    digitalWrite(MY_LED, LOW);
}

void morse_line(){
    digitalWrite(MY_LED, HIGH);
    delay(1000);
    digitalWrite(MY_LED, LOW);
}


// Long blink for line, short blink for dot
void morse_code(char c){
    c = tolower(c);
    switch (c){
        case 'a':
            morse_dot();
            morse_line();
            break;
        case 'b':
            morse_line();
            morse_dot();
            morse_dot();
            morse_dot();
            break;
        case 'c':
            morse_line();
            morse_dot();
            morse_line();
            morse_dot();
            break;
        case 'd':
            morse_line();
            morse_dot();
            morse_dot();
            break;
        case 'e':
            morse_dot();
            break;
        case 'f':
            morse_dot();
            morse_dot();
            morse_line();
            morse_dot();
            break;
        case 'g':
            morse_line();
            morse_line();
            morse_dot();
            break;
        case 'h':
            morse_dot();
            morse_dot();
            morse_dot();
            morse_dot();
            break;
        case 'i':
            morse_dot();
            morse_dot();
            break;
        case 'j':
            morse_dot();
            morse_line();
            morse_line();
            morse_line();
            break;
        case 'k':
            morse_line();
            morse_dot();
            morse_line();
            break;
        case 'l':
            morse_dot();
            morse_line();
            morse_dot();
            morse_dot();
            morse_dot();
            break;
        case 'm':
            morse_line();
            morse_line();
            break;
        case 'n':
            morse_line();
            morse_dot();
            break;
        case 'o':
            morse_line();
            morse_line();
            morse_line();
            break;
        case 'p':
            morse_dot();
            morse_line();
            morse_line();
            morse_dot();
            break;
        case 'q':
            morse_line();
            morse_line();
            morse_dot();
            morse_line();
            break;
        case 'r':
            morse_dot();
            morse_line();
            morse_dot();
            break;
        case 's':
            morse_dot();
            morse_dot();
            morse_dot();
            break;
        case 't':
            morse_line();
            break;
        case 'u':
            morse_dot();
            morse_dot();
            morse_line();
            break;
        case 'v':
            morse_dot();
            morse_dot();
            morse_dot();
            morse_line();
            break;
        case 'w':
            morse_dot();
            morse_line();
            morse_line();
            break;
        case 'x':
            morse_line();
            morse_dot();
            morse_dot();
            morse_line();
            break;
        case 'y':
            morse_line();
            morse_dot();
            morse_line();
            morse_line();
            break;
        case 'z':
            morse_line();
            morse_line();
            morse_dot();
            morse_dot();
            break;
        default:
            // Flash to indicate error
            digitalWrite(MY_LED, HIGH);
            delay(250);
            digitalWrite(MY_LED, LOW);
            delay(250);
            digitalWrite(MY_LED, HIGH);
            break;
        
    }
    digitalWrite(MY_LED, LOW);
    delay(250); // Wait 2 second before next letter
}

int encode_morse(String s){
    for (int i = 0; i < s.length(); i++ ){
        morse_code(s[i]);
    }
    
    digitalWrite(MY_LED, LOW);
    delay(5000);
    return 1;
}

void setup() {
    pinMode(MY_LED, OUTPUT);
    digitalWrite(MY_LED, LOW);
	Particle.function("Morse Code Word", encode_morse);

}

void loop() {
    // Testing
    /*
    for (int i = 0; i < test_name.length(); i++ ){
        morse_code(test_name[i]);
    }
    
    digitalWrite(MY_LED, LOW);
    delay(5000);
    */
}

























