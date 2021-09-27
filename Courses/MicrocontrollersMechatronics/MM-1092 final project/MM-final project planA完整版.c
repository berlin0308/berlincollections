/*
PC1~4 PB1~4 按鍵/in(0)
PC5 Buzzer/out(1)
PD0~7 PB 0 6 7 三個顯示器/out(1)
PD0 1 2 個十百
*/

#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>

const int C3=60;
const int D3=53.5;
const int E3=47.6;
const int F3=44.6;
const int G3=40;
const int A3=35.5;

void MakeSound(int n,int eng)
{
	//t 每按一次要歸零
	int t=0;
	
	//約t=50時約為按下按鈕的時長
	while(t<50)
	{
		//關掉buzzer
		PORTC=0b00011110;
		
		//持續多久
		OCR0A=n;                     //設定n 就是代表一個數值而已
		TCCR0A=0x02;                 //CTC mode
		TCCR0B=0x03;                 //start timer p=64
		while((TIFR0&(1<<OCF0A))==0);//wait for flag
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
		
		//要打開buzzer
		PORTC=0b00111110;
		
		//持續多久
		OCR0A=n;                     //設定n
		TCCR0A=0x02;                 //CTC mode
		TCCR0B=0x03;                 //start timer p=64
		while((TIFR0&(1<<OCF0A))==0);//wait for flag
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
		
		//計算總發音時長
		t++;

		displayEng(eng);
		_delay_ms(2);
		//顯示3
		PORTB=0b10011111;
		PORTD=0b10000001;
		_delay_ms(2);
	}
}

void displaycount(int secOne,int secTen,int minu)
{
	for(int i=0;i<4;i++)
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
};

void BGcount()
{
	for(int i=0;i<4;i++)
	{
		OCR0A=255;//設定n
		TCCR0A=0x02;//CTC state
		TCCR0B=0x05;//P=1024
		//wait for flag
		while((TIFR0&(1<<OCF0A))==0);
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
	}
};

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
	
};

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
};

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
	
};

void displayEng(int eng)
{
	if(eng==1)
	{
		PORTB=0b11011110;
		PORTD=0b00110010;
	}
	else if(eng==2)
	{
		PORTB=0b11011110;
		PORTD=0b00000010;
	}
	else if(eng==3)
	{
		PORTB=0b10011110;
		PORTD=0b00110010;
	}
	else if(eng==4)
	{
		PORTB=0b10011110;
		PORTD=0b01110010;
	}
	else if(eng==5)
	{
		PORTB=0b10011110;
		PORTD=0b00010010;
	}
	else if(eng==6)
	{
		PORTB=0b10011110;
		PORTD=0b01000010;
	}
}

int main(void)
{
	//set clock to 1MHz
	CLKPR=(1<<CLKPCE);
	CLKPR=0b00000011;
	
	DDRB=0b11000001;//b1~4 是input
	DDRC=0b00111110;//c1~4 是output
	//B pull up
	PORTB=0b00011110;
	//D out
	DDRD=0b11111111;


	int state=0,last=0,s=0,secTen=0,secOne=0,minu=0,farward=0,back;
	while(1)
	{
		//如果是正數
		if(state==0)
		{
			//上一個狀態是倒數就歸零
			if(last==1)
			{
				farward=0;
				secTen=0;
				secOne=0;
				minu=0;
			}
			displaycount(secOne,secTen,minu);
			farward++;
			secOne=farward%10;
			secTen=farward/10;
			minu=farward/60;
			secTen=secTen-minu*6;

			last=0;

			//按1切成倒數
			PORTC=0b00001110;
			_delay_ms(5);
			if((~PINB)&(1<<PORTB2))
			{
				state=1;
			}

			//按0切成琴
			PORTC=0b00001110;
			_delay_ms(5);
			if((~PINB)&(1<<PORTB1))
			{
				state=2;
			}
		}

		//如果是倒數
		else if(state==1)
		{
			if(last==0)
			{
				back=71;
			}
			displaycount(secOne,secTen,minu);
			back--;
			secOne=back%10;
			secTen=back/10;
			minu=back/60;
			secTen=secTen-minu*6;

			last=1;

			//按1切成正數
			PORTC=0b00001110;
			_delay_ms(5);
			if((~PINB)&(1<<PORTB2))
			{
				state=0;
			}
		}
		//如果是琴
		else if(state==2)
		{
			BGcount();
			farward++;

			//第一橫排
			PORTC = 0b00011100;
			_delay_ms(5);
			if ((~PINB) & (1 << PORTB1))
			{
				MakeSound(F3,4);
			}
			else if ((~PINB) & (1 << PORTB2))
			{
				MakeSound(E3,3);
			}
			else if ((~PINB) & (1 << PORTB3))
			{
				MakeSound(D3,2);
			}
			else if ((~PINB) & (1 << PORTB4))
			{
				MakeSound(C3,1);
			}
			
			//第二橫排
			PORTC = 0b00011010;
			_delay_ms(5);
			if ((~PINB) & (1 << PORTB1))
			{
				MakeSound(G3,5);
			}

			//第三橫排
			PORTC = 0b00010110;
			_delay_ms(5);
			if ((~PINB) & (1 << PORTB1))
			{
				MakeSound(A3,6);
			}

			//關掉螢幕
			PORTB=0b11011111;
			PORTD=0b11111000;

			last=2;

			//按0切成正數
			PORTC=0b00001110;
			_delay_ms(5);
			if((~PINB)&(1<<PORTB1))
			{
				state=0;
			}
		}
	}
}