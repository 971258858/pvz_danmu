from pymouse import PyMouse

m = PyMouse()
a = m.position()    #获取当前坐标的位置(这个东西到时候可以新建个py 获取坐标)
print(a)

m.move(50, 500)   #鼠标移动到(x,y)位置
a = m.position()
print(a)

m.click(50, 50)  #移动并且在(x,y)位置左击

m.click(300, 300, 2) #(300,300)位置右击