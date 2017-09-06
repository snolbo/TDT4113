
const int buttonPin = 2;     // the number of the pushbutton pin
const int redLedPin =  3;
const int blueLedPin =  4;
const int greenLedPin =  5;

const int T = 300; // milliseconds for which a time period is defined

int sentCommand = -1;

int pressTime = 0; // holds the time in millis the button was pressed
// HIGH means that the button is not pressed. LOW is pressed
int buttonState = HIGH; // to get input of current button state
int lastButtonState = HIGH; // to hold value of previous button state
boolean stateChanged = false; // describes if the state of the buttons changed

void setup() {
  Serial.begin(9600);
  pinMode(redLedPin, OUTPUT);  
  pinMode(blueLedPin, OUTPUT);  
  pinMode(greenLedPin, OUTPUT);
  pinMode(buttonPin, INPUT); 

}

// 0000 0 0100 0100 111

void loop() {
  // Read the pin and change the state if valid
  buttonState = digitalRead(buttonPin);
  changeButtonStates(buttonState); 
  
  if(millis() - pressTime > T/2 && stateChanged){ // timer handles deboounce together with statechanged
    pressTime = millis() - pressTime;
    // return command to send corresponding to timeinterval since last state change
    sentCommand = sendCommand(pressTime);
    // Light LED based on sent command
    showLastCommandWithLed(sentCommand);
    // set NOW as time for last press
    pressTime = millis();
 }
  stateChanged = false;
 

}


// sends command depending on the time the button was in rest or paused
int sendCommand(int pressTime){
  int commandToSend = -1;
  if(buttonState == HIGH){
    if(pressTime <= 2*T && pressTime >= T/2 ){
      Serial.print(1);
      commandToSend = 1;
    }
    else if(pressTime <= 4*T && pressTime > 2*T){
      Serial.print(2);
      commandToSend = 2;
    }
    else{
      // do nothing
    }
  }
  else if(buttonState == LOW){
    if(pressTime <= 5*T && pressTime >= 2*T){
      // send 2
      Serial.print(3);
      commandToSend = 3;
    }
    else if(pressTime > 5*T ){
      // send 3
      Serial.print(4); 
      commandToSend = 4;  
    }
    else{
      // do nothing
    }
  }
  return commandToSend;
}


// changes buttonstates depending on given state, and the previous
void changeButtonStates(int buttonState){
  if(buttonState != lastButtonState ){
    lastButtonState = buttonState;
    stateChanged = true;
  }
}


// shows with the LED's the command corresponding to the input value
void showLastCommandWithLed(int lastCommand){
  turnOffAllLights();
  if(lastCommand == 1){
    digitalWrite(redLedPin, HIGH);
  }
  else if(lastCommand == 2){
    digitalWrite(blueLedPin, HIGH);
  }
  else if(lastCommand == 3){
    digitalWrite(greenLedPin, HIGH);
  }
  else if(lastCommand == 4){
    digitalWrite(redLedPin, HIGH);
    digitalWrite(blueLedPin, HIGH);
    digitalWrite(greenLedPin, HIGH); 
  }
}

// turns off all LED lgihts
void turnOffAllLights(){
  digitalWrite(redLedPin, LOW);
  digitalWrite(blueLedPin, LOW);
  digitalWrite(greenLedPin, LOW);
}



