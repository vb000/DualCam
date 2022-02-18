/*
 * HM.h
 *
 *  Created on: Jul 6, 2020
 *      Author: saffaria
 */

#ifndef INC_HM_H_
#define INC_HM_H_

#include "stm32l4xx_hal.h"
#include "HMRegs.h"
#include "main.h"

void hm_i2c_write(I2C_HandleTypeDef* hi2c1, uint16_t addr, uint8_t data);
uint8_t hm_i2c_read(I2C_HandleTypeDef* hi2c, uint16_t addr);
void hm01b0_init(I2C_HandleTypeDef* hi2c);
void hm01b0_init_fixed_rom_qvga_fixed(I2C_HandleTypeDef* hi2c);
void hm01b0_stream(I2C_HandleTypeDef* hi2c, uint8_t frames);
void hm01b0_trig(I2C_HandleTypeDef* hi2c);


#endif /* INC_HM_H_ */
