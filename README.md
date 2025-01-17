# Sungrow Monitor
A python 3 module to allow direct monitoring of sungrow inverters over LAN TCP modbus connections.

Based on a modified version of [thomasfa18 script](https://github.com/thomasfa18/solar-sungrow) please check out their work if you are interested in a solution to upload data to [pvoutput.org](pvoutput.org).

Based on a cut down version of [Meltaxa's solarIoT script](https://github.com/meltaxa/solariot) please check out their work if you are interested in a full on prememsis solution.

The modbus map was generated from the official sungrow modbus specification and contains many registers. These are present simply as a register index to make it easier for anyone else that is looking for the information.

## Getting started
```python
from SungrowModbusClient import Client, sungrow_register

c = Client(sungrow_register.regmap, "192.168.0.120", 502)

c.load_register()

for i in c.inverter:
    print(i, c.inverter[i])
```

## Standard Disclaimer
All Content on this site is provided "as is" without warranty of any kind, either express or implied, including, but not limited to, the implied warranties of merchantability or fitness for a particular purpose, or the warranty of non-infringement. Without limiting the foregoing, the developer makes no warranty that
(i) the services and Content will meet your requirements,
(ii) the services and Content will be uninterrupted, timely, secure, or error-free,
(iii) the results that may be obtained from the use of the service or Content will be effective, accurate or reliable,
(iv) the quality of any products, services, or information purchased or obtained by you from the site will meet your expectations, and
(v) any errors in the software obtained from the site will be corrected. 

This site could include technical or other errors, inaccuracies or typographical errors. "The Developer" may make changes to the Content and Services at this site, including the prices and descriptions of any products or Services listed herein, at any time without notice. The Content or Services at this site may be out of date, and "The Developer" makes no commitment to update such Content or Services. "The Developer" assumes no responsibility for errors or omissions in the information, documents, software, Content and/or services which are referenced by or linked to this site. References to other corporations, their services and products, are provided "as is" without warranty of any kind, either express or implied.

In no event shall "The Developer" be liable to you or any third party for any special, incidental, indirect or consequential damages of any kind, or any damages whatsoever, including, without limitation, those resulting from loss of use, data or profits, whether or not "The Developer" has been advised of the possibility of such damages, and on any theory of liability, arising out of or in connection with the use of this site or of any web site referenced or linked to from this site. Some jurisdictions prohibit the exclusion or limitation of liability for consequential or incidental damages, so the above limitations may not apply to you.

The downloading or other acquisition of any Content through the site is done at your own discretion and risk and with your agreement that you will be solely responsible for any damage to your computer system or loss of data that results from the downloading or acquisition of any such Content. No advice or information, whether oral or written, obtained by you from "The Developer" or through or from the site shall create any warranty not expressly stated in the terms of use.

  - This has been tested on a a sungrow SG5.0RT inverter
  - A list of "valid devices" is included at the top of the modbus map, this came from the sungrow modbus specification document directly. It may work with other devices, I do not know.
  - The script only performs reads of the input registers (function code 04), if you do not know anything about modbus I would highly dicourage you from making changes.
  - In short, you are welcome to use this, but if you do you are agreeing that if something bad happens then it was not my fault and you can't sue me.
