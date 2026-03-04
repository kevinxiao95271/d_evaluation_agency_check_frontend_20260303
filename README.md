# 机构考核评估系统 - 前端

Vue.js 前端应用，用于浙江省医疗机构质量控制中心考核评估系统。

## 🚀 快速开始

### 环境要求
- Node.js 18.x 或更高版本
- npm 或 yarn

### 安装依赖
```bash
npm install
```

### 开发服务器
```bash
npm run dev
```
访问: http://localhost:5039

### 构建生产版本
```bash
npm run build
```

## 📋 功能特性

### 评委端功能
- 🔐 评委登录认证
- 📋 待评机构列表
- 📊 双模式评分系统
  - 直接打总分模式
  - 逐条打分模式
- 📈 评分进度跟踪

### 管理后台
- 🏢 机构管理 (64个机构)
- 👥 评委管理 (76个评委账号)
- 📝 任务管理
- 📊 评分表模板配置
- 🎁 附加项管理 (主任演讲+8分，秘书参与+2分)
- ⚙️ 系统配置
- 📈 结果统计
- 📋 评分记录管理

### 评分记录管理
- 📊 评分记录列表展示
- 🔍 多维度筛选 (评委、机构、任务、评分模式)
- 📈 实时统计信息
- 👁️ 评分详情查看
- 🗑️ 评分记录删除
- 📤 数据导出 (CSV格式)

## 🔧 技术栈

- **框架**: Vue 3 + Composition API
- **UI库**: Element Plus
- **构建工具**: Vite
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **图标**: Element Plus Icons

## 📊 系统数据

- **评委总数**: 76个 (38个专家评委 + 38个大众评委)
- **参评机构**: 64个 (质控中心 + 技术服务中心)
- **评分任务**: 2,812个 (76评委 × 37机构，回避自己机构)
- **评分条目**: 11个 (4个分类)

## 🔑 测试账号

### 评委账号 (密码: 123456)
- **专家评委**: expert1 ~ expert38
- **大众评委**: public1 ~ public38

### 管理员账号
- **用户名**: admin
- **密码**: admin123

## 🌐 API集成

### 后端服务
- **开发环境**: http://localhost:5031
- **API代理**: Vite开发服务器自动代理 `/api` 到后端

### 主要API端点
- `POST /api/judge/login` - 评委登录
- `GET /api/task/current` - 获取当前任务
- `GET /api/task/pending` - 获取待评任务
- `GET /api/score/submit` - 提交评分
- `GET /api/score/records` - 评分记录管理
- `GET /api/score/statistics` - 评分统计

## 📁 项目结构

```
src/
├── api/                 # API接口定义
├── components/          # 组件
│   └── admin/          # 管理后台组件
├── router/             # 路由配置
├── views/              # 页面组件
│   ├── Login.vue       # 登录页
│   ├── Home.vue        # 评委首页
│   ├── Score.vue       # 评分页面
│   ├── Admin.vue       # 管理后台
│   └── ScoreStatus.vue # 评分状态
└── main.js             # 应用入口
```

## 🎯 开发指南

### 添加新功能
1. 在 `src/api/index.js` 中定义API接口
2. 在 `src/components/` 中创建组件
3. 在 `src/router/index.js` 中配置路由
4. 在对应的视图中使用组件

### 样式规范
- 使用Element Plus组件样式
- 自定义样式使用scoped CSS
- 响应式设计适配移动端

### API调用规范
- 统一使用 `src/api/index.js` 中定义的方法
- 错误处理使用Element Plus的ElMessage
- 加载状态使用loading指示器

## 🚀 部署

### 开发环境
```bash
npm run dev
```

### 生产环境
```bash
npm run build
npm run preview
```

## 📝 更新日志

### v1.0.0 (2026-03-04)
- ✅ 完整的Vue 3前端应用
- ✅ 评委登录和评分功能
- ✅ 管理后台完整功能
- ✅ 评分记录管理系统
- ✅ API集成和错误处理
- ✅ 响应式设计

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。