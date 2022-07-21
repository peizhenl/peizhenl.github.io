### 系统环境部署步骤
1.首先，完成python环境的安装
2.打开命令行，确认pip命令可以正常使用
3.在项目根文件目录，执行命令：pip install -r requirements.txt, 完成系统运行环境的安装
4.使用任意一个mysql数据库连接客户端，如：MySQL Workbench或Navicat，打开数据库查询面板，将项目根文件目录下中schema.sql文件里的sql脚本复制到当前打开的查询面板，并执行，完成数据库和数据表的创建
5.最后，在项目根文件目录下，执行：python run.py完成系统的启动
6.输入http://localhost:5000/admin/add.html 完成管理员账号创建，用户名:admin，密码:123456
6.输入以下网址可访问网址: 
    http://localhost:5000  首页界面
    http://localhost:5000/admin/login.html 管理员登陆界面