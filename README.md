# Flask-Heler

## 2.0.10
加载默认views hooks 尽量使用真实module name

## 2.0.9
修复cross_domain bug

## 2.0.8
支持加载固定后缀的view 和 hook

## 2.0.7
修复无法一个方法注册两个路由问题

## 2.0.6
修复因为eventlet问题的启动问题

## 2.0.5
支持设置 cross_domain 参数，可以设置 methods, origin, headers
## 2.0.4
删除_packet_data

## 2.0.3
修复
'Flask2' object has no attribute 'session_cookie_name'

## 2.0.2
修复
TypeError: send_file() got an unexpected keyword argument 'cache_timeout'

## 2.0.1
不再支持from flask_helper import globals

## 1.2.7
utils.log支持getLogger

## 1.2.6
utils.registry exist_in 支持 add_not_exist

## 1.2.5
flask_helper.view.View支持view_context_func

## 1.2.4
user agent hook 允许从url参数中取User-Agent
utils.registry add notify and notify_callback

## 1.2.3
user agent hook 允许过滤一些path不校验

## 1.2.2
add HookRegistry

## 1.2.1
删除不必要的print

## 1.2
Flask增加log
Hook也包含log对象，默认使用app的log属性

## 1.1
Flask.run 使 eventlet

## 1.0
只允许python3

## 0.19
扩展功能(cross_domain real_ip handle_30x filter_user_agent)只设置一次

## 0.3
可从 from flask_helper import Flask2 