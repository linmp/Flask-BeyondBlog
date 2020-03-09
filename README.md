# Flask-Blog-Python3
### An Open Source Blog System that developed with Flask and Python3.

---

### 为什么想搭建个博客呢?
1. 大概去年(2018 12月)这个时候我就很想找些博客代码来参考和学习
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
2. 检查登陆状态  /admin/session
3. 登出  /admin/session
4. 发送公告  /admin/bulletin/board
5. 获取登录日志  /admin/login/log
6. 获取操作日志 /admin/operate/log
7. 添加管理员 /admin/ manager
8. 删除管理员 /admin/ manager
9. 新增标签  /tag
10. 删除标签  /tag
11. 屏蔽用户  /user/status
12. 删除评论   /comment
13. 统计浏览量   /views/numbers
14. 查看所有用户略情   /all/user/<int:page>
15. 查看所有的反馈信息  /feedback/<int:page>"
16. 发博总数   /blog/numbers
17. 注册用户量  /register/numbers
18. 发表博客  /blog/article
19. 修改博客状态  /blog/article/status

...


#### 用户

- 发送注册验证码  /main/sms
- 注册  /main/register
- 登录  /main/login
- 登录状态  /main/session
- 登出  /main/session
- 修改密码  /main/password
- 发送找回密码验证码   /main/reset/password/sms
- 找回密码   /main/password
- 获取个人信息 /main/user/profile/<user_id>
- 设置用户的头像 /main/user/avatar
- 修改用户的用户名 /main/user/username
- 评论  /main/comment
- 删自己评论  /main/comment
- 收藏博客   /main/blog/collect
- 取消收藏博客  /main/blog/collect
- 反馈  /main/message
- 搜索  /main/blog/search/<int:page>
- 获取博客详情 /main /blog/article/detail/<int:blog_id>

...

---
**TODO**

- [ ] 异步celery使用
- [ ] 日志和用户信息应该加入redis缓存
- [ ] 前端搭建

---
