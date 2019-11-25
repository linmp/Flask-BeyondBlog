# 数据库表

#### 用户信息
**User**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| username | String | 用户名（唯一的） |
| password| String | 密码 |
| gender | String | 性别 |
| avatar | String | 照片路由 |
| info| TEXT | 个人简介 |
| email | String | 邮箱（唯一的） |
| degree | Integer | 等级 |
| create_time| DateTime | 注册的时间 |
| update_time | DateTime | 最近上线时间 |

---
####  博客信息
**Blog**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| title | TEXT |标题 |
| content | TEXT | 内容 |
| summary | TEXT | 简介 |
| logo | String | 封面） |
| status | Integer | 文章状态 1发表可见 2保存草稿不发表 3屏蔽不可见|
| author_id | Integer | 所属用户 |
| tag | relationship |  标签外键关系关联 |
| comment | relationship | 评论外键关系关联 |
| page_view | Integer | 浏览次数 |
| like_number | Integer | 点赞次数 |
| comment_number | Integer |评论次数 |
| create_time | DateTime | 记录创建时间 |
| update_time | DateTime | 记录更新时间 |

---
#### 搜索历史
**SearchHistory**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| keyword | TEXT |搜索内容 |
| user_id | Integer |所属用户 |
| add_time | DateTime |记录添加时间 |

---
#### 收藏文章
**CollectBlogArticle**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| blog_id | Integer |所属博客 |
| user_id | Integer |所属用户 |
| add_time | DateTime |记录添加时间 |

---
#### 关注
**Follow**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| follower_id | Integer |关注者 |
| followed_id | Integer |被关注者 |
| add_time | DateTime |记录添加时间 |

---
#### 私信
**Message**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| sender_id | Integer |发送者 |
| recipient_id | Integer |接收者 |
| content | TEXT | 内容 |
| add_time | DateTime |记录添加时间 |

---
#### 评论博客
**Comment**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| comment_id | Integer |评论对象编号id |
| sender_id | Integer |发送者 |
| recipient_id | Integer |接收者 |
| content | TEXT | 回复内容 |
| type | Integer | 类型，1是评论，2是回复 |
| blog_id | Integer | 所属博客文章 |
| add_time | DateTime |记录添加时间 |

---
#### 用户登录日志
**UserLoginLog**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| user_id | Integer |所属用户 |
| ip | String |ip地址 |
| add_time | DateTime |记录添加时间 |

---
#### 用户操作日志
**UserOperateLog**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| user_id | Integer |所属用户 |
| ip | String |ip地址 |
| detail | String | 操作详情 |
| add_time | DateTime |记录添加时间 |

---
#### 管理员
**Admin**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| username | String | 管理员用户名　（唯一的） |
| password| String | 密码 |
| avatar | String | 头像路由 |
| authority | Integer | 权限等级 |
| create_time| DateTime | 创建时间 |
| update_time | DateTime | 最近上线时间 |

---
#### 管理员登录日志
**AdminLoginLog**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| admin_id | Integer |所属管理员 |
| ip | String |ip地址 |
| add_time | DateTime |记录添加时间 |

---
#### 管理员操作日志
**AdminOperateLog**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| admin_id | Integer |所属管理员 |
| ip | String |ip地址 |
| detail | String | 操作详情 |
| add_time | DateTime |记录添加时间 |


---
#### 标签
**Tag**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| blog_id | Integer |所属的文章编号 |
| name | String |标签名字 |
| add_time | DateTime |记录添加时间 |


---
#### 公告
**Board**

| 参数 | 类型 | 备注 |
| :------| ------: | :------: |
| id | Integer | 编号 |
| title | TEXT |标题 |
| content | TEXT |内容 |
| add_time | DateTime |记录添加时间 |
| admin_id | Integer |所属管理员 |