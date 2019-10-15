# A web application of Django + Vue
使用 Django + Vue “快速” 搭建 WEB应用

## Django
Servdoudou & servdou
+ 照常写就行了
+ 记得migrate
+ 记得collectstatic

## Vue
idioum
+ vue celi搭建

### vue
+ CSRF
从Cookies中获取，附到headers中

### UI
+ MUSE UI
这个问题很大，vue3都出来了，这个却停更好久了
+ Element UI
上传模块

## 部署
可部署到 CentOS: nginx + uwsgi (uWSGI?)
+ 升级py3
+ 升级SQLite3
+ 安装uwsgi & 配置ini
+ 安装nginx & 配置conf
+ 运行就可了(uwsgi可后台：&)
