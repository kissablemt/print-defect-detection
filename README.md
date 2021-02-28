# Print Defect Detection(铭牌印刷缺陷视觉检测系统)

加载过慢可查看README.png
--- 

![picture 1](images/7574d22ad94137e02ffb82f8241e1bf6f4736618d7f32f2c527e2b31882cb4ea.png)  
<center>标准图</center>
<br>


![picture 2](images/de5b5fcfb01750aaac85fdcd3a255246c3007102b0cf8ade6ebe069b5aaac5bf.bmp)  
<center>待测图</center>
<br>

![picture 3](images/291d7379d2971cd743ac44e0ee63737af5083aa51317ab33500067a9cdfd69d4.jpeg)  
<center>效果图</center>
<br>

--- 
## 实现思路及中间处理结果
1. surf获取特征点集；
![picture 4](images/b646e7f3d4ce145617f7b98af32beb70f41d982f825ca4ffe30013a9bad38ad7.jpeg)  

2. 特征点集调优获得标准图到待测图的最优单映射变换矩阵H，然后利用H进行透视变换；
![picture 5](images/c3a4305d005ddda49388f2b8b3a75441e4f6054401acb3eeac4546aad04ab6aa.jpeg)  

3. 变换后的标准图与待测图作差获得图diff；
![picture 6](images/1c227d5ed1aef5875c0907fc0bee170282850bca030469059d465832f36e12d7.jpeg)  

4. 图diff进行阈值化，获得图d_thr;
![picture 7](images/000128b7e800eb9306e7f3823da14bbc27429b8c56c7859d4ebeb1905070b57c.jpeg)  


5. 图d_thr进行均值滤波，获的图dt_blur;
![picture 8](images/34b69cb10dcbf7f9f23eb1c3f36306f05cf8765acc0d6e09580225fc834abc72.jpeg)  


6. 图dt_blur进行闭运算，获的图dtb_mor；
![picture 9](images/7d612b5421abf2f5adbeca32b8647b4ec93fb37fa45c542bce258ffc026b6970.jpeg)  


7. 在图dtb_mor进行轮廓的查找，并过滤轮廓周长小于9的轮廓，然后进行画图，获得最后的效果图final；
![picture 3](images/291d7379d2971cd743ac44e0ee63737af5083aa51317ab33500067a9cdfd69d4.jpeg)  
