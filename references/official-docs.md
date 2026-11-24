# 按业务场景查 V10 官方开发文档

官方总览列出的适用版本为 V10.5.6，文档版本标为「企业正式版」。用它定位扩展类型、事件或接口名，再到目标版本核对加载器与调用点。已有源码足以定位时可直接从源码入手。外部系统通过 HTTP 调用站点时，查独立的业务系统 API 文档。[开发总览](https://docs.idcsmart.com/docs/V10业务系统开发文档) · [V10 开发规范](https://docs.idcsmart.com/docs/V10业务系统开发文档/V10%20开发规范) · [业务系统 API](https://docs.idcsmart.com/docs/V10业务系统API)

## 从一句需求选择入口

下表中的目录均相对于 `public/plugins/`。

| 要做什么 | 起点和需要核对的地方 | 官方章节 |
| --- | --- | --- |
| 给订单、客户或后台增加业务规则、页面或提醒 | 常规 `addon/`。有后台、会员菜单时分别查 `sidebar.php`、`sidebar_clientarea.php`。自定义路由对照控制器、登录中间件和操作权限。 | [插件开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/插件开发) |
| 销售一种商品，接入供应商履约 | 产品模块 `server/`。从 `metaData()` 和业务所需的方法入手，区分购物车报价 `cartCalculatePrice()` 与实际开通 `createAccount()`。 | [模块开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/模块开发) |
| 在后台首页显示统计卡片 | 独立挂件可从 `widget/<类名>.php` 起步，继承 `Widget`，用 `getData()` 提供数据、`output()` 渲染。已有插件也可通过 `admin_widget` 提供挂件。验收时检查管理组的挂件权限。 | [挂件开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/挂件开发) |
| 接入收款渠道或邮件、短信服务商 | 收款用 `gateway/` 的支付入口，邮件用 `mail/` 的 `send()`，短信用 `sms/`，按实际服务地区核对模板和发送接口。 | [支付](https://docs.idcsmart.com/docs/V10业务系统开发文档/支付接口开发) · [邮件](https://docs.idcsmart.com/docs/V10业务系统开发文档/邮件接口开发) · [短信](https://docs.idcsmart.com/docs/V10业务系统开发文档/短信接口开发) |
| 接入第三方登录、实名认证、图形验证码或对象存储 | 按能力分别查 `oauth/`、`certification/`、`captcha/` 或 `oss/`。例如登录驱动核对 `url()` 和 `callback()` 两端。 | [登录](https://docs.idcsmart.com/docs/V10业务系统开发文档/第三方登录开发) · [实名认证](https://docs.idcsmart.com/docs/V10业务系统开发文档/实名认证接口开发) · [验证码](https://docs.idcsmart.com/docs/V10业务系统开发文档/图形验证码插件开发) · [对象存储](https://docs.idcsmart.com/docs/V10业务系统开发文档/对象存储开发) |

## 核对 Hook 的注册和返回值

官方按前台、后台、公共业务、系统与自动任务分类。选到事件后，沿目标版本检查谁加载处理方法、触发时传入哪些参数，以及调用方如何使用返回值。[Hook 开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/Hook开发)

- 普通 addon 可在主类实现小驼峰方法，例如 `afterOrderCreate($param)`。对照 `app/admin/model/PluginModel.php` 的安装登记与 `app/event/AppInit.php` 对已启用监听的加载。产品模块的 `hooks.php` 则用 `add_hook()`，加载范围可覆盖多个模块，处理前确认商品或服务归属。沿目标模块选一种实际生效的注册方式。[插件开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/插件开发) · [模块开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/模块开发)
- 例如 `before_order_pay` 收到 `order_id`、`gateway` 和 `order`。核对过的 `app/common/model/OrderTmpModel.php` 会遍历各监听结果，遇到含 `status = 400` 的数组即中止支付。单笔取消路径的 `after_order_cancel` 则在事务提交后收到 `id`，调用方没有读取监听返回值。涉及拦截时验证原操作被阻止，涉及事后通知时验证动作已触发。[订单支付前](https://docs.idcsmart.com/docs/V10业务系统开发文档/Hook开发/公共业务Hook/订单、支付与退款/007-订单支付前) · [订单取消后](https://docs.idcsmart.com/docs/V10业务系统开发文档/Hook开发/公共业务Hook/订单、支付与退款/010-订单取消后)

## 按实际页面定位主题

会员中心从 `public/clientarea/template/` 查，购物车从 `public/cart/template/` 查，两者分别有 `pc/` 和 `mobile/`。产品模块的模板在 `public/plugins/server/<模块>/template/` 的 `clientarea/` 或 `cart/` 下，官网另在 `public/web/`。例如排查「购物车可见，会员账单页缺入口」时，分别打开购物车和会员中心，记录设备、启用的主题和实际模板。涉及第三方主题时，沿同一业务路径核对其模板目录。[官网与主题开发](https://docs.idcsmart.com/docs/V10业务系统开发文档/官网与主题开发)
