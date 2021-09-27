 #define F_CPU 1000000UL
 #include <avr/io.h>
 #include <util/delay.h>

 const int noteC3=59.6;
 const int noteD3=53.2;
 const int noteE3=47.4;
 const int noteF3=44.7;
 const int noteG3=39.9;
 const int noteA3=35.5;
 int secOne=0,secTen=0,minu=0;
 int t=0,h=70;

 //數一秒鐘
void count(int secOne,int secTen,int minu)
 {
	 for(int i=0;i<32;i++)
	 {
		 OCR0A=255;//設定n
		 TCCR0A=0x02;//CTC mode
		 TCCR0B=0x05;//P=1024
		 //wait for flag
		 while((TIFR0&(1<<OCF0A))==0)
		 {
			 //display 數字
			 displayO(secOne);
			 _delay_ms(2);     //要delay不然兩位數會來不及切換 而重複顯示
			 display1(secTen);
			 _delay_ms(2);
			 display2(minu);
			 _delay_ms(2);
		 }
		 TCCR0B=0x00;                 //stop timer
		 TIFR0=TIFR0|(1<<OCF0A);      //clear timer
	 }
 }

void BinCout()
{
	//B->input C->output
	DDRB=0b11000001;
	DDRC=0b00111110;
	//B pull up
	PORTB=0xFF;
	// set D
	DDRD=0b11111111;
}

void BoutCin()
{
	//B->output C->input
	DDRB=0b11011111;
	DDRC=0b00100000;
	//C pull up
	PORTC=0b11011111;   // the buzzer is on PC5
	// set D
	DDRD=0b11111111;
}

void displayO(int secOne)
{
	if(secOne==0)
	{
		PORTB=0b11011110;
		PORTD=0b00000001;

	}
	else if(secOne==1)
	{
		PORTB=0b11011111;
		PORTD=0b11001001;

	}
	else if(secOne==2)
	{
		PORTB=0b10011111;
		PORTD=0b00100001;

	}
	else if(secOne==3)
	{
		PORTB=0b10011111;
		PORTD=0b10000001;


	}
	else if(secOne==4)
	{
		PORTB=0b10011110;
		PORTD=0b11001001;

	}
	else if(secOne==5)
	{
		PORTB=0b10011110;
		PORTD=0b10010001;
	}
	else if(secOne==6)
	{
		PORTB=0b10011110;
		PORTD=0b00010001;

	}
	else if(secOne==7)
	{
		PORTB=0b11011110;
		PORTD=0b11000001;


	}
	else if(secOne==8)
	{
		PORTB=0b10011110;
		PORTD=0b00000001;

	}
	else if(secOne==9)
	{
		PORTB=0b10011110;
		PORTD=0b10000001;

	}
	
}

void display1(int secTen)
{
	if(secTen==0)
	{
		PORTB=0b11011110;
		PORTD=0b00000010;

	}
	else if(secTen==1)
	{
		PORTB=0b11011111;
		PORTD=0b11001010;

	}
	else if(secTen==2)
	{
		PORTB=0b10011111;
		PORTD=0b00100010;

	}
	else if(secTen==3)
	{
		PORTB=0b10011111;
		PORTD=0b10000010;


	}
	else if(secTen==4)
	{
		PORTB=0b10011110;
		PORTD=0b11001010;

	}
	else if(secTen==5)
	{
		PORTB=0b10011110;
		PORTD=0b10010010;


	}
	else if(secTen==6)
	{
		PORTB=0b10011110;
		PORTD=0b00010010;


	}
	else if(secTen==7)
	{
		PORTB=0b11011110;
		PORTD=0b11000010;


	}
	else if(secTen==8)
	{
		PORTB=0b10011110;
		PORTD=0b00000010;

	}
	else if(secTen==9)
	{
		PORTB=0b10011110;
		PORTD=0b10000010;

	}
	else if(secTen==12) //C
	{
		PORTB=0b11011110;
		PORTD=0b00110010;
		
	}
	else if(secTen==13) //D
	{
		PORTB=0b11011110;
		PORTD=0b00000010;
		
	}
	else if(secTen==14) //E
	{
		PORTB=0b10011110;
		PORTD=0b00110010;
		
	}
	else if(secTen==15) //F
	{
		PORTB=0b10011110;
		PORTD=0b01110010;
		
	}
	else if(secTen==16) //G
	{
		PORTB=0b11011110;
		PORTD=0b00010010;
		
	}
	else if(secTen==10) //A
	{
		PORTB=0b10011110;
		PORTD=0b01000010;
		
	}
}

void display2(int minu)
{
	if(minu==0)
	{
		PORTB=0b01011110;
		PORTD=0b00000100;

	}
	else if(minu==1)
	{
		PORTB=0b01011111;
		PORTD=0b11001100;

	}
	else if(minu==2)
	{
		PORTB=0b00011111;
		PORTD=0b00100100;

	}
	else if(minu==3)
	{
		PORTB=0b00011111;
		PORTD=0b10000100;


	}
	else if(minu==4)
	{
		PORTB=0b00011110;
		PORTD=0b11001100;

	}
	else if(minu==5)
	{
		PORTB=0b00011110;
		PORTD=0b10010100;


	}
	else if(minu==6)
	{
		PORTB=0b00011110;
		PORTD=0b00010100;


	}
	else if(minu==7)
	{
		PORTB=0b01011110;
		PORTD=0b11000100;


	}
	else if(minu==8)
	{
		PORTB=0b00011110;
		PORTD=0b00000100;

	}
	else if(minu==9)
	{
		PORTB=0b00011110;
		PORTD=0b10000100;

	}
	
}

void MakeSound(int n)
{
	int t=0,c;

	if(n==noteA3)
	c=10;
	if(n==noteC3)
	c=12;
	if(n==noteD3)
	c=13;
	if(n==noteE3)
	c=14;
	if(n==noteF3)
	c=15;
	if(n==noteG3)
	c=16;

	//約t=50時約為按下按鈕的時長
	while(t<250)
	{
		displayO(3);
		//關掉buzzer
		PORTC=0b00011110;
		
		//持續多久
		OCR0A=n;                   //設定n 就是代表一個數值而已
		TCCR0A=0x02;                 //CTC mode
		TCCR0B=0x03;                 //start timer p=64
		while((TIFR0&(1<<OCF0A))==0);//wait for flag
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
		
		display1(c);
		//要打開buzzer
		PORTC=0b00111110;
		
		//持續多久
		OCR0A=n;                   //設定n
		TCCR0A=0x02;                 //CTC mode
		TCCR0B=0x03;                 //start timer p=64
		while((TIFR0&(1<<OCF0A))==0);//wait for flag
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
		
		//計算總發音時長
		t++;
	}
}
 
 int main(void)
 {
 
 //B->output C->input
 DDRB=0b11011111;
 DDRC=0b00100000;
 //C pull up
 PORTC=0b11011111;   //buzzer 要關(有改)
 // set D
 DDRD=0b11111111;
 
 int t=0,secTen=0,secOne=0,minu=0;
 for(int y=0;y<3000;y++)
 { //display 數字
	 displayO(0);
	 _delay_ms(2);     //要delay不然兩位數會來不及切換 而重複顯示
	 display1(0);
	 _delay_ms(2);
	 display2(0);
	 _delay_ms(2);
 }
 while (1)
 {
	 count(secOne,secTen,minu);
	 t++;
	 
	 secOne=t%10;
	 secTen=t/10;
	 minu=t/60;
	 secTen=secTen-minu*6;
	 
	 if(t==22)
	 break;
 }
 DDRD=0b11111000;
 _delay_ms(15000);
 DDRD=0b11111111;
 DDRB=0b11011111;
 
 //C
 MakeSound(noteC3);

 PORTC=0b11011111;

 
 _delay_ms(5000);
 
 //D
 MakeSound(noteD3);
 PORTC=0b11011111;
 _delay_ms(5000);
 
 //E
 
 MakeSound(noteE3);
 PORTC=0b11011111;
 _delay_ms(5000);

 //F
 MakeSound(noteF3);
 PORTC=0b11011111;
 _delay_ms(5000);
 
 //G
 MakeSound(noteG3);
 PORTC=0b11011111;
 _delay_ms(5000);
 
 //A
 MakeSound(noteA3);
 PORTC=0b11011111;
 _delay_ms(5000);

 _delay_ms(10000);
 
 t=29;
 while (1)
 {
	 
	 t++;
	 
	 secOne=t%10;
	 secTen=t/10;
	 minu=t/60;
	 secTen=secTen-minu*6;
	 count(secOne,secTen,minu);
	 
	 if(t==70)
	 break;
 }
 for(int y=0;y<2500;y++)
 { //display 數字
	 displayO(0);
	 _delay_ms(2);     //要delay不然兩位數會來不及切換 而重複顯示
	 display1(1);
	 _delay_ms(2);
	 display2(1);
	 _delay_ms(2);
 }
 t=70;
 while (1)
 {
	 count(secOne,secTen,minu);
	 t--;
	 
	 secOne=t%10;
	 secTen=t/10;
	 minu=t/60;
	 secTen=secTen-minu*6;
	 
	 if(t==42)
	 break;
 }
 
 _delay_ms(10000);
 t=0;
 secOne=secTen=minu=0;
 while (1)
 {
	 count(secOne,secTen,minu);
	 t++;
	 
	 secOne=t%10;
	 secTen=t/10;
	 minu=t/60;
	 secTen=secTen-minu*6;
	 
	 if(t==200)
	 break;
 }
 }