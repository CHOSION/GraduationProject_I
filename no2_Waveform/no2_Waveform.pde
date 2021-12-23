import ddf.minim.*;
Minim minim;
AudioInput in;
AudioRecorder recorder;
PImage button;
PGraphics alphaG;
PFont font;

float timeRate = 1.0/30.0;
int j;
float time;
int count = 1;
boolean running = false;

//버튼 관련 변수들
int circleX, circleY;
int circleSize = 100;
color circleColor, circleHighlight;
boolean circleOver = false;

int buttonX, buttonY;
int buttonSize = 50;
boolean buttonOver = false;

//질문거리
String sen1="살면서 가장 재미있었던 나이와 그 이유는?";
String sen2="코로나가 끝나면 제일 먼저 하고 싶은 것은?";
String sen3="현재 가장 고민인 것은?";
String sen4="당신이 원하는 삶의 모습은?";
String sen5="어린 시절의 꿈은?";
String sen6="1년 전의 나에게 하고 싶은 말?";
String sen7="생애 최초의 기억은?";
String sen8="1년 후의 내 모습은?";
String sen9="행복이란?";
String sen10="나의 매력 포인트는 무엇인가요?";
String sen11="애창곡 한 소절 불러주세요^-^";
String sen12="요즘 최대의 관심사는?";

int randomNum;
int textX, textY;

void setup(){
  fullScreen();
  //size(1000, 500);           //이거 둘 중에 하나 쓰면 됩니다
  
  minim = new Minim(this);
  in = minim.getLineIn();
  recorder = minim.createRecorder(in, "../no3_Ticket/voice/" + str(count) + "_voice.wav");
  
  randomNum = int(random(1, 13));
  
  font = createFont("조선일보명조.ttf", 48);
  button = loadImage("reset.png");

  circleColor = color(230, 20, 15);
  circleHighlight = color(162, 48, 46);
  circleX = width/2;
  circleY = 950;  
  ellipseMode(CENTER);
  
  buttonX = 150;
  buttonY = 240;
  
  textX = width/2;
  textY = 300;
  
  reset_sketch();     //setup은 프로세싱 실행할 때 딱 한 번만 돌아가므로 녹음 버튼 누를때마다 reset_sketch로 setup의 기능을 수행함
}


void reset_sketch(){
  frameRate(30);

  recorder = minim.createRecorder(in, "../no3_Ticket/voice/" + str(count) + "_voice.wav");
  alphaG = createGraphics(1080, 300, JAVA2D);           //음파 저장할 파일의 가로세로 사이즈

  time = 6.0;
  j = 0;

}


void draw(){
  update(mouseX, mouseY);
  background(255, 255, 255);          
  
  //버튼 관련
  if (circleOver) {           //원 위에 마우스 커서가 있는지?
    circleSize = 110;
    fill(circleHighlight);
  } else {
    circleSize = 100;
    fill(circleColor);
  }
  stroke(200);
  strokeWeight(12);
  ellipse(circleX, circleY, circleSize, circleSize);
    
  if(buttonOver){               //새로고침 버튼 위에 마우스 커서가 있는지?
    image(button, buttonX-10, buttonY-10, buttonSize+20, buttonSize+20);
  }
  else {
    image(button, buttonX, buttonY, buttonSize, buttonSize);
  }
  
  //질문
  textFont(font,80);
  textAlign(CENTER);
  noStroke();
  fill(70);
  switch(randomNum){
    case 1:
      text(sen1, textX, textY);
      break;
    case 2:
      text(sen2, textX, textY);
      break;
    case 3:
      text(sen3, textX, textY);
      break;
    case 4:
      text(sen4, textX, textY);
      break;
    case 5:
      text(sen5, textX, textY);
      break;
    case 6:
      text(sen6, textX, textY);
      break;
    case 7:
      text(sen7, textX, textY);
      break;
    case 8:
      text(sen8, textX, textY);
      break;
    case 9:
      text(sen9, textX, textY);
      break;
    case 10:
      text(sen10, textX, textY);
      break;
    case 11:
      text(sen11, textX, textY);
      break;
    case 12:
      text(sen12, textX, textY);
      break;
  }
  
  //alphaG.beginDraw();
  //alphaG.background(255);
  //alphaG.endDraw();
  //image(alphaG, width/2-450 ,500);         //위치 확인용 코드, 실행시 주석처리 필요
   
   
  //Waveform
  if(running){
    textSize(50);
    textAlign(CENTER);
    fill(0);
    time = time - timeRate;
    if(time < 0.07){
      time = 0.000;
    }
    text(time, width/2, 760);
    
    recorder.beginRecord();

    alphaG.beginDraw();   
    //alphaG.background(255);         //이것도 음파확인용 코드, 실행시 주석처리 필요
    alphaG.stroke(70);
    
    //Waveform 그리는 코드
    for(int i = 0; i < in.bufferSize()-1; i++){
      float x1 = map( i, 0, in.bufferSize()/2, 0, 6 );
      float x2 = map( i+1, 0, in.bufferSize()/2, 0, 6 );

      alphaG.line( x1 + j, 150+in.left.get(i)*300, 
                   x2 + j, 150+in.left.get(i+1)*300 );
    }
    
    alphaG.endDraw();
    image(alphaG, width/2-540 ,380);
    j+= 6;
    
    //시간이 다 됐으면
    if(j == 1080){      
      recorder.endRecord();
      //wav파일 저장
      recorder.save();
      //waveform 이미지 저장
      alphaG.save("../no3_Ticket/waveform/" + str(count) + "_waveform.png");

      count++;
      j = 0;
      
      delay(500);
      randomNum = int(random(1, 13));
      running = false;
    }
  }
}

void update(int x, int y){
  if (overCircle(circleX, circleY, circleSize)){
    circleOver = true;
  }
  else {
    circleOver = false;
  }
  
  if(overButton(x, y)){
    buttonOver = true;
  }
  else {
    buttonOver = false;
  }
}

boolean overCircle(int x, int y, int diameter){
  float distX = x - mouseX;
  float distY = y - mouseY;
  if(sqrt(sq(distX) + sq(distY)) < diameter/2){
    return true;
  }
  else{
    return false;
  }
}

boolean overButton(int x, int y){
  if((x > buttonX - buttonSize && x < buttonX + buttonSize) && (y > buttonY - buttonSize && y < buttonY + buttonSize)){
    return true;
  }
  else {
    return false;
  }
  
}

void mouseClicked(){
  if (circleOver){   

    running = true;
    reset_sketch();
  }
  
  if(buttonOver){
    randomNum = int(random(1, 13));
  }
}
