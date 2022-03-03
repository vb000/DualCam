/*
 * HM.c
 *
 *  Created on: Jul 6, 2020
 *      Author: saffaria
 */

#define CAM_ADR (0x24<<1)
#define TIMEOUT 2

#include "HM.h"

void hm_i2c_write(I2C_HandleTypeDef* hi2c, uint16_t addr, uint8_t data)
{
	uint8_t cmd[3];
	cmd[0] = (uint8_t)(addr >> 8);
	cmd[1] = (uint8_t)(addr);
	cmd[2] = data;
	HAL_I2C_Master_Transmit(hi2c, CAM_ADR, cmd, 3, TIMEOUT);
}

uint8_t hm_i2c_read(I2C_HandleTypeDef* hi2c, uint16_t addr)
{
	uint8_t cmd[3];
	cmd[0] = (uint8_t)(addr >> 8);
	cmd[1] = (uint8_t)(addr);
	uint8_t res = 0x00;
	HAL_I2C_Master_Transmit(hi2c, CAM_ADR, cmd, 2, TIMEOUT);
	HAL_I2C_Master_Receive(hi2c, CAM_ADR, &res, 1, TIMEOUT);
	return res;
}

void hm01b0_init(I2C_HandleTypeDef* hi2c)
{
	uint8_t version=0;
	while(1){
		hm_i2c_write(hi2c, REG_MODE_SELECT, 0x00);
		version = hm_i2c_read(hi2c, REG_MODEL_ID_L);
//		HAL_GPIO_TogglePin(LEDG_GPIO_Port, LEDG_Pin);
		if(version == 0xB0){
			HAL_Delay(2);
			break;

		}

	}
//	HAL_GPIO_TogglePin(LEDR_GPIO_Port, LEDR_Pin);

	hm_i2c_write(hi2c, REG_MODE_SELECT, 0x00);

	hm01b0_init_fixed_rom_qvga_fixed(hi2c);
}

void hm01b0_init_fixed_rom_qvga_fixed(I2C_HandleTypeDef* hi2c)
{
    hm_i2c_write(hi2c,  REG_SW_RESET, 0x00); //Software reset, reset all serial interface registers to its default values
    hm_i2c_write(hi2c, REG_MODE_SELECT, 0x00);//go to stand by mode
    hm_i2c_write(hi2c, REG_ANA_REGISTER_17, 0x00);//register to change the clk source(osc:1 mclk:0), if no mclk it goes to osc by default
    //hm_i2c_write(hi2c, REG_TEST_PATTERN_MODE, TEST_PATTERN_WALKING_1);//Enable the test pattern, set it to walking 1


    //Image size settings. Enable QQVGA.
//    hm_i2c_write(hi2c, REG_QVGA_WIN_EN, 0x01);//Enable QVGA Window
//    hm_i2c_write(hi2c, REG_BIN_RDOUT_X, 0x03);//Horizontal Binning enable
//    hm_i2c_write(hi2c, REG_BIN_RDOUT_Y, 0x03);//Vertical Binning enable
//    hm_i2c_write(hi2c, REG_BINNING_MODE, 0x03);//VERTICAL BIN MODE: Horizontal & Vertical

    hm_i2c_write(hi2c, REG_QVGA_WIN_EN, 0x00);//Enable QVGA Window
    hm_i2c_write(hi2c, REG_BIN_RDOUT_X, 0x01);//full Horizontal
    hm_i2c_write(hi2c, REG_BIN_RDOUT_Y, 0x01);// full Vertical
    hm_i2c_write(hi2c, REG_BINNING_MODE, 0x00);//VERTICAL BIN MODE: Horizontal & Vertical disable
    /*looking at lattice cfg setting*/
//    hm_i2c_write(hi2c, REG_SW_RESET,0x00);


    /*looking at lattice cfg setting*/
    //hm_i2c_write(hi2c, REG_SW_RESET, 0x00);


    hm_i2c_write(hi2c,0x3044,0x0A);
    hm_i2c_write(hi2c,0x3045,0x00);
    hm_i2c_write(hi2c,0x3047,0x0A);
    hm_i2c_write(hi2c,0x3050,0xC0);
    hm_i2c_write(hi2c,0x3051,0x42);
//    hm_i2c_write(hi2c,0x3052,0x50);
    hm_i2c_write(hi2c,0x3053,0x00);
    hm_i2c_write(hi2c,0x3054,0x03);
    hm_i2c_write(hi2c,0x3055,0xF7);
    hm_i2c_write(hi2c,0x3056,0xF8);
    hm_i2c_write(hi2c,0x3057,0x29);
    hm_i2c_write(hi2c,0x3058,0x1F);
//    hm_i2c_write(hi2c,0x3059,0x1E);//bit control
    hm_i2c_write(hi2c,0x3064,0x00);
    hm_i2c_write(hi2c,0x3065,0x04);

    //black level control
    hm_i2c_write(hi2c,0x1000,0x43);
    hm_i2c_write(hi2c,0x1001,0x40);
    hm_i2c_write(hi2c,0x1002,0x32);
    hm_i2c_write(hi2c,0x1003,0x08);//default from lattice 0x08
    hm_i2c_write(hi2c,0x1006,0x01);
    hm_i2c_write(hi2c,0x1007,0x08);//default from lattice 0x08

    hm_i2c_write(hi2c,0x0350,0x7F);


    //Sensor reserved
    hm_i2c_write(hi2c,0x1008,0x00);
    hm_i2c_write(hi2c,0x1009,0xA0);
    hm_i2c_write(hi2c,0x100A,0x60);
    hm_i2c_write(hi2c,0x100B,0x90);//default from lattice 0x90
    hm_i2c_write(hi2c,0x100C,0x40);//default from lattice 0x40

    //Vsync, hsync and pixel shift register
    hm_i2c_write(hi2c, REG_VSYNC_HSYNC_PIXEL_SHIFT_EN, 0x00); //lattice value

    //Statistic control and read only
    hm_i2c_write(hi2c,0x2000,0x07);
    hm_i2c_write(hi2c,0x2003,0x00);
    hm_i2c_write(hi2c,0x2004,0x1C);
    hm_i2c_write(hi2c,0x2007,0x00);
    hm_i2c_write(hi2c,0x2008,0x58);
    hm_i2c_write(hi2c,0x200B,0x00);
    hm_i2c_write(hi2c,0x200C,0x7A);
    hm_i2c_write(hi2c,0x200F,0x00);
    hm_i2c_write(hi2c,0x2010,0xB8);
    hm_i2c_write(hi2c,0x2013,0x00);
    hm_i2c_write(hi2c,0x2014,0x58);
    hm_i2c_write(hi2c,0x2017,0x00);
    hm_i2c_write(hi2c,0x2018,0x9B);

    //Automatic exposure gain control
    hm_i2c_write(hi2c,0x2100,0x01);
    hm_i2c_write(hi2c,0x2101,0x70);//0x70);//lattice 0xA0
    hm_i2c_write(hi2c,0x2102,0x01);//lattice 0x06
    hm_i2c_write(hi2c,0x2104,0x07);
    hm_i2c_write(hi2c,0x2105,0x03);
    hm_i2c_write(hi2c,0x2106,0xA4);
    hm_i2c_write(hi2c,0x2108,0x33);
    hm_i2c_write(hi2c,0x210A,0x00);
    //hm_i2c_write(hi2c,0x210C,0x04);
    hm_i2c_write(hi2c,0x210B,0x80);
    hm_i2c_write(hi2c,0x210F,0x00);
    hm_i2c_write(hi2c,0x2110,0xE9);
    hm_i2c_write(hi2c,0x2111,0x01);
    hm_i2c_write(hi2c,0x2112,0x17);
    hm_i2c_write(hi2c,0x2150,0x03);

    //Sensor exposure gain
    hm_i2c_write(hi2c,0x0205,0x05);//Vikram
    hm_i2c_write(hi2c,0x020E,0x01);//Vikram
    hm_i2c_write(hi2c,0x020F,0x00);//Vikram
    hm_i2c_write(hi2c,0x0202,0x01);//Vikram
    hm_i2c_write(hi2c,0x0203,0x08);//Vikram


//    hm_i2c_write(hi2c,0x3010,0x01); //done in lower lines
//    hm_i2c_write(hi2c,0x0383,0x00); //done in lower lines
//    hm_i2c_write(hi2c,0x0387,0x00); //done in lower lines
//    hm_i2c_write(hi2c,0x0390,0x00); //done in lower lines
//    hm_i2c_write(hi2c,0x3059,0x42); //done in lower lines
//    hm_i2c_write(hi2c,0x3060,0x51); //done in lower lines

//    hm_i2c_write(hi2c,0x0101,0x00);//this part gives error
//    hm_i2c_write(hi2c,0x0100,0x05);

////    hm_i2c_write(hi2c,0x3061,0x20);
////    hm_i2c_write(hi2c,0x3067,0x01);

//    hm_i2c_write(hi2c,0x0104,0xFF);//changed by Ali
//    hm_i2c_write(hi2c,0x0104,0x00);//makes the image look crooked!

    //hm_i2c_write(hi2c,0x0205,0x30);

    /*looking at lattice cfg setting*/

//    hm_i2c_write(hi2c, 0x3044, 0x0A);/*this part gives error*/

    //frame timing control
    hm_i2c_write(hi2c, REG_FRAME_LENGTH_LINES_H, 0x00);//0x00
    hm_i2c_write(hi2c, REG_FRAME_LENGTH_LINES_L, 0x80);//0x80
    hm_i2c_write(hi2c, REG_FRAME_LENGTH_PCK_H, 0x00);//0x00
    hm_i2c_write(hi2c, REG_FRAME_LENGTH_PCK_L, 0xD7);

    hm_i2c_write(hi2c, REG_OSC_CLK_DIV, 0x38);//This is effective when we use external clk, Use the camera in the gated clock mode to make the clock zero when there is no data

    hm_i2c_write(hi2c, REG_BIT_CONTROL, 0x20);//Set the output to send 1 bit serial

//    hm_i2c_write(hi2c, REG_PMU_PROGRAMMABLE_FRAMECNT, 0x01);//set the number of frames to be sent out, it sends N frames

}
void hm01b0_stream(I2C_HandleTypeDef* hi2c, uint8_t frames)
{
	if (frames == 0)
	{
		hm_i2c_write(hi2c, REG_MODE_SELECT, MODE_STREAMING);
	}
	else
	{
		hm_i2c_write(hi2c, REG_PMU_PROGRAMMABLE_FRAMECNT, frames);
		hm_i2c_write(hi2c, REG_MODE_SELECT, MODE_STREAMING2);
	}
}

void hm01b0_trig(I2C_HandleTypeDef* hi2c)
{
	hm_i2c_write(hi2c, REG_MODE_SELECT, MODE_STREAMING3);
}
