# aixia.me
![](https://ooo.0o0.ooo/2017/02/10/589d63356aed4.png)
基于flask的个人博客

##Done
1. 博客框架
2. 添加Markdown
3. Tag分类
4. 分页功能
5. 一般设置，封面图，每页显示文章数，站点标题
6. 后台登录与管理
7. 全文搜索，flask_whooshalchemyPlus + jieba
8. 多说评论
9. 分区式架构
10. 删除代码里无用部分


##To Do
1. 前段几个js,jq
2. 七牛or又拍云，做个自己的图床
3. 找个二维码的api，自动生成当前文章的二维码
4. 代码高亮还是有点问题，可选方案：[prism](http://prismjs.com/)
[highlight](http://www.bootcdn.cn/highlight.js/)


### 预览图
![aiax.info-(iPhone 6 Plus).png](https://ooo.0o0.ooo/2017/02/10/589d60ef8accd.png)
![login.png](https://ooo.0o0.ooo/2017/02/10/589d610276cbf.png)
![](https://ooo.0o0.ooo/2017/02/10/589d60fac869b.png)


## 使用
创建数据库&生成用户：`python manage.py shell`
创建迁移库：`python manage.py db init`
