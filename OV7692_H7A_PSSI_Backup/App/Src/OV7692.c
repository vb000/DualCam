/*
 * OV7692.c
 *
 *  Created on: Dec 10, 2021
 *      Author: saffaria
 */

#include "OV7692.h"
#include "stm32h7xx_hal.h"

/*
 * HM.c
 *
 *  Created on: Jul 6, 2020
 *      Author: saffaria
 */

#define CAM_ADR (0x3C<<1)
#define TIMEOUT 1



void i2c_write(I2C_HandleTypeDef* hi2c, uint8_t addr, uint8_t data)
{
	uint8_t cmd[2];
	cmd[0] = addr;
	cmd[1] = data;
	HAL_I2C_Master_Transmit(hi2c, CAM_ADR, cmd, 2, TIMEOUT);
}

uint8_t i2c_read(I2C_HandleTypeDef* hi2c, uint8_t addr)
{
	uint8_t cmd[1];
	cmd[0] = addr;
	uint8_t res = 0x00;
	HAL_I2C_Master_Transmit(hi2c, CAM_ADR, cmd, 1, TIMEOUT);
	HAL_I2C_Master_Receive(hi2c, CAM_ADR, &res, 1, TIMEOUT);
	return res;
}

void camera_init(I2C_HandleTypeDef* hi2c)
{
	uint8_t version=0;
	while(1){

		version = i2c_read(hi2c, PIDH);

		if(version == 0x76){
//			HAL_GPIO_WritePin(LED_RED_GPIO_Port, LD3 (Red Led)_Pin, GPIO_PIN_RESET);
			break;

		}

	}

    i2c_write(hi2c, REG12 , 0x80);	// System reset
    HAL_Delay(2);
    i2c_write(hi2c, REG12 , 0x10);	// System UN-RESET
    HAL_Delay(2);
    i2c_write(hi2c, REG0C , 0x96);
	i2c_write(hi2c, REG3E , 0x40);	// Suppress PCLK on horiz blank. Set PCLK of YUV output double the PCLK of RAW output.


//
	i2c_write(hi2c, CLKRC, 0x40);

//	i2c_write(hi2c, SHIFT, 0x17);
//	i2c_write(hi2c, HSTART, 0x69);
//	i2c_write(hi2c, HSIZE, 0xA0);
//	i2c_write(hi2c, VSTART, 0x0E);
//	i2c_write(hi2c, VSIZE, 0xF0);
//
//////QVGA
//	i2c_write(hi2c, HSIZE, 0x28);
//	i2c_write(hi2c, VSIZE, 0x3C);
//	i2c_write(hi2c, REG09, 0x0C);
//	 i2c_write(hi2c, REG12 , 0x00);	// System UN-RESET
//	i2c_write(hi2c, REG12 , 0x00);	// System UN-RESET
	i2c_write(hi2c, REG15 , 0x03);
	i2c_write(hi2c, REG82 , 0x03);
//
//////
//	i2c_write(hi2c, REGC8, 0x02);
//	i2c_write(hi2c, REGC9, 0x10);
//	i2c_write(hi2c, REGCA, 0x01);
//	i2c_write(hi2c, REGCB, 0xB0);

//////////
//	i2c_write(hi2c, REGCC, 0x00);
//	i2c_write(hi2c, REGCD, 0xA0);
//	i2c_write(hi2c, REGCE, 0x00);
//	i2c_write(hi2c, REGCF, 0x78);

	//	i2c_write(REGC8, 0x02);
	//	i2c_write(REGC9, 0x0D);
	//	i2c_write(REGCA, 0x01);
	//	i2c_write(REGCB, 0xB0);
	//
	////	i2c_write(REGC8, 0x01);
	////	i2c_write(REGC9, 0x5E);
	////	i2c_write(REGCA, 0x01);
	////	i2c_write(REGCB, 0x20);
	//
	//	i2c_write(REGCC, 0x00);
	//	i2c_write(REGCD, 0xAF);
	//	i2c_write(REGCE, 0x00);
	//	i2c_write(REGCF, 0x90);

//	i2c_write(hi2c, REG81, 0x4D);


	i2c_write(hi2c, REGB4, 0x36);			/// Set the sharpenning and denoise to auto.
	i2c_write(hi2c, REGB5, 0xAF);
	i2c_write(hi2c, REGB6, 0x01);


	i2c_write(hi2c, 0x13 , 0xF7);
//
//
//
//
//	i2c_write(hi2c, AECH , 0x00);
//	i2c_write(hi2c, AECL , 0x1F);




//	i2c_write(hi2c, REG61 , 0x70); //test pattern
//	i2c_write(hi2c, CLKRC, 0x01);		// divide by 2
//	i2c_write(hi2c, REG28 , 0x40);
//	i2c_write(PLL, 0x02); 		// bypass PLL

//
//	i2c_write(hi2c, REG82 , 0x0F);


	version=0;
	while(1){

		version = i2c_read(hi2c, PIDH);

		if(version == 0x76){
			HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_SET);
			break;

		}

	}


}











