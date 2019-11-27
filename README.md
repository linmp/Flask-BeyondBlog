# Flask-Blog-Python3
An Open Source Blog System that developed with Flask and Python3.
---
### 为什么想搭建个博客呢?
1. 大概去年这个时候我就很想找些博客代码来参考和学习
2. 想搭建个属于自己的博客
3. Python3并且是flask搭建的博客很少
4. **帮助入门的初学者**来学一下完整的一个项目的开发该做的步骤
5. 学了Python这么久,算是一年的成绩单吧

所以打算用**Python3** 采用 **前后端分离**方式来完成个博客

将搭建个**高可用的博客**

如果完成得了的话,将会出个教程来总结一下所用到的技术

星期五, 25. 十月 2019 08:38下午 
*****
**完成的接口有**

#### 管理员

1. 登录  /admin/login
2. 登录状态  /admin/session
3. 登出  /admin/session
4. 发送公告  /admin/bulletin/board
5. 获取登录日志  /admin/login/log
6. 获取操作日志 /admin/operate/log
7. 添加管理员 /admin/ manager
8. 删除管理员 /admin/ manager

...


#### 用户

1. 登录  /main/login
2. 登录状态  /main/session
3. 登出  /main/session
4. 修改密码  /main/password
5. 获取某用户的信息 /main/profile
...


---
**TODO**


- [ ] 验证码注册
- [ ] 异步celery使用
- [ ] 异步发送邮箱
- [ ] 添加websocket
- [ ] 日志和用户信息应该加入redis缓存