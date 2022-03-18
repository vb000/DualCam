/*
 * OV7692.h
 *
 *  Created on: Dec 10, 2021
 *      Author: saffaria
 */

#ifndef INC_OV7692_H_
#define INC_OV7692_H_

#include "main.h"
#include "stm32h7xx_hal.h"

#define GAIN    0x00
#define BGAIN   0x01
#define RGAIN   0x02
#define GGAIN   0x03

#define REG09   0x09
#define PIDH	0x0A
#define REG0C	0x0C
#define REG0E	0x0E
#define AECH	0x0F
#define AECL	0x10
#define CLKRC	0x11
#define REG12	0x12
#define REG15	0x15
#define REG16	0x16
#define HSTART	0x17
#define HSIZE	0x18
#define VSTART	0x19
#define VSIZE	0x1A
#define	SHIFT	0x1B
#define REG28	0x28
#define PLL0	0x30
#define PLL1	0x31
#define REG37	0x37
#define REG3E	0x3E
#define PWC0	0x49

#define REG61	0x61
#define REG81	0x81
#define REG82	0x82

#define REGB4	0xB4
#define REGB5	0xB5
#define REGB6	0xB6

#define REGC8	0xC8
#define REGC9	0xC9
#define REGCA	0xCA
#define REGCB	0xCB

#define REGCC	0xCC
#define REGCD	0xCD
#define REGCE	0xCE
#define REGCF	0xCF

void camera_init(I2C_HandleTypeDef* hi2c2);
void i2c_write(I2C_HandleTypeDef* hi2c2, uint8_t addr, uint8_t data);
uint8_t i2c_read(I2C_HandleTypeDef* hi2c2, uint8_t addr);


#endif /* INC_OV7692_H_ */
